def extract_line_height(span):
    """Extract line height information from span"""
    line = span.get('line', {})
    return line.get('height', 0)

def extract_char_spacing(span):
    """Extract character spacing from span"""
    return span.get('char_spacing', 0)

def extract_spacing_css(span):
    """Convert spacing attributes to CSS"""
    line_height = extract_line_height(span)
    char_spacing = extract_char_spacing(span)
    
    css_parts = []
    if line_height:
        css_parts.append(f'line-height: {line_height}px')
    if char_spacing:
        css_parts.append(f'letter-spacing: {char_spacing}px')
    
    return '; '.join(css_parts)
