from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEnginePage

def capture_full_page(tab, output_path):
    """Save page as PDF (full page)."""
    tab.web_view.page().printToPdf(output_path)