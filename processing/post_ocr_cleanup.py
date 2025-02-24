import re

def remove_artifacts(text):
    """Remove common OCR artifacts"""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove isolated symbols
    text = re.sub(r'\s[^a-zA-Z0-9\s]{1}\s', ' ', text)
    return text.strip()

def fix_common_errors(text):
    """Fix common OCR mistakes"""
    replacements = {
        'l1': 'll',  # Common OCR confusion
        '0O': 'OO',
        'rn': 'm',
    }
    for error, fix in replacements.items():
        text = text.replace(error, fix)
    return text

def cleanup_ocr_text(text):
    """Apply all cleanup operations"""
    text = remove_artifacts(text)
    text = fix_common_errors(text)
    return text
