"""Inject custom JavaScript/CSS into pages."""
from PyQt5.QtWebEngineWidgets import QWebEngineScript

def inject_script(profile, name, source, world=QWebEngineScript.MainWorld):
    script = QWebEngineScript()
    script.setName(name)
    script.setSourceCode(source)
    script.setInjectionPoint(QWebEngineScript.DocumentReady)
    script.setWorldId(world)
    script.setRunsOnSubFrames(False)
    profile.scripts().insert(script)