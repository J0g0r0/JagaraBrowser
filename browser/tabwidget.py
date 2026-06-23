from PyQt5.QtWidgets import QTabWidget, QTabBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

class GroupedTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.group_colors = {}  # tab_index -> QColor

    def set_tab_group(self, index, color: QColor):
        self.group_colors[index] = color
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        # Gambar indikator warna di bawah tab jika dikelompokkan
        painter = QPainter(self)
        for i in range(self.count()):
            if i in self.group_colors:
                rect = self.tabRect(i)
                painter.fillRect(rect.adjusted(4, rect.height()-4, -4, 0), self.group_colors[i])