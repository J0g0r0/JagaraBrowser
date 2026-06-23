"""
Extract main content and display in a clean reader view.
"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import QUrl
from bs4 import BeautifulSoup
import requests

def get_reader_view(url):
    try:
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, 'html.parser')
        # Remove scripts, styles, ads
        for tag in soup(['script', 'style', 'nav', 'footer', 'aside', '.ad', '.sidebar']):
            tag.decompose()
        # Extract article or body
        article = soup.find('article') or soup.find('main') or soup.body
        if article:
            return str(article)
        return "<p>Failed to extract content.</p>"
    except Exception as e:
        return f"<p>Error: {e}</p>"

class ReaderDialog(QDialog):
    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reading Mode")
        self.resize(800, 600)
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        btn = QPushButton("Close")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)
        # Load content in background
        import threading
        def load():
            content = get_reader_view(url)
            self.text_edit.setHtml(content)
        threading.Thread(target=load, daemon=True).start()