from PyQt5.QtWidgets import QDockWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class Sidebar(QDockWidget):
    def __init__(self, window):
        super().__init__("Sidebar", window)
        self.window = window
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.setWidget(self.tree)
        self.hide()

    def show_bookmarks(self):
        self.tree.clear()
        root = QTreeWidgetItem(self.tree, ["Bookmarks"])
        for title, url in self.window.bookmark_manager.get_all():
            item = QTreeWidgetItem(root, [title])
            item.setData(0, Qt.UserRole, url)
        root.setExpanded(True)

    def show_history(self):
        self.tree.clear()
        root = QTreeWidgetItem(self.tree, ["History"])
        for url, title in self.window.history_manager.get_recent(50):
            display = title if title else url
            item = QTreeWidgetItem(root, [display])
            item.setData(0, Qt.UserRole, url)
        root.setExpanded(True)

    def _on_item_double_clicked(self, item, column):
        url = item.data(0, Qt.UserRole)
        if url:
            self.window.current_tab().navigate(url)