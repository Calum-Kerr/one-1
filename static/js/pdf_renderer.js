class PDFRenderer {
    constructor(container, filepath) {
        this.container = container;
        this.filepath = filepath;
        this.currentPage = 1;
        this.zoom = 1.0;
        this.loading = false;
        this.pageCount = 0;
    }

    async initialize() {
        try {
            const response = await fetch('/api/get-text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filepath: this.filepath })
            });
            
            const data = await response.json();
            this.pageCount = data.pageCount;
            this.renderPage(1);
            this.setupEventListeners();
        } catch (error) {
            console.error('Failed to initialize PDF renderer:', error);
        }
    }

    setupEventListeners() {
        document.getElementById('zoomLevel').addEventListener('change', (e) => {
            this.setZoom(parseFloat(e.target.value));
        });

        document.getElementById('pageNumber').addEventListener('change', (e) => {
            this.goToPage(parseInt(e.target.value));
        });
    }

    async renderPage(pageNumber) {
        if (this.loading || pageNumber < 1 || pageNumber > this.pageCount) return;
        
        this.loading = true;
        try {
            const response = await fetch('/api/render-page', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    filepath: this.filepath,
                    page: pageNumber,
                    zoom: this.zoom
                })
            });
            
            const pageData = await response.json();
            this.updatePageContent(pageData);
        } catch (error) {
            console.error('Failed to render page:', error);
        } finally {
            this.loading = false;
        }
    }

    updatePageContent(pageData) {
        this.container.innerHTML = '';
        pageData.elements.forEach(element => {
            const div = document.createElement('div');
            div.textContent = element.text;
            div.style.cssText = element.style;
            div.className = 'text-span';
            div.dataset.bbox = JSON.stringify(element.bbox);
            this.container.appendChild(div);
        });
    }
}
