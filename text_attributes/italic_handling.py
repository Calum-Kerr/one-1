def extract_italic(span):
    """Extract italic attribute from PyMuPDF span"""
    return bool('italic' in span.get('font', '').lower())

def apply_italic(text, is_italic):
    """Apply italic formatting to text"""
    if is_italic:
        return f'<em>{text}</em>'
    return text

def extract_italic_css(span):
    """Convert italic attribute to CSS"""
    return 'font-style: italic;' if extract_italic(span) else ''
