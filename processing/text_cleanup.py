import re
import html
from typing import Dict, List, Optional
from unicodedata import normalize

class TextCleanup:
    # Common character replacements
    REPLACEMENTS: Dict[str, str] = {
        '—': '-',  # Em dash
        '–': '-',  # En dash
        ''': "'",  # Smart quotes
        ''': "'",
        '"': '"',
        '"': '"',
        '…': '...',
        '\u200b': '',  # Zero-width space
        '\ufeff': '',  # BOM
        '\xa0': ' ',  # Non-breaking space
    }

    @staticmethod
    def remove_control_chars(text: str) -> str:
        """Remove non-printable characters while preserving newlines"""
        return ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')

    @staticmethod
    def normalize_whitespace(text: str, preserve_paragraphs: bool = True) -> str:
        """Normalize whitespace while optionally preserving paragraph breaks"""
        if preserve_paragraphs:
            # Preserve double newlines for paragraphs
            paragraphs = text.split('\n\n')
            cleaned_paragraphs = [' '.join(p.split()) for p in paragraphs]
            return '\n\n'.join(cleaned_paragraphs)
        return ' '.join(text.split())

    @staticmethod
    def decode_html_entities(text: str) -> str:
        """Convert HTML entities to their corresponding characters"""
        return html.unescape(text)

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """Normalize Unicode characters to their canonical form"""
        return normalize('NFKC', text)

    @staticmethod
    def fix_common_issues(text: str) -> str:
        """Fix common text extraction issues"""
        for old, new in TextCleanup.REPLACEMENTS.items():
            text = text.replace(old, new)
        
        # Fix common OCR mistakes
        text = re.sub(r'l1', 'll', text)  # lowercase L + 1 to double L
        text = re.sub(r'0O', 'OO', text)  # zero + O to double O
        text = re.sub(r'rn', 'm', text)   # r + n to m
        
        # Fix multiple periods
        text = re.sub(r'\.{4,}', '...', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'(\d)\s+%', r'\1%', text)
        
        return text

    @staticmethod
    def validate_text(text: str) -> Optional[str]:
        """Validate text before cleaning"""
        if not isinstance(text, str):
            return None
        if not text.strip():
            return None
        return text

    @classmethod
    def clean_text(cls, text: str, preserve_paragraphs: bool = True) -> str:
        """Apply all cleanup operations in the correct order"""
        cleaned = cls.validate_text(text)
        if cleaned is None:
            return ''
            
        cleaned = cls.remove_control_chars(cleaned)
        cleaned = cls.decode_html_entities(cleaned)
        cleaned = cls.normalize_unicode(cleaned)
        cleaned = cls.fix_common_issues(cleaned)
        cleaned = cls.normalize_whitespace(cleaned, preserve_paragraphs)
        
        return cleaned.strip()

    @staticmethod
    def extract_paragraphs(text: str) -> List[str]:
        """Extract properly formatted paragraphs from text"""
        # Split on double newlines and filter out empty paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text)]
        return [p for p in paragraphs if p]
