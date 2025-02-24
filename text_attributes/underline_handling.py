def extract_underline(span):
    """Extract underline attribute from PyMuPDF span"""
    return bool(span.get('flags', 0) & 4)  # 4 is the underline flag in PyMuPDF

def apply_underline(text, is_underlined):
    """Apply underline formatting to text"""
    if is_underlined:
        return f'<u>{text}</u>'
    return text

def extract_underline_css(span):
    """Convert underline attribute to CSS"""
    return 'text-decoration: underline;' if extract_underline(span) else ''
