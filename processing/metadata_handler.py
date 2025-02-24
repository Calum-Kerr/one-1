from datetime import datetime
from typing import Dict, Optional

class MetadataHandler:
    def __init__(self, doc):
        self.doc = doc
        
    def get_metadata(self) -> Dict[str, str]:
        """Extract PDF metadata"""
        metadata = self.doc.metadata
        if metadata is None:
            return {}
            
        return {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'keywords': metadata.get('keywords', ''),
            'creator': metadata.get('creator', ''),
            'producer': metadata.get('producer', ''),
            'creation_date': self._format_date(metadata.get('creationDate')),
            'modification_date': self._format_date(metadata.get('modDate'))
        }
        
    def update_metadata(self, updates: Dict[str, str]) -> bool:
        """Update PDF metadata"""
        try:
            current = dict(self.doc.metadata)
            current.update(updates)
            current['modDate'] = self._get_current_date()
            self.doc.set_metadata(current)
            return True
        except Exception:
            return False
            
    def _format_date(self, date_str: Optional[str]) -> str:
        """Format PDF date string to ISO format"""
        if not date_str:
            return ''
        try:
            # Handle PDF date format: D:YYYYMMDDHHmmSS
            if date_str.startswith('D:'):
                date_str = date_str[2:]
            return datetime.strptime(date_str[:14], '%Y%m%d%H%M%S').isoformat()
        except ValueError:
            return date_str
            
    def _get_current_date(self) -> str:
        """Get current date in PDF format"""
        return f"D:{datetime.now().strftime('%Y%m%d%H%M%S')}"
