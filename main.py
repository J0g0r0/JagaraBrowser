#!/usr/bin/env python3
import sys, os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QDir, QStandardPaths
from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineScript, QWebEngineSettings
from browser.window import BrowserWindow
from database.db_manager import DatabaseManager

def configure_profile():
    profile = QWebEngineProfile.defaultProfile()
    
    # 1. User agent agar tidak dicurigai
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
    profile.setHttpUserAgent(user_agent)
    profile.setHttpAcceptLanguage("en-US,en;q=0.9,id;q=0.8")
    
    # 2. Cache & performance
    data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    cache_path = os.path.join(data_dir, "JagaraBrowser", "cache")
    os.makedirs(cache_path, exist_ok=True)
    profile.setCachePath(cache_path)
    profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
    
    settings = profile.settings()
    settings.setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
    settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
    settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
    settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
    settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
    settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
    settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, False)
    settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, False)
    settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)  # agar copy/paste jalan
    settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
    settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
    settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, False)
    settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
    settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
    settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)

    
    # 3. Minimal anti-detection
    script = QWebEngineScript()
    script.setName("remove-webdriver")
    script.setSourceCode("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    script.setInjectionPoint(QWebEngineScript.DocumentCreation)
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setRunsOnSubFrames(True)
    profile.scripts().insert(script)

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("JagaraBrowser")
    app.setOrganizationName("JagaraTech")
    
    # Database
    db_path = os.path.join(QDir.homePath(), ".jagarabrowser", "data.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    DatabaseManager.initialize(db_path)
    
    # Profile
    configure_profile()
    
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()