def rgb_to_hex(rgb_tuple):
    """Convert RGB tuple to hex color code"""
    return '#{:02x}{:02x}{:02x}'.format(*[int(255 * x) for x in rgb_tuple])

def extract_color(span):
    """Extract color from PyMuPDF span"""
    color = span.get('color', (0, 0, 0))
    return rgb_to_hex(color)

def extract_color_css(span):
    """Convert color to CSS"""
    return f'color: {extract_color(span)};'
