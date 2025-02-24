def extract_transform_matrix(span):
    """Extract full transform matrix from span"""
    return span.get('transform', [1, 0, 0, 1, 0, 0])

def extract_scale(matrix):
    """Extract scale factors from transform matrix"""
    if len(matrix) >= 4:
        scale_x = round(math.sqrt(matrix[0]**2 + matrix[1]**2), 3)
        scale_y = round(math.sqrt(matrix[2]**2 + matrix[3]**2), 3)
        return scale_x, scale_y
    return 1, 1

def extract_transform_css(span):
    """Convert transformation to CSS"""
    matrix = extract_transform_matrix(span)
    if matrix == [1, 0, 0, 1, 0, 0]:  # Identity matrix
        return ''
        
    return f'transform: matrix({",".join(str(x) for x in matrix)});'
