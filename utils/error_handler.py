from flask import jsonify
from functools import wraps

class PDFError(Exception):
    """Base class for PDF processing errors"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def handle_pdf_errors(f):
    """Decorator to handle PDF processing errors"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except PDFError as e:
            return jsonify({'error': e.message}), e.status_code
        except Exception as e:
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper
