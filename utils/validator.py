from werkzeug.datastructures import FileStorage
import magic
import os
from utils.error_handler import PDFError

class InputValidator:
    ALLOWED_MIME_TYPES = {'application/pdf'}
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

    @staticmethod
    def validate_pdf_file(file: FileStorage) -> bool:
        """Validate uploaded file"""
        if not isinstance(file, FileStorage):
            return False
            
        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        if size > InputValidator.MAX_FILE_SIZE:
            return False
            
        # Check mime type
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)
        
        return mime in InputValidator.ALLOWED_MIME_TYPES

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
