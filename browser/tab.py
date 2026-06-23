"""
Individual browser tab containing QWebEngineView and custom New Tab Page.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEnginePage, QWebEngineProfile
)
from PyQt5.QtGui import QIcon
from browser.newtab import NewTabPage
from core.adblocker import AdBlocker

class WebTab(QWidget):
    """Represents a single browser tab with web view."""
    titleChanged = pyqtSignal(str)
    iconChanged = pyqtSignal(QIcon)
    urlChanged = pyqtSignal(QUrl)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Web engine profile
        self.profile = QWebEngineProfile.defaultProfile()
        self.ad_blocker = AdBlocker(self.profile)

        # Web view
        self.web_view = QWebEngineView()
        self.web_page = QWebEnginePage(self.profile, self.web_view)
        self.web_view.setPage(self.web_page)

        # Tracking loading state
        self._loading = False
        self._progress = 0
        self.web_view.loadStarted.connect(self._on_load_started)
        self.web_view.loadProgress.connect(self._on_load_progress)
        self.web_view.loadFinished.connect(self._on_load_finished)

        # Connect title/icon/url signals
        self.web_view.titleChanged.connect(self._on_title_changed)
        self.web_view.iconChanged.connect(self._on_icon_changed)
        self.web_view.urlChanged.connect(self._on_url_changed)

        self.layout.addWidget(self.web_view)

        # Custom new tab page (hidden initially)
        self.new_tab_page = NewTabPage(self)
        self.new_tab_page.hide()
        self.layout.addWidget(self.new_tab_page)

        self._is_new_tab = False

    def navigate(self, url):
        """Load a URL in the web view."""
        if isinstance(url, str):
            url = QUrl(url)
        self.web_view.load(url)
        self._show_web_view()

    def set_new_tab_page(self):
        """Display the custom new tab page."""
        self.web_view.hide()
        self.new_tab_page.show()
        self._is_new_tab = True

    def _show_web_view(self):
        self.web_view.show()
        self.new_tab_page.hide()
        self._is_new_tab = False

    def back(self):
        self.web_view.back()

    def forward(self):
        self.web_view.forward()

    def reload(self):
        self.web_view.reload()

    def stop(self):
        self.web_view.stop()

    def title(self):
        return self.web_view.title()

    def url(self):
        return self.web_view.url()

    def icon(self):
        return self.web_view.icon()

    def toggle_mute(self):
        page = self.web_view.page()
        page.setAudioMuted(not page.isAudioMuted())

    def navigate_to_home(self):
        self.navigate("https://www.google.com")

    def is_loading(self):
        return self._loading

    def load_progress(self):
        return self._progress

    # Internal slots
    def _on_load_started(self):
        self._loading = True
        self._progress = 0

    def _on_load_progress(self, progress):
        self._progress = progress

    def _on_load_finished(self, ok):
        self._loading = False
        self._progress = 100

    def _on_title_changed(self, title):
        self.titleChanged.emit(title)

    def _on_icon_changed(self, icon):
        self.iconChanged.emit(icon)

    def _on_url_changed(self, url):
        self.urlChanged.emit(url)
        from database.db_manager import DatabaseManager
        DatabaseManager.add_history(url.toString(), self.title())

    # ---------- NEW FEATURES ----------
    def view_source(self):
        """Open page source in a new tab."""
        self.web_view.page().toHtml(self._show_source_in_new_tab)

    def _show_source_in_new_tab(self, html):
        # 'self' masih merujuk ke WebTab karena callback di atas
        new_tab = self.parent().add_new_tab(background=False)
        new_tab.web_view.setHtml(html, QUrl(self.url().toString()))

    def inspect_element(self):
        """Open DevTools for this page."""
        page = self.web_view.page()
        # Mengaktifkan DevTools dan membuka inspektor
        page.setDevToolsPage(page.devToolsPage())
        page.triggerAction(QWebEnginePage.InspectElement)