"""
Animated new tab page with search bar, shortcuts, weather, and quotes.
"""
import random
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QGridLayout, QLineEdit, QMenu, QInputDialog
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from ui.resources import get_icon
from browser.speeddial_manager import SpeedDialManager


class ParticleBackground(QWidget):
    """Animated particle background with gentle movement."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(30)
        for _ in range(30):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            size = random.randint(2, 6)
            speed = random.uniform(0.2, 1)
            self.particles.append({"x": x, "y": y, "size": size, "speed": speed})

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255, 30))
        painter.setPen(Qt.NoPen)
        for p in self.particles:
            x = int(p["x"] * self.width() / 100)
            y = int(p["y"] * self.height() / 100)
            painter.drawEllipse(x, y, p["size"], p["size"])
            p["y"] = (p["y"] - p["speed"]) % 100


class NewTabPage(QWidget):
    """Custom new tab page with search, speed dial, quotes, and weather."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Particle background
        self.bg = ParticleBackground(self)
        self.bg.lower()

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Google or type a URL")
        self.search_input.setMaximumWidth(600)
        self.search_input.setStyleSheet(
            "padding: 12px; border-radius: 24px; background: rgba(255,255,255,0.2); color: white;"
        )
        self.search_input.returnPressed.connect(self._search)
        self.main_layout.addWidget(self.search_input, alignment=Qt.AlignCenter)

        # Speed dial grid
        self.speed_dial_grid = QGridLayout()
        self.speed_dial_grid.setSpacing(10)
        self.main_layout.addLayout(self.speed_dial_grid)

        # Load speed dial entries
        self._load_speed_dial()

        # Quote label
        quotes = [
            "“The only way to do great work is to love what you do.” – Steve Jobs",
            "“Innovation distinguishes between a leader and a follower.” – Steve Jobs",
            "“Stay hungry, stay foolish.” – Steve Jobs",
        ]
        self.quote_label = QLabel(random.choice(quotes))
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setStyleSheet("color: white; font-style: italic; margin-top: 20px;")
        self.main_layout.addWidget(self.quote_label)

        # Weather widget (placeholder)
        self.weather_label = QLabel("☀️ 32°C Jakarta")
        self.weather_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.main_layout.addWidget(self.weather_label, alignment=Qt.AlignRight)

    def _search(self):
        text = self.search_input.text()
        if text:
            self.parent().navigate("https://www.google.com/search?q=" + text.replace(" ", "+"))

    def _load_speed_dial(self):
        # Hapus item lama
        while self.speed_dial_grid.count():
            item = self.speed_dial_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        items = SpeedDialManager.get_all()
        for i, (title, url) in enumerate(items[:8]):
            btn = QPushButton(get_icon("shortcut"), title)
            btn.setIconSize(QSize(32, 32))
            btn.setFixedSize(120, 90)
            btn.clicked.connect(lambda checked, u=url: self.parent().navigate(u))
            # Context menu untuk hapus
            btn.setContextMenuPolicy(Qt.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, b=btn, u=url: self._show_context_menu(pos, b, u))
            row, col = divmod(i, 4)
            self.speed_dial_grid.addWidget(btn, row, col)

        # Tombol tambah jika kurang dari 8
        if len(items) < 8:
            add_btn = QPushButton("+ Add")
            add_btn.setFixedSize(120, 90)
            add_btn.clicked.connect(self._add_speed_dial)
            row, col = divmod(len(items), 4)
            self.speed_dial_grid.addWidget(add_btn, row, col)

    def _add_speed_dial(self):
        title, ok1 = QInputDialog.getText(self, "Add Shortcut", "Title:")
        if ok1 and title:
            url, ok2 = QInputDialog.getText(self, "Add Shortcut", "URL:")
            if ok2 and url:
                SpeedDialManager.add(title, url)
                self._load_speed_dial()

    def _show_context_menu(self, pos, btn, url):
        menu = QMenu()
        menu.addAction("Remove", lambda: self._remove_speed_dial(url))
        menu.exec_(btn.mapToGlobal(pos))

    def _remove_speed_dial(self, url):
        SpeedDialManager.remove(url)
        self._load_speed_dial()