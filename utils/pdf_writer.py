import fitz
from text_attributes.bold_handling import apply_bold
from text_attributes.italic_handling import apply_italic
from text_attributes.underline_handling import apply_underline

class PDFWriter:
    def __init__(self, input_path):
        self.doc = fitz.open(input_path)
        
    def apply_text_changes(self, changes):
        """Apply text changes to PDF"""
        for change in changes:
            page = self.doc[change['page']]
            text = change['text']
            if change.get('bold'):
                text = apply_bold(text, True)
            if change.get('italic'):
                text = apply_italic(text, True)
            if change.get('underline'):
                text = apply_underline(text, True)
                
            # Update text in PDF
            page.add_redact_annot(
                change['bbox'],
                text=text,
                fontname=change.get('font', 'Times-Roman')
            )
            page.apply_redactions()
            
    def save(self, output_path):
        """Save modified PDF"""
        self.doc.save(output_path)
        self.doc.close()
