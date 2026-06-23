"""
Settings dialog for themes, privacy, and more.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTabWidget, QCheckBox, QComboBox,
    QPushButton, QLabel, QWidget
)
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(500, 400)
        layout = QVBoxLayout(self)

        tabs = QTabWidget()

        # Appearance tab
        appear = QWidget()
        appear_layout = QVBoxLayout(appear)
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark", "Light"])
        theme_combo.setCurrentText(parent.current_theme.capitalize())
        theme_combo.currentTextChanged.connect(lambda t: setattr(parent, 'current_theme', t.lower()))
        appear_layout.addWidget(QLabel("Theme:"))
        appear_layout.addWidget(theme_combo)
        tabs.addTab(appear, "Appearance")

        # Privacy tab
        privacy = QWidget()
        privacy_layout = QVBoxLayout(privacy)
        self.dnt_check = QCheckBox("Send 'Do Not Track' request")
        privacy_layout.addWidget(self.dnt_check)
        tabs.addTab(privacy, "Privacy")

        layout.addWidget(tabs)

        # Buttons
        btn_layout = QVBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)