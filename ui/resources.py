"""
Load icons using Qt's built-in standard pixmaps (no external files needed).
"""
from PyQt5.QtWidgets import QStyle, QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

def get_icon(name):
    """Return a QIcon for the given logical name using QStyle or simple drawing."""
    style = QApplication.style()
    # Map logical names to QStyle standard pixmaps
    mapping = {
        "back": QStyle.SP_ArrowBack,
        "forward": QStyle.SP_ArrowForward,
        "refresh": QStyle.SP_BrowserReload,
        "home": QStyle.SP_DirHomeIcon,
        "download": QStyle.SP_ArrowDown,
        "settings": QStyle.SP_FileDialogDetailedView,
        "bookmark": QStyle.SP_FileDialogListView,
        "bookmarks": QStyle.SP_FileDialogListView,
        "star": QStyle.SP_FileDialogListView,
        "star-filled": QStyle.SP_DialogApplyButton,   # centang sebagai pengganti bintang penuh
        "lock": QStyle.SP_MessageBoxWarning,
        "lock_secure": QStyle.SP_MessageBoxInformation,
        "tab-new": QStyle.SP_FileIcon,
        "menu": QStyle.SP_TitleBarMenuButton,
        "incognito": QStyle.SP_MessageBoxQuestion,
        "shortcut": QStyle.SP_FileLinkIcon,
        "history": QStyle.SP_FileDialogBack,
        "theme": QStyle.SP_ComputerIcon,
    }
    if name in mapping:
        return style.standardIcon(mapping[name])
    # Fallback: draw a simple colored square with the first letter
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor("#1976d2"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(2, 2, 28, 28, 6, 6)
    painter.setPen(Qt.white)
    font = painter.font()
    font.setBold(True)
    font.setPixelSize(18)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, name[0].upper())
    painter.end()
    return QIcon(pixmap)

def load_stylesheet(theme):
    """Return QSS for dark/light theme (embedded)."""
    if theme == "dark":
        return """
        QMainWindow { background-color: #1a1a2e; color: #e0e0e0; }
        QToolBar { background: #16213e; border: none; spacing: 5px; }
        QTabWidget::pane { border: none; }
        QTabBar::tab { background: #0f3460; color: white; padding: 8px 16px; border-radius: 8px; margin: 2px; }
        QTabBar::tab:selected { background: #e94560; }
        QLineEdit { background: #16213e; color: white; border: 2px solid #0f3460; border-radius: 12px; padding: 6px; }
        """
    else:
        return """
        QMainWindow { background-color: #f5f5f5; color: #333; }
        QToolBar { background: #ffffff; border: none; spacing: 5px; }
        QTabBar::tab { background: #e0e0e0; color: black; padding: 8px 16px; border-radius: 8px; }
        QTabBar::tab:selected { background: #1976d2; color: white; }
        QLineEdit { background: white; border: 2px solid #e0e0e0; border-radius: 12px; padding: 6px; }
        """