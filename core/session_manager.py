"""
Save and restore browsing sessions (list of open tabs).
"""
import json
import os
from PyQt5.QtCore import QDir

class SessionManager:
    def __init__(self):
        # Tentukan path file sesi di folder data JagaraBrowser
        data_dir = os.path.join(QDir.homePath(), ".jagarabrowser")
        self.session_file = os.path.join(data_dir, "session.json")
        # Pastikan direktori ada
        os.makedirs(data_dir, exist_ok=True)

    def save_session(self, window):
        """Simpan URL semua tab yang terbuka ke file JSON."""
        tabs = []
        for i in range(window.tab_widget.count()):
            tab = window.tab_widget.widget(i)
            if tab and tab.url().isValid():
                tabs.append(tab.url().toString())
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(tabs, f, indent=2)
        except Exception as e:
            print(f"Session save error: {e}")

    def restore_session(self, window):
        """Kembalikan tab dari file sesi, jika ada."""
        if not os.path.exists(self.session_file):
            return False
        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                tabs = json.load(f)
            if not tabs:
                return False
            for url in tabs:
                window.add_new_tab(url, background=True)
            # Hapus tab kosong pertama yang dibuat oleh __init__
            if window.tab_widget.count() > len(tabs):
                window.close_tab(0)
            return True
        except Exception as e:
            print(f"Session restore error: {e}")
            return False