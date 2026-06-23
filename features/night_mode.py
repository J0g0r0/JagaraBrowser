from PyQt5.QtWebEngineWidgets import QWebEngineScript

def inject_night_mode(profile):
    script = QWebEngineScript()
    script.setName("nightmode")
    script.setSourceCode("""
        (function() {
            const style = document.createElement('style');
            style.id = 'jagara-night-mode';
            style.textContent = 'html { filter: invert(1) hue-rotate(180deg) !important; background: #111 !important; } img, video, canvas { filter: invert(1) hue-rotate(180deg) !important; }';
            document.head.appendChild(style);
        })();
    """)
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setWorldId(QWebEngineScript.MainWorld)
    script.setRunsOnSubFrames(False)
    profile.scripts().insert(script)