def extract_size(span):
    """Extract font size from PyMuPDF span"""
    return span.get('size', 12)

def normalize_size(size):
    """Normalize font size to reasonable bounds"""
    return min(max(size, 6), 72)

def extract_size_css(span):
    """Convert font size to CSS"""
    size = normalize_size(extract_size(span))
    return f'font-size: {size}pt;'
