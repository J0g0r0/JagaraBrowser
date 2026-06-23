"""
Detect video and open in a separate frameless window.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class PiPWindow(QWidget):
    def __init__(self, url):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(400, 300)
        layout = QVBoxLayout(self)
        self.webview = QWebEngineView()
        self.webview.load(QUrl(url))
        layout.addWidget(self.webview)
        # Close button
        close_btn = QPushButton("X")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)