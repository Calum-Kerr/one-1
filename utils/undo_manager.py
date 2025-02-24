class UndoManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.max_stack_size = 50

    def push_change(self, change):
        """Add new change to undo stack"""
        self.undo_stack.append(change)
        self.redo_stack.clear()
        
        if len(self.undo_stack) > self.max_stack_size:
            self.undo_stack.pop(0)

    def undo(self):
        """Revert last change"""
        if not self.undo_stack:
            return None
            
        change = self.undo_stack.pop()
        self.redo_stack.append(change)
        return self.invert_change(change)

    def redo(self):
        """Reapply previously undone change"""
        if not self.redo_stack:
            return None
            
        change = self.redo_stack.pop()
        self.undo_stack.append(change)
        return change

    @staticmethod
    def invert_change(change):
        """Create inverse of a change operation"""
        return {
            'operation': 'revert',
            'original': change,
            'bbox': change['bbox'],
            'page': change['page']
        }
