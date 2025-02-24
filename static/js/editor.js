class PDFEditor {
    constructor() {
        this.currentPage = 0;  // Start from page 0
        this.totalPages = 1;
        this.filepath = document.getElementById('filepath').value;
        this.scale = 1;
        this.init();
    }

    async init() {
        await this.loadText();
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('nextPage')?.addEventListener('click', () => this.changePage(1));
        document.getElementById('prevPage')?.addEventListener('click', () => this.changePage(-1));
        
        // Text editing listeners
        document.querySelectorAll('.text-span').forEach(span => {
            span.addEventListener('click', (e) => this.makeEditable(e.target));
        });

        document.getElementById('zoomLevel')?.addEventListener('change', (e) => {
            this.scale = parseFloat(e.target.value);
            this.loadText();
        });
        
        document.getElementById('downloadBtn')?.addEventListener('click', () => {
            window.location.href = `/download/${this.filepath.split('/').pop()}`;
        });
    }

    async loadText() {
        try {
            const response = await fetch('/api/get-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filepath: this.filepath,
                    page: this.currentPage
                })
            });

            const data = await response.json();
            if (data.error) {
                console.error(data.error);
                return;
            }

            this.renderText(data.text_elements || []);
            this.totalPages = data.total_pages || 1;
            this.updatePageCounter();
        } catch (error) {
            console.error('Error loading text:', error);
        }
    }

    renderText(textElements) {
        const container = document.getElementById('pdfContainer');
        container.innerHTML = '';
        container.style.transform = `scale(${this.scale})`;

        textElements.forEach(element => {
            const span = document.createElement('div');
            span.className = 'text-span';
            span.textContent = element.text;
            span.style.cssText = element.style;
            
            const [x, y, x2, y2] = element.bbox;
            span.style.left = `${x}px`;
            span.style.top = `${y}px`;
            span.style.width = `${Math.max(x2 - x, 10)}px`;  // Minimum width
            span.dataset.bbox = JSON.stringify(element.bbox);
            
            span.addEventListener('click', () => this.makeEditable(span));
            container.appendChild(span);
        });
    }

    makeEditable(element) {
        if (element.getAttribute('contenteditable') === 'true') return;
        
        element.contentEditable = true;
        element.focus();
        
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(element);
        selection.removeAllRanges();
        selection.addRange(range);
        
        const saveChanges = () => {
            const newText = element.textContent.trim();
            if (newText !== '') {
                this.saveTextChanges(element);
            }
            element.contentEditable = false;
        };

        element.addEventListener('blur', saveChanges, { once: true });
        element.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                element.blur();
            }
        });
    }

    async saveTextChanges(element) {
        const originalText = element.textContent;
        element.contentEditable = false;
        
        try {
            const response = await fetch('/api/save-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filepath: this.filepath,
                    text: originalText,
                    bbox: JSON.parse(element.dataset.bbox),
                    page: this.currentPage
                })
            });
            
            const data = await response.json();
            if (!data.success) {
                throw new Error(data.error || 'Save failed');
            }
            
            // Reload the page content after successful save
            await this.loadText();
            
        } catch (error) {
            console.error('Save error:', error);
            element.classList.add('save-error');
            element.textContent = originalText;
            
            setTimeout(() => {
                element.classList.remove('save-error');
                this.loadText();  // Reload to ensure consistency
            }, 2000);
        }
    }

    async changePage(delta) {
        const newPage = this.currentPage + delta;
        if (newPage < 1 || newPage > this.totalPages) return;

        this.currentPage = newPage;
        await this.loadText();
    }

    updatePageCounter() {
        const counter = document.getElementById('pageCounter');
        if (counter) {
            counter.textContent = `Page ${this.currentPage} of ${this.totalPages}`;
        }
    }
}

// Initialize editor when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PDFEditor();
});
