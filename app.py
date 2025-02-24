from flask import Flask, render_template
from routes.upload_route import upload_bp
from routes.edit_route import edit_bp
from routes.download_route import download_bp

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(download_bp)

@app.route('/')
def index():
    """Render the index page"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
