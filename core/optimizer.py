import os
import gc
from PyQt5.QtCore import QTimer

class MemoryOptimizer:
    def __init__(self, parent=None):
        self.timer = QTimer(parent)
        self.timer.timeout.connect(self.optimize)
        self.timer.start(60000)  # setiap 60 detik

    def optimize(self):
        # Paksa garbage collection untuk mengurangi penggunaan memori
        gc.collect()