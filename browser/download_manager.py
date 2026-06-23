"""
Download manager with pause/resume (simplified).
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QProgressBar, QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem

class DownloadManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Downloads")
        self.resize(400, 300)
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        # Normally you'd connect to profile downloadRequested signal
        # but for demo we just show a placeholder.
    
    def add_download(self, download_item: QWebEngineDownloadItem):
        """Add a download to the list."""
        widget = QWidget()
        vbox = QVBoxLayout(widget)
        label = QLabel(download_item.path())
        progress = QProgressBar()
        vbox.addWidget(label)
        vbox.addWidget(progress)
        self.list_widget.addItem(widget)
        
        download_item.downloadProgress.connect(lambda recv, total: progress.setValue(recv/total*100))
        download_item.finished.connect(lambda: progress.setValue(100))