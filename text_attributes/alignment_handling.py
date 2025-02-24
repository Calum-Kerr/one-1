def extract_alignment(span):
    """Extract text alignment from PyMuPDF span"""
    flags = span.get('flags', 0)
    if flags & 8:  # Center aligned
        return 'center'
    elif flags & 16:  # Right aligned
        return 'right'
    return 'left'  # Default alignment

def extract_alignment_css(span):
    """Convert alignment to CSS"""
    return f'text-align: {extract_alignment(span)};'
