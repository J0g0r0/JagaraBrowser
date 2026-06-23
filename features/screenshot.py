"""
Capture full page screenshot.
"""
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer

def take_screenshot(tab):
    """Capture visible part of web page."""
    pixmap = tab.web_view.grab()
    path, _ = QFileDialog.getSaveFileName(None, "Save Screenshot", "", "PNG (*.png)")
    if path:
        pixmap.save(path)