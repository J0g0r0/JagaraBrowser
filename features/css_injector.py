from PyQt5.QtWebEngineWidgets import QWebEngineScript
from database.db_manager import DatabaseManager

class CSSInjector:
    @staticmethod
    def add_rule(domain: str, css: str):
        DatabaseManager._connection.execute(
            "INSERT OR REPLACE INTO custom_css (domain, css) VALUES (?, ?)",
            (domain, css)
        )
        DatabaseManager._connection.commit()

    @staticmethod
    def get_rules():
        cur = DatabaseManager._connection.execute("SELECT domain, css FROM custom_css")
        return cur.fetchall()

    @staticmethod
    def apply_to_profile(profile):
        # Untuk setiap halaman yang dimuat, kita periksa domain dan inject CSS
        # Kita gunakan interceptor atau script injector global.
        # Untuk sederhana, kita bisa gunakan QWebEngineUrlRequestInterceptor? Lebih baik via script.
        pass