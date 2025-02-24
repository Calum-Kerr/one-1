import re

def extract_bold(span):
    """Extract bold attribute from PyMuPDF span"""
    return bool('bold' in span.get('font', '').lower())

def apply_bold(text, is_bold):
    """Apply bold formatting to text"""
    if is_bold:
        return f'<strong>{text}</strong>'
    return text

def extract_bold_css(span):
    """Convert bold attribute to CSS"""
    return 'font-weight: bold;' if extract_bold(span) else ''
