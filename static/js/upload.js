document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (data.success && data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    } catch (error) {
        console.error('Upload failed:', error);
    }
});
