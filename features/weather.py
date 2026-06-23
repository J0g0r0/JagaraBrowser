import requests
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer

class WeatherWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Loading weather...")
        self.setStyleSheet("color: white; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.fetch_weather)
        self.timer.start(600000)  # setiap 10 menit
        self.fetch_weather()

    def fetch_weather(self):
        try:
            # Gunakan wttr.in (gratis, tanpa API key)
            resp = requests.get("https://wttr.in/Jakarta?format=%C+%t", timeout=3)
            if resp.status_code == 200:
                self.setText(resp.text.strip())
        except:
            self.setText("Weather unavailable")