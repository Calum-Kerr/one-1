import os
from utils.error_handler import PDFError

class InputValidator:
    @staticmethod
    def validate_pdf_file(filepath):
        """Validate PDF file existence and format"""
        if not os.path.exists(filepath):
            raise PDFError("File not found")
            
        if not filepath.lower().endswith('.pdf'):
            raise PDFError("Invalid file format")
            
        if os.path.getsize(filepath) > 100 * 1024 * 1024:  # 100MB
            raise PDFError("File too large")
        
        return True

    @staticmethod
    def validate_bbox(bbox):
        """Validate bounding box coordinates"""
        if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
            raise PDFError("Invalid bbox format")
            
        if not all(isinstance(x, (int, float)) for x in bbox):
            raise PDFError("Invalid bbox coordinates")
            
        if bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
            raise PDFError("Invalid bbox dimensions")
        
        return True
