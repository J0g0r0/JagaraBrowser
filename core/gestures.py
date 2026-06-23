from PyQt5.QtCore import QObject, QEvent, Qt, QPoint
from PyQt5.QtWidgets import QApplication

class GestureRecognizer(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.start_pos = QPoint()
        self.tracking = False
        window.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                self.start_pos = event.pos()
                self.tracking = True
                return True
        elif event.type() == QEvent.MouseMove and self.tracking:
            # opsional: draw line
            pass
        elif event.type() == QEvent.MouseButtonRelease:
            if self.tracking and event.button() == Qt.RightButton:
                self.tracking = False
                delta = event.pos() - self.start_pos
                if abs(delta.x()) > abs(delta.y()) and abs(delta.x()) > 40:
                    if delta.x() < 0:
                        self.window.current_tab().back()
                    else:
                        self.window.current_tab().forward()
                elif abs(delta.y()) > 40:
                    if delta.y() < 0:
                        self.window.add_new_tab()
                    else:
                        self.window.close_tab(self.window.tab_widget.currentIndex())
                return True
        return super().eventFilter(obj, event)