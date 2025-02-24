import tempfile

PROCESSING_SETTINGS = {
    'temp_dir': tempfile.gettempdir(),
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'allowed_extensions': {'.pdf'},
    'compression_level': 2,  # 0-4, higher = smaller file but slower
    'max_image_resolution': 300  # DPI
}

ERROR_MESSAGES = {
    'file_too_large': 'File exceeds maximum size limit',
    'invalid_extension': 'Invalid file type',
    'processing_error': 'Error processing PDF file',
    'permission_error': 'Insufficient permissions to modify file'
}

CLEANUP_SETTINGS = {
    'delete_temp_after': 3600,  # seconds
    'max_temp_files': 100
}
