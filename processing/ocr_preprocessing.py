import fitz
from config.ocr_settings import OCR_CONFIDENCE_THRESHOLD

def needs_ocr(pdf_path):
    """Determine if document needs OCR"""
    doc = fitz.open(pdf_path)
    text_content = 0
    
    for page in doc:
        if len(page.get_text().strip()) > 0:
            text_content += 1
    
    doc.close()
    return text_content / doc.page_count < 0.1
