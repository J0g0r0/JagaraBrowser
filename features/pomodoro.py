from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer, Qt

class PomodoroDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pomodoro Timer")
        self.resize(300, 200)
        layout = QVBoxLayout(self)

        self.label = QLabel("25:00")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.label)

        self.progress = QProgressBar()
        self.progress.setMaximum(25*60)
        layout.addWidget(self.progress)

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_timer)
        layout.addWidget(self.start_btn)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_btn)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining = 25 * 60
        self.running = False

    def start_timer(self):
        if not self.running:
            self.timer.start(1000)
            self.running = True
            self.start_btn.setText("Pause")
        else:
            self.timer.stop()
            self.running = False
            self.start_btn.setText("Resume")

    def reset_timer(self):
        self.timer.stop()
        self.running = False
        self.remaining = 25 * 60
        self.update_display()
        self.start_btn.setText("Start")

    def update_timer(self):
        self.remaining -= 1
        self.update_display()
        if self.remaining <= 0:
            self.timer.stop()
            self.running = False
            self.start_btn.setText("Done!")

    def update_display(self):
        mins, secs = divmod(self.remaining, 60)
        self.label.setText(f"{mins:02d}:{secs:02d}")
        self.progress.setValue(25*60 - self.remaining)