import fitz
from config.ocr_settings import OCR_CONFIDENCE_THRESHOLD

def needs_ocr(pdf_path):
    """Determine if document needs OCR"""
    try:
        doc = fitz.open(pdf_path)
        text_content = 0
        page_count = doc.page_count
        
        for page in doc:
            if len(page.get_text().strip()) > 0:
                text_content += 1
                
        doc.close()
        return (text_content / page_count) < 0.1 if page_count > 0 else True
        
    except Exception as e:
        print(f"Error checking OCR need: {str(e)}")
        return True
    finally:
        if 'doc' in locals():
            try:
                doc.close()
            except:
                pass
