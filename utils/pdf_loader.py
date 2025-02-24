import fitz
from utils.error_handler import PDFError

class PDFLoader:
    def __init__(self, filepath):
        try:
            self.doc = fitz.open(filepath)
            self.page_count = self.doc.page_count
        except Exception as e:
            raise PDFError(f"Failed to load PDF: {str(e)}")

    def get_page_text(self, page_num):
        """Extract text with formatting from specific page"""
        if not 0 <= page_num < self.page_count:
            raise PDFError(f"Invalid page number: {page_num}")
            
        page = self.doc[page_num]
        return page.get_text("dict")

    def close(self):
        """Close the document"""
        if hasattr(self, 'doc'):
            self.doc.close()
