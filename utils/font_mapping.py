from config.allowed_fonts import ALLOWED_FONTS, DEFAULT_FONT

def validate_font(font_name):
    """Validate and map fonts to allowed alternatives"""
    if not font_name:
        return DEFAULT_FONT
    
    normalized_font = font_name.split('-')[0].strip()
    return ALLOWED_FONTS.get(normalized_font, DEFAULT_FONT)

def get_font_css(span):
    """Convert font information to CSS"""
    font_name = validate_font(span.get('font'))
    font_size = span.get('size', 12)
    return f'font-family: {font_name}; font-size: {font_size}pt;'
