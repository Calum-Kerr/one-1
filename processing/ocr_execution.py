import ocrmypdf
from config.ocr_settings import OCR_SETTINGS
import os

def run_ocr(input_path):
    """Execute OCR on PDF file"""
    output_path = input_path.replace('.pdf', '_ocr.pdf')
    try:
        ocrmypdf.ocr(
            input_path,
            output_path,
            **OCR_SETTINGS
        )
        if os.path.exists(output_path):
            return output_path
    except Exception as e:
        print(f"OCR failed: {str(e)}")
    return input_path
