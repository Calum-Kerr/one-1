from flask import Blueprint, send_file, jsonify, current_app
import os
from utils.error_handler import PDFError

download_bp = Blueprint('download', __name__)

@download_bp.route('/download/<filename>')
def download_pdf(filename):
    """Handle PDF download"""
    try:
        filepath = os.path.join(current_app.root_path, 'uploads', filename)
        if not os.path.exists(filepath):
            raise PDFError("File not found")
            
        return send_file(
            filepath,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
