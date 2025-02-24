from flask import Blueprint, send_file, request, jsonify
from utils.pdf_writer import PDFWriter
import os

download_bp = Blueprint('download', __name__)

@download_bp.route('/download', methods=['POST'])
def download_pdf():
    """Process changes and return modified PDF"""
    input_path = request.json.get('filepath')
    changes = request.json.get('changes', [])
    
    if not input_path or not os.path.exists(input_path):
        return jsonify({'error': 'Invalid file path'}), 400
        
    output_path = input_path.replace('.pdf', '_modified.pdf')
    
    writer = PDFWriter(input_path)
    writer.apply_text_changes(changes)
    writer.save(output_path)
    
    return send_file(
        output_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='modified.pdf'
    )
