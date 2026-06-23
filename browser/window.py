"""
JagaraBrowser - Main Window with all premium features.
"""
import os, sys
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QToolBar, QAction, QLineEdit,
    QVBoxLayout, QWidget, QSplitter, QTreeView, QDockWidget,
    QMenu, QMessageBox, QFileDialog, QShortcut, QLabel,
    QListWidget, QProgressBar, QPushButton, QInputDialog,
    QStyle
)
from PyQt5.QtCore import Qt, QUrl, QFileInfo, QStandardPaths, QTimer
from PyQt5.QtGui import QIcon, QKeySequence, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineSettings, QWebEngineDownloadItem
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from browser.tab import WebTab
from browser.addressbar import AddressBarWidget
from browser.bookmark_manager import BookmarkManager
from browser.history_manager import HistoryManager
from browser.settings_dialog import SettingsDialog
from browser.sidebar import Sidebar
from browser.newtab import NewTabPage
from core.session_manager import SessionManager
from core.download_manager import DownloadManager, DownloadWidget
from core.optimizer import MemoryOptimizer
from core.gestures import GestureRecognizer
from core.password_manager import PasswordVault
from features.reading_mode import ReaderDialog
from features.fullpage_screenshot import capture_full_page
from features.translator import translate_page
from features.night_mode import inject_night_mode
from features.pip import PiPWindow
from ui.resources import get_icon, load_stylesheet
from ui.shortcut_dialog import ShortcutDialog
from database.db_manager import DatabaseManager

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JagaraBrowser")
        self.resize(1280, 800)

        # Managers
        self.bookmark_manager = BookmarkManager()
        self.history_manager = HistoryManager()
        self.session_manager = SessionManager()
        self.current_theme = "dark"
        self._closed_tabs = []  # stack (url, title, icon) untuk restore

        # Start download manager singleton
        DownloadManager.instance()

        self._init_ui()
        self._create_actions()
        self._create_toolbars()
        self._setup_shortcuts()
        self._apply_theme()
        self._init_features()

        if not self.session_manager.restore_session(self):
            self.add_new_tab()

    def _init_ui(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab_widget.customContextMenuRequested.connect(self.show_tab_context_menu)
        self.setCentralWidget(self.tab_widget)

        self.sidebar = Sidebar(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sidebar)
        self.sidebar.hide()

    def show_password_manager(self):
        from PyQt5.QtWidgets import QInputDialog
        master, ok = QInputDialog.getText(self, "Master Password", "Enter master password:", QLineEdit.Password)
        if ok and master:
            vault = PasswordVault(master)
        # Tampilkan daftar situs yang tersimpan
            sites = vault.get_all_sites()
            if not sites:
                QMessageBox.information(self, "Password Manager", "No passwords stored yet.")
                return
        # Pilih situs untuk melihat password
            site, ok2 = QInputDialog.getItem(self, "Select Site", "Site:", sites, 0, False)
            if ok2:
                user, pw = vault.get_password(site)
                QMessageBox.information(self, f"Credentials for {site}", f"Username: {user}\nPassword: {pw}")   

    def _create_actions(self):
        """Create all QActions for menus and toolbars."""
        self.new_tab_action = QAction(get_icon("tab-new"), "New Tab", self)
        self.new_tab_action.triggered.connect(lambda: self.add_new_tab())

        self.new_window_action = QAction(get_icon("window-new"), "New Window", self)
        self.new_window_action.triggered.connect(self.open_new_window)

        self.view_source_action = QAction(get_icon("shortcut"), "View Page Source", self)
        self.view_source_action.triggered.connect(self.view_page_source)

        self.inspect_action = QAction(get_icon("shortcut"), "Inspect Element", self)
        self.inspect_action.triggered.connect(self.inspect_element)

        self.copy_action = QAction("Copy", self)
        self.copy_action.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Copy).trigger())
        
        self.paste_action = QAction("Paste", self)
        self.paste_action.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Paste).trigger())
       
        self.cut_action = QAction("Cut", self)
        self.cut_action.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Cut).trigger())
       
        self.find_action = QAction(get_icon("shortcut"), "Find in Page", self)
        self.find_action.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Find).trigger())
        self.find_action.setShortcut(QKeySequence("Ctrl+F"))

        self.new_incognito_action = QAction(get_icon("incognito"), "New Incognito Window", self)
        self.new_incognito_action.triggered.connect(self.open_incognito_window)

        self.bookmark_page_action = QAction(get_icon("bookmark"), "Bookmark This Page", self)
        self.bookmark_page_action.triggered.connect(self.bookmark_current_page)

        self.show_bookmarks_action = QAction(get_icon("bookmarks"), "Show All Bookmarks", self)
        self.show_bookmarks_action.triggered.connect(self.show_bookmarks_sidebar)

        self.show_history_action = QAction(get_icon("history"), "History", self)
        self.show_history_action.triggered.connect(self.show_history_sidebar)

        self.show_downloads_action = QAction(get_icon("download"), "Downloads", self)
        self.show_downloads_action.triggered.connect(self.show_downloads)

        self.reading_mode_action = QAction(get_icon("shortcut"), "Reading Mode", self)
        self.reading_mode_action.triggered.connect(self.open_reading_mode)

        self.screenshot_action = QAction(get_icon("lock_secure"), "Save Full Page PDF", self)
        self.screenshot_action.triggered.connect(self.save_page_pdf)

        self.translate_action = QAction(get_icon("shortcut"), "Translate Page", self)
        self.translate_action.triggered.connect(lambda: translate_page(self.current_tab()))

        self.pip_action = QAction(get_icon("shortcut"), "Picture-in-Picture", self)
        self.pip_action.triggered.connect(self.open_pip)

        self.night_mode_action = QAction(get_icon("theme"), "Toggle Night Mode", self)
        self.night_mode_action.triggered.connect(self.toggle_night_mode)

        self.toggle_theme_action = QAction(get_icon("theme"), "Toggle Theme", self)
        self.toggle_theme_action.triggered.connect(self.toggle_theme)

        self.settings_action = QAction(get_icon("settings"), "Settings", self)
        self.settings_action.triggered.connect(self.show_settings)

        self.shortcut_help_action = QAction(get_icon("menu"), "Keyboard Shortcuts", self)
        self.shortcut_help_action.triggered.connect(lambda: ShortcutDialog(self).exec_())

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)

        self.find_action = QAction(get_icon("shortcut"), "Find in Page", self)
        self.find_action.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Find).trigger())
        self.find_action.setShortcut(QKeySequence("Ctrl+F"))

    def _create_toolbars(self):
        nav_toolbar = QToolBar("Navigation")
        nav_toolbar.setMovable(False)
        self.addToolBar(nav_toolbar)

        self.back_btn = QAction(get_icon("back"), "Back", self)
        self.back_btn.triggered.connect(lambda: self.current_tab().back() if self.current_tab() else None)
        nav_toolbar.addAction(self.back_btn)

        self.forward_btn = QAction(get_icon("forward"), "Forward", self)
        self.forward_btn.triggered.connect(lambda: self.current_tab().forward() if self.current_tab() else None)
        nav_toolbar.addAction(self.forward_btn)

        self.refresh_btn = QAction(get_icon("refresh"), "Refresh", self)
        self.refresh_btn.triggered.connect(lambda: self.current_tab().reload() if self.current_tab() else None)
        nav_toolbar.addAction(self.refresh_btn)

        self.home_btn = QAction(get_icon("home"), "Home", self)
        self.home_btn.triggered.connect(lambda: self.current_tab().navigate_to_home() if self.current_tab() else None)
        nav_toolbar.addAction(self.home_btn)

        self.address_bar = AddressBarWidget(self)   # <-- PERBAIKAN
        nav_toolbar.addWidget(self.address_bar)

        self.menu_btn = QAction(get_icon("menu"), "Menu", self)
        self.menu_btn.setMenu(self._build_main_menu())
        nav_toolbar.addAction(self.menu_btn)

    def _build_main_menu(self):
        menu = QMenu()
        menu.addAction(self.new_tab_action)
        menu.addAction(self.new_window_action)
        menu.addAction(self.new_incognito_action)
        menu.addSeparator()
        menu.addAction(self.bookmark_page_action)
        menu.addAction(self.show_bookmarks_action)
        menu.addAction(self.show_history_action)
        menu.addAction(self.show_downloads_action)
        menu.addSeparator()
        menu.addAction(self.reading_mode_action)
        menu.addAction(self.screenshot_action)
        menu.addAction(self.translate_action)
        menu.addAction(self.pip_action)
        menu.addSeparator()
        menu.addAction(self.night_mode_action)
        menu.addAction(self.toggle_theme_action)
        menu.addSeparator()

    # ---------- Edit menu ----------
        edit_menu = menu.addMenu("Edit")

        copy_act = QAction("Copy", self)
        copy_act.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Copy).trigger() if self.current_tab() else None)
        copy_act.setShortcut(QKeySequence("Ctrl+C"))
        edit_menu.addAction(copy_act)

        paste_act = QAction("Paste", self)
        paste_act.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Paste).trigger() if self.current_tab() else None)
        paste_act.setShortcut(QKeySequence("Ctrl+V"))
        edit_menu.addAction(paste_act)

        cut_act = QAction("Cut", self)
        cut_act.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Cut).trigger() if self.current_tab() else None)
        cut_act.setShortcut(QKeySequence("Ctrl+X"))
        edit_menu.addAction(cut_act)

        edit_menu.addSeparator()

        find_act = QAction("Find...", self)
        find_act.triggered.connect(lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Find).trigger() if self.current_tab() else None)
        find_act.setShortcut(QKeySequence("Ctrl+F"))
        edit_menu.addAction(find_act)

        menu.addSeparator()
        menu.addAction(self.settings_action)
        menu.addAction(self.shortcut_help_action)
        menu.addSeparator()
        menu.addAction(self.exit_action)

        return menu

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+T"), self, lambda: self.add_new_tab())
        QShortcut(QKeySequence("Ctrl+W"), self, lambda: self.close_tab(self.tab_widget.currentIndex()))
        QShortcut(QKeySequence("Ctrl+Shift+T"), self, self.reopen_closed_tab)
        QShortcut(QKeySequence("Ctrl+L"), self, lambda: self.address_bar.setFocus())
        QShortcut(QKeySequence("Ctrl+D"), self, lambda: self.bookmark_current_page())
        QShortcut(QKeySequence("Ctrl+H"), self, lambda: self.show_history_sidebar())
        QShortcut(QKeySequence("Ctrl+J"), self, lambda: self.show_downloads())
        QShortcut(QKeySequence("F11"), self, self.toggle_fullscreen)
        QShortcut(QKeySequence("Ctrl+R"), self, lambda: self.current_tab().reload())
        QShortcut(QKeySequence("F5"), self, lambda: self.current_tab().reload())
        QShortcut(QKeySequence("Ctrl+0"), self, lambda: self.current_tab().web_view.setZoomFactor(1))
        QShortcut(QKeySequence("Ctrl+="), self, lambda: self.zoom_in())
        QShortcut(QKeySequence("Ctrl+-"), self, lambda: self.zoom_out())
        QShortcut(QKeySequence("Ctrl+Tab"), self, self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self, self.prev_tab)
        QShortcut(QKeySequence("Ctrl+M"), self, self.mute_current_tab)
        QShortcut(QKeySequence("Ctrl+Shift+P"), self, self.open_reading_mode)
        QShortcut(QKeySequence("Ctrl+F"), self, lambda: self.current_tab().web_view.page().findText(""))
        QShortcut(QKeySequence("Escape"), self, lambda: self.current_tab().stop())
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_page_pdf)
        QShortcut(QKeySequence("Ctrl+?"), self, lambda: ShortcutDialog(self).exec_())
        QShortcut(QKeySequence("Ctrl+U"), self, self.view_page_source)
        QShortcut(QKeySequence("Ctrl+Shift+I"), self, self.inspect_element)
