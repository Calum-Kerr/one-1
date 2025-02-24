class ToolbarHandler {
    constructor(editor) {
        this.editor = editor;
        this.initializeListeners();
    }

    initializeListeners() {
        document.querySelectorAll('.style-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleStyleClick(e));
        });

        document.getElementById('fontSelect').addEventListener('change', (e) => {
            this.handleFontChange(e.target.value);
        });

        document.getElementById('undoBtn').addEventListener('click', () => {
            this.editor.undo();
        });

        document.getElementById('redoBtn').addEventListener('click', () => {
            this.editor.redo();
        });
    }

    handleStyleClick(event) {
        const style = event.target.closest('.style-btn').dataset.style;
        this.editor.applyStyle(style);
        event.target.closest('.style-btn').classList.toggle('active');
    }

    handleFontChange(fontFamily) {
        if (this.editor.selectedText) {
            this.editor.applyFont(fontFamily);
        }
    }

    updateButtonStates(styles) {
        document.querySelectorAll('.style-btn').forEach(btn => {
            const style = btn.dataset.style;
            btn.classList.toggle('active', styles.includes(style));
        });
    }
}
