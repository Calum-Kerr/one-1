import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from processing.ocr_preprocessing import needs_ocr
from processing.ocr_execution import run_ocr

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        if needs_ocr(filepath):
            filepath = run_ocr(filepath)
            
        return jsonify({'success': True, 'filepath': filepath})
    
    return jsonify({'error': 'Invalid file type'}), 400
