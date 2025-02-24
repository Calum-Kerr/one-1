def extract_opacity(span):
    """Extract opacity value from span"""
    opacity = span.get('opacity', 1.0)
    return max(0.0, min(1.0, opacity))  # Clamp between 0 and 1

def extract_opacity_css(span):
    """Convert opacity to CSS"""
    opacity = extract_opacity(span)
    return f'opacity: {opacity};' if opacity < 1 else ''
