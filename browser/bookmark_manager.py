"""
Bookmark management with SQLite backend.
"""
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from database.db_manager import DatabaseManager

class BookmarkManager:
    """Manages bookmarks: add, remove, check existence."""
    
    def __init__(self):
        self.model = BookmarkListModel(self)
    
    def add_bookmark(self, title, url):
        DatabaseManager.add_bookmark(title, url)
        self.model.refresh()
    
    def remove_bookmark(self, url):
        DatabaseManager.remove_bookmark(url)
        self.model.refresh()
    
    def is_bookmarked(self, url):
        return DatabaseManager.is_bookmarked(url)
    
    def get_all(self):
        return DatabaseManager.get_all_bookmarks()

class BookmarkListModel(QAbstractListModel):
    """Model for displaying bookmarks in a list/tree."""
    
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.bookmarks = []
        self.refresh()
    
    def refresh(self):
        self.beginResetModel()
        self.bookmarks = self.manager.get_all()
        self.endResetModel()
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        if role == Qt.DisplayRole:
            return self.bookmarks[row][0]  # title
        elif role == Qt.UserRole:
            return self.bookmarks[row][1]  # url
        return None
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.bookmarks)