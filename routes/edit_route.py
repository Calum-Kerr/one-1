from flask import Blueprint, render_template, jsonify, request, current_app
import os
import fitz
from utils.font_mapping import get_font_css
from text_attributes.bold_handling import extract_bold_css
from text_attributes.italic_handling import extract_italic_css
from text_attributes.underline_handling import extract_underline_css

edit_bp = Blueprint('edit', __name__)

@edit_bp.route('/edit/<filename>')
def edit_pdf(filename):
    """Render the PDF editor page"""
    # Construct full filepath from filename
    filepath = os.path.join(current_app.root_path, 'uploads', filename)
    return render_template('edit.html', filepath=filepath)

@edit_bp.route('/api/get-text', methods=['POST'])
def get_text():
    """Get text content from PDF"""
    filepath = request.json.get('filepath')
    page_num = request.json.get('page', 0)
    
    try:
        doc = fitz.open(filepath)
        page = doc[page_num]
        
        # Initialize response data
        text_data = {
            'text_elements': [],
            'total_pages': doc.page_count
        }
        
        # Get words with basic parameters
        words = page.get_text("words")
        if not words:
            doc.close()
            return jsonify(text_data)
            
        # Track line information
        current_line = []
        current_y = None
        line_spacing = 14  # Base line spacing in points
        
        # Process words
        for word in words:
            x0, y0, x1, y1, text, *_ = word  # Safely unpack word tuple
            
            # Skip empty text
            if not text.strip():
                continue
                
            # Check if this is a new line
            if current_y is None:
                current_y = y0
            elif abs(y0 - current_y) > line_spacing:
                # Process completed line
                if current_line:
                    text_data['text_elements'].append({
                        'text': ' '.join(word['text'] for word in current_line),
                        'style': 'font-family: Helvetica; font-size: 11px; line-height: 1.5;',
                        'bbox': [
                            min(w['bbox'][0] for w in current_line),
                            min(w['bbox'][1] for w in current_line),
                            max(w['bbox'][2] for w in current_line),
                            max(w['bbox'][3] for w in current_line)
                        ]
                    })
                current_line = []
                current_y = y0
            
            # Add word to current line
            current_line.append({
                'text': text,
                'bbox': [x0, y0, x1, y1]
            })
        
        # Add last line if exists
        if current_line:
            text_data['text_elements'].append({
                'text': ' '.join(word['text'] for word in current_line),
                'style': 'font-family: Helvetica; font-size: 11px; line-height: 1.5;',
                'bbox': [
                    min(w['bbox'][0] for w in current_line),
                    min(w['bbox'][1] for w in current_line),
                    max(w['bbox'][2] for w in current_line),
                    max(w['bbox'][3] for w in current_line)
                ]
            })
        
        doc.close()
        return jsonify(text_data)
        
    except Exception as e:
        print(f"Text extraction error: {str(e)}")  # Add error logging
        if 'doc' in locals():
            doc.close()
        return jsonify({'error': str(e)}), 500

@edit_bp.route('/api/save-text', methods=['POST'])
def save_text():
    """Save edited text back to PDF"""
    filepath = None
    doc = None
    try:
        data = request.json
        filepath = data.get('filepath')
        page_num = int(data.get('page', 0))
        text = data.get('text', '').strip()
        bbox = data.get('bbox')

        if not all([filepath, isinstance(bbox, list), len(bbox) == 4]):
            raise ValueError("Invalid parameters")
            
        # Create a copy first
        temp_path = f"{filepath}.tmp"
        with open(filepath, 'rb') as src:
            with open(temp_path, 'wb') as dst:
                dst.write(src.read())

        # Work with the copy
        doc = fitz.open(temp_path)
        page = doc[page_num]
        
        # Create white rectangle
        rect = fitz.Rect(bbox)
        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
        
        # Insert text
        page.insert_text(
            point=(bbox[0] + 2, bbox[1] + 11),
            text=text,
            fontname="helv",
            fontsize=11,
            color=(0, 0, 0)
        )
        
        # Save and close
        doc.save(temp_path)
        doc.close()
        doc = None
        
        # Replace original
        os.replace(temp_path, filepath)
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Save error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if doc:
            try:
                doc.close()
            except:
                pass
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
