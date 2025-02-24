class PDFEditor {
    constructor() {
        this.changes = [];
        this.selectedText = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('boldBtn').addEventListener('click', () => this.toggleStyle('bold'));
        document.getElementById('italicBtn').addEventListener('click', () => this.toggleStyle('italic'));
        document.getElementById('underlineBtn').addEventListener('click', () => this.toggleStyle('underline'));
        document.getElementById('saveBtn').addEventListener('click', () => this.saveChanges());
    }

    toggleStyle(style) {
        if (!this.selectedText) return;
        
        const change = {
            text: this.selectedText.text,
            bbox: this.selectedText.bbox,
            page: this.selectedText.page,
            [style]: true
        };
        
        this.changes.push(change);
        this.updatePreview();
    }

    async saveChanges() {
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    changes: this.changes,
                    filepath: document.getElementById('filepath').value
                })
            });
            
            if (response.ok) {
                window.location.href = response.url;
            }
        } catch (error) {
            console.error('Failed to save changes:', error);
        }
    }
}

new PDFEditor();
