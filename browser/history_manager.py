"""
History tracking and retrieval.
"""
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from database.db_manager import DatabaseManager
from datetime import datetime

class HistoryManager:
    def __init__(self):
        self.model = HistoryListModel(self)
    
    def add_entry(self, url, title):
        DatabaseManager.add_history(url, title)
        self.model.refresh()
    
    def get_recent(self, limit=100):
        return DatabaseManager.get_recent_history(limit)
    
    def search(self, keyword):
        return DatabaseManager.search_history(keyword)
    
    def clear(self):
        DatabaseManager.clear_history()
        self.model.refresh()

class HistoryListModel(QAbstractListModel):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.entries = []
        self.refresh()
    
    def refresh(self):
        self.beginResetModel()
        self.entries = self.manager.get_recent(200)
        self.endResetModel()
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        if role == Qt.DisplayRole:
            title = self.entries[row][1]
            return title if title else self.entries[row][0]
        elif role == Qt.UserRole:
            return self.entries[row][0]  # url
        return None
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.entries)