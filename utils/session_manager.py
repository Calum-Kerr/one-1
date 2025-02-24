import os
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self, base_dir='temp'):
        self.base_dir = base_dir
        self.sessions = {}
        
    def create_session(self, pdf_path):
        """Create new editing session"""
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.sessions[session_id] = {
            'path': pdf_path,
            'created': datetime.now(),
            'modified': datetime.now()
        }
        return session_id
        
    def cleanup_old_sessions(self, max_age_hours=24):
        """Remove sessions older than max_age_hours"""
        now = datetime.now()
        expired = [
            sid for sid, data in self.sessions.items()
            if now - data['modified'] > timedelta(hours=max_age_hours)
        ]
        for sid in expired:
            self.delete_session(sid)
            
    def delete_session(self, session_id):
        """Delete session and associated files"""
        if session_id in self.sessions:
            try:
                os.remove(self.sessions[session_id]['path'])
            except OSError:
                pass
            del self.sessions[session_id]
