import feedparser
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLineEdit, QTextBrowser
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class RSSWorker(QThread):
    finished = pyqtSignal(list)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        feed = feedparser.parse(self.url)
        entries = [(e.title, e.link) for e in feed.entries]
        self.finished.emit(entries)

class RSSDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RSS Reader")
        self.resize(600, 400)
        layout = QVBoxLayout(self)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter RSS feed URL...")
        layout.addWidget(self.url_input)

        self.load_btn = QPushButton("Load Feed")
        self.load_btn.clicked.connect(self.load_feed)
        layout.addWidget(self.load_btn)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.open_entry)
        layout.addWidget(self.list_widget)

    def load_feed(self):
        url = self.url_input.text().strip()
        if url:
            self.worker = RSSWorker(url)
            self.worker.finished.connect(self.populate_list)
            self.worker.start()

    def populate_list(self, entries):
        self.list_widget.clear()
        for title, link in entries:
            self.list_widget.addItem(f"{title}")

    def open_entry(self, item):
        # Buka di tab baru browser utama
        pass  # butuh reference ke BrowserWindow, bisa via parent