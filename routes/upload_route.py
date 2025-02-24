import os
from flask import Blueprint, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from processing.ocr_preprocessing import needs_ocr
from processing.ocr_execution import run_ocr
from utils.validator import InputValidator

upload_bp = Blueprint('upload', __name__)

def ensure_upload_folder():
    """Ensure upload folder exists"""
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and InputValidator.validate_pdf_file(file):
        try:
            upload_folder = ensure_upload_folder()
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            if needs_ocr(filepath):
                filepath = run_ocr(filepath)
                
            # Use relative path for URL
            relative_path = os.path.relpath(filepath, current_app.root_path)
            return jsonify({
                'success': True,
                'filepath': filepath,
                'message': 'File processed successfully',
                'redirect_url': url_for('edit.edit_pdf', filename=os.path.basename(filepath))
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400
