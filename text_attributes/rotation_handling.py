def extract_rotation(span):
    """Extract rotation angle from span"""
    matrix = span.get('transform', [1, 0, 0, 1, 0, 0])
    if len(matrix) >= 4:
        # Calculate rotation angle from transformation matrix
        angle = round(math.atan2(matrix[1], matrix[0]) * 180 / math.pi, 2)
        return angle
    return 0

def extract_rotation_css(span):
    """Convert rotation to CSS transform"""
    angle = extract_rotation(span)
    return f'transform: rotate({angle}deg);' if angle != 0 else ''