# Shortcut copy/paste/cut biasanya sudah ada di QWebEngineView, tapi kita tambahkan agar selalu tersedia
        QShortcut(QKeySequence("Ctrl+C"), self, lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Copy).trigger())
        QShortcut(QKeySequence("Ctrl+V"), self, lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Paste).trigger())
        QShortcut(QKeySequence("Ctrl+X"), self, lambda: self.current_tab().web_view.pageAction(QWebEnginePage.Cut).trigger())
        QShortcut(QKeySequence("Ctrl+A"), self, lambda: self.current_tab().web_view.pageAction(QWebEnginePage.SelectAll).trigger())

    def _init_features(self):
        # Memory optimizer
        self.optimizer = MemoryOptimizer(self)
        # Mouse gestures (right click drag)
        self.gesture = GestureRecognizer(self)
        # Night mode ready (not applied by default)
        self.night_mode_enabled = False

    def add_new_tab(self, url=None, background=False):
        tab = WebTab(self)
        index = self.tab_widget.addTab(tab, "New Tab")
        if not background:
            self.tab_widget.setCurrentIndex(index)
        # Signals
        tab.web_view.loadStarted.connect(lambda t=tab: self.address_bar.update_for_tab(t))
        tab.web_view.loadProgress.connect(lambda p, t=tab: self.address_bar.update_for_tab(t))
        tab.web_view.loadFinished.connect(lambda ok, t=tab: self.address_bar.update_for_tab(t))
        tab.titleChanged.connect(lambda title, t=tab: self.update_tab_title(t, title))
        tab.iconChanged.connect(lambda icon, t=tab: self.update_tab_icon(t, icon))
        tab.urlChanged.connect(lambda url, t=tab: self.on_url_changed(t, url))
        if url:
            tab.navigate(url)
        else:
            tab.set_new_tab_page()
        return tab

    def current_tab(self):
        return self.tab_widget.currentWidget() if self.tab_widget.count() else None

    def close_tab(self, index):
        if self.tab_widget.count() <= 1:
            self.add_new_tab()  # hindari jendela kosong
        widget = self.tab_widget.widget(index)
        if widget:
            # Simpan info untuk restore
            self._closed_tabs.append({
                'url': widget.url().toString(),
                'title': widget.title(),
                'icon': widget.icon()
            })
            self.tab_widget.removeTab(index)
            widget.deleteLater()

    def reopen_closed_tab(self):
        if self._closed_tabs:
            info = self._closed_tabs.pop()
            tab = self.add_new_tab(info['url'])
            if info['title']:
                tab.titleChanged.emit(info['title'])
            if info['icon'] and not info['icon'].isNull():
                tab.iconChanged.emit(info['icon'])

    def on_tab_changed(self, index):
        tab = self.current_tab()
        if tab:
            self.address_bar.update_for_tab(tab)
            self.update_navigation_buttons()

    def update_tab_title(self, tab, title):
        index = self.tab_widget.indexOf(tab)
        if index != -1:
            self.tab_widget.setTabText(index, title[:30])

    def update_tab_icon(self, tab, icon):
        index = self.tab_widget.indexOf(tab)
        if index != -1:
            self.tab_widget.setTabIcon(index, icon)

    def view_page_source(self):
        tab = self.current_tab()
        if tab:
            tab.view_source()
   
    def inspect_element(self):
        tab = self.current_tab()
        if tab:
            tab.inspect_element()        

    def on_url_changed(self, tab, url):
        if tab == self.current_tab():
            self.address_bar.update_for_tab(tab)
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        tab = self.current_tab()
        if tab:
            self.back_btn.setEnabled(tab.web_view.history().canGoBack())
            self.forward_btn.setEnabled(tab.web_view.history().canGoForward())

    def bookmark_current_page(self):
        tab = self.current_tab()
        if tab:
            self.bookmark_manager.add_bookmark(tab.title(), tab.url().toString())
            QMessageBox.information(self, "Bookmarked", "Page bookmarked.")

    def show_bookmarks_sidebar(self):
        self.sidebar.show_bookmarks()
        self.sidebar.show()

    def show_history_sidebar(self):
        self.sidebar.show_history()
        self.sidebar.show()

    def show_downloads(self):
        self.download_widget = DownloadWidget()
        self.download_widget.show()

    def open_reading_mode(self):
        tab = self.current_tab()
        if tab:
            ReaderDialog(tab.url().toString(), self).show()

    def save_page_pdf(self):
        tab = self.current_tab()
        if tab:
            path, _ = QFileDialog.getSaveFileName(self, "Save Page as PDF", "", "PDF (*.pdf)")
            if path:
                capture_full_page(tab, path)

    def toggle_night_mode(self):
        profile = QWebEngineProfile.defaultProfile()
        if not self.night_mode_enabled:
            inject_night_mode(profile)
            self.night_mode_enabled = True
            # Reload tabs? Tidak perlu, hanya halaman baru yang terpengaruh.
            QMessageBox.information(self, "Night Mode", "Night mode enabled for new pages. Reload to apply to current.")
        else:
            # Sulit untuk dihapus, sebaiknya gunakan toggle local di tab dengan message.
            pass

    def open_pip(self):
        tab = self.current_tab()
        if tab:
            # Coba ekstrak URL video pertama via JavaScript
            js = "document.querySelector('video').src || document.querySelector('video').currentSrc || ''"
            tab.web_view.page().runJavaScript(js, lambda result: self._show_pip_window(result))

    def _show_pip_window(self, video_url):
        if video_url:
            self.pip_win = PiPWindow(video_url)
            self.pip_win.show()
        else:
            QMessageBox.warning(self, "PiP", "No video found on this page.")

    def show_settings(self):
        dlg = SettingsDialog(self)
        if dlg.exec_():
            self._apply_theme()

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme()

    def _apply_theme(self):
        self.setStyleSheet(load_stylesheet(self.current_theme))

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def open_new_window(self):
        BrowserWindow().show()

    def open_incognito_window(self):
        profile = QWebEngineProfile("incognito", self)
        profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        win = BrowserWindow()
        win.setWindowTitle("JagaraBrowser (Incognito)")
        win.show()

    def show_tab_context_menu(self, pos):
        index = self.tab_widget.tabBar().tabAt(pos)
        if index < 0:
            return
        menu = QMenu()
        menu.addAction("Reload", lambda: self.tab_widget.widget(index).reload())
        menu.addAction("Duplicate", lambda: self.duplicate_tab(index))
        menu.addAction("Mute Tab", lambda: self.tab_widget.widget(index).toggle_mute())
        menu.addAction("Close Tab", lambda: self.close_tab(index))
        menu.exec_(self.tab_widget.tabBar().mapToGlobal(pos))

    def duplicate_tab(self, index):
        tab = self.tab_widget.widget(index)
        self.add_new_tab(tab.url().toString())

    def zoom_in(self):
        tab = self.current_tab()
        if tab:
            z = tab.web_view.zoomFactor() + 0.1
            tab.web_view.setZoomFactor(min(z, 5.0))

    def zoom_out(self):
        tab = self.current_tab()
        if tab:
            z = tab.web_view.zoomFactor() - 0.1
            tab.web_view.setZoomFactor(max(z, 0.25))

    def next_tab(self):
        idx = (self.tab_widget.currentIndex() + 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(idx)

    def prev_tab(self):
        idx = (self.tab_widget.currentIndex() - 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(idx)

    def mute_current_tab(self):
        tab = self.current_tab()
        if tab:
            tab.toggle_mute()

    def closeEvent(self, event):
        self.session_manager.save_session(self)
        event.accept()