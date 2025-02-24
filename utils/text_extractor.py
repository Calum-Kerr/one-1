from text_attributes.bold_handling import extract_bold_css
from text_attributes.italic_handling import extract_italic_css
from text_attributes.underline_handling import extract_underline_css
from text_attributes.color_handling import extract_color_css
from text_attributes.size_handling import extract_size_css
from text_attributes.alignment_handling import extract_alignment_css
from text_attributes.margins_handling import extract_margins_css

class TextExtractor:
    @staticmethod
    def extract_styles(span):
        """Extract all style information from a span"""
        styles = [
            extract_bold_css(span),
            extract_italic_css(span),
            extract_underline_css(span),
            extract_color_css(span),
            extract_size_css(span),
            extract_alignment_css(span),
            extract_margins_css(span)
        ]
        return ' '.join(filter(None, styles))

    @staticmethod
    def extract_text_with_styles(page_dict):
        """Extract text with all styling information"""
        text_elements = []
        
        for block in page_dict.get('blocks', []):
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    text_elements.append({
                        'text': span.get('text', ''),
                        'style': TextExtractor.extract_styles(span),
                        'bbox': span.get('bbox', (0, 0, 0, 0))
                    })
                    
        return text_elements
