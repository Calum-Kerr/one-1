document.addEventListener('DOMContentLoaded', function() {
    const editor = {
        selectedText: null,
        changes: [],

        init() {
            this.bindEvents();
            this.loadPDF();
        },

        bindEvents() {
            document.querySelectorAll('.style-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    this.applyStyle(e.target.dataset.style);
                });
            });

            document.getElementById('saveBtn').addEventListener('click', () => {
                this.saveChanges();
            });
        },

        async loadPDF() {
            const response = await fetch('/api/get-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filepath: document.getElementById('filepath').value
                })
            });
            
            const textData = await response.json();
            this.renderText(textData);
        },

        renderText(textData) {
            const container = document.getElementById('pdfContainer');
            container.innerHTML = '';
            
            textData.forEach(span => {
                const div = document.createElement('div');
                div.textContent = span.text;
                div.style.cssText = span.style;
                div.className = 'text-span';
                container.appendChild(div);
            });
        }
    };

    editor.init();
});
