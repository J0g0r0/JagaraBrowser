from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton

class ShortcutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        self.resize(500, 400)
        layout = QVBoxLayout(self)
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Shortcut", "Action"])
        shortcuts = [
            ("Ctrl+T", "New Tab"),
            ("Ctrl+W", "Close Tab"),
            ("Ctrl+Shift+T", "Reopen Closed Tab"),
            ("Ctrl+L", "Focus Address Bar"),
            ("Ctrl+D", "Bookmark This Page"),
            ("Ctrl+H", "Show History"),
            ("Ctrl+J", "Downloads"),
            ("Ctrl+Shift+N", "New Incognito Window"),
            ("Ctrl+R / F5", "Refresh"),
            ("Alt+Left", "Back"),
            ("Alt+Right", "Forward"),
            ("Ctrl+0", "Reset Zoom"),
            ("Ctrl+Plus", "Zoom In"),
            ("Ctrl+Minus", "Zoom Out"),
            ("Ctrl+Tab", "Next Tab"),
            ("Ctrl+Shift+Tab", "Previous Tab"),
            ("Ctrl+1..8", "Switch to Tab 1-8"),
            ("Ctrl+9", "Switch to Last Tab"),
            ("Ctrl+M", "Mute/Unmute Tab"),
            ("Ctrl+Shift+P", "Reading Mode"),
            ("F11", "Fullscreen"),
            ("Ctrl+Shift+B", "Toggle Bookmark Bar"),
            ("Ctrl+F", "Find in Page"),
            ("Escape", "Stop Loading"),
            ("Ctrl+S", "Save Page as PDF"),
            ("Ctrl+?", "Show This Dialog"),
        ]
        table.setRowCount(len(shortcuts))
        for i, (key, action) in enumerate(shortcuts):
            table.setItem(i, 0, QTableWidgetItem(key))
            table.setItem(i, 1, QTableWidgetItem(action))
        layout.addWidget(table)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)