def extract_margins(span):
    """Extract margin information from PyMuPDF span"""
    bbox = span.get('bbox', (0, 0, 0, 0))
    return {
        'left': bbox[0],
        'top': bbox[1],
        'right': bbox[2],
        'bottom': bbox[3]
    }

def extract_margins_css(span):
    """Convert margins to CSS"""
    margins = extract_margins(span)
    return f'margin: {margins["top"]}px {margins["right"]}px {margins["bottom"]}px {margins["left"]}px;'
