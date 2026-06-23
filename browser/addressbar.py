"""
Smart address bar with search engine integration, security indicators,
autocomplete, loading spinner, favicon, thin progress bar, and right‑click menu.
"""
from PyQt5.QtWidgets import (
    QLineEdit, QProgressBar, QWidget, QVBoxLayout,
    QCompleter, QAction, QMenu
)
from PyQt5.QtCore import Qt, QUrl, QStringListModel
from PyQt5.QtGui import QIcon
from ui.resources import get_icon

class AddressBarWidget(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.line_edit = AddressLineEdit(window)
        layout.addWidget(self.line_edit)

        self.progress = QProgressBar()
        self.progress.setMaximumHeight(3)
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.hide()
        layout.addWidget(self.progress)

    def update_for_tab(self, tab):
        self.line_edit.update_for_tab(tab)
        if tab and tab.is_loading():
            self.progress.show()
            self.progress.setValue(tab.load_progress())
        else:
            self.progress.hide()

    def setFocus(self):
        self.line_edit.setFocus()


class AddressLineEdit(QLineEdit):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setPlaceholderText("Search or enter URL")
        self.returnPressed.connect(self._on_enter)

        # Autocomplete
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setMaxVisibleItems(10)
        self.setCompleter(self.completer)

        # Leading actions
        self.security_action = self.addAction(get_icon("lock"), QLineEdit.LeadingPosition)
        self.loading_action = self.addAction(get_icon("refresh"), QLineEdit.LeadingPosition)
        self.loading_action.setVisible(False)

        # Trailing bookmark star
        self.bookmark_action = self.addAction(get_icon("star"), QLineEdit.TrailingPosition)
        self.bookmark_action.triggered.connect(self.window.bookmark_current_page)

    def update_for_tab(self, tab):
        if not tab:
            return
        url = tab.url()
        self.setText(url.toString())

        if url.scheme() == "https":
            self.security_action.setIcon(get_icon("lock_secure"))
        else:
            self.security_action.setIcon(get_icon("lock"))
        icon = tab.icon()
        if icon and not icon.isNull():
            self.security_action.setIcon(icon)

        self.loading_action.setVisible(tab.is_loading())

        if self.window.bookmark_manager.is_bookmarked(url.toString()):
            self.bookmark_action.setIcon(get_icon("star-filled"))
        else:
            self.bookmark_action.setIcon(get_icon("star"))

        self._update_completer()

    def contextMenuEvent(self, event):
        """Custom right‑click menu with Paste & Go, etc."""
        menu = self.createStandardContextMenu()
        # Tambahkan aksi kustom di atas menu standar
        menu.addSeparator()
        menu.addAction("Paste && Go", self._paste_and_go)
        menu.addAction("Paste && Search", self._paste_and_search)
        menu.exec_(event.globalPos())

    def _paste_and_go(self):
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            self.setText(text)
            self._on_enter()

    def _paste_and_search(self):
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            self.setText(text)
            # force search even if URL-like
            self.window.current_tab().navigate("https://www.google.com/search?q=" + text.replace(" ", "+"))

    def _on_enter(self):
        text = self.text().strip()
        if not text:
            return
        if self._is_url(text):
            url = QUrl(text)
            if url.scheme() == "":
                url.setScheme("http")
        else:
            url = QUrl("https://www.google.com/search?q=" + text.replace(" ", "+"))
        self.window.current_tab().navigate(url)

    def _is_url(self, text):
        return "." in text and " " not in text

    def _update_completer(self):
        suggestions = set()
        for bm in self.window.bookmark_manager.get_all():
            suggestions.add(bm[1])
        for hist in self.window.history_manager.get_recent(50):
            suggestions.add(hist[1])
        model = QStringListModel(sorted(suggestions)[:20])
        self.completer.setModel(model)