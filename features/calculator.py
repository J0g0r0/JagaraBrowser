from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt

class CalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator")
        self.resize(250, 300)
        layout = QVBoxLayout(self)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.display)

        buttons = [
            ['7','8','9','/'],
            ['4','5','6','*'],
            ['1','2','3','-'],
            ['0','.','=','+']
        ]
        grid = QGridLayout()
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn = QPushButton(text)
                btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
                grid.addWidget(btn, i, j)
        layout.addLayout(grid)

        self.current_input = ""

    def on_button_click(self, char):
        if char == '=':
            try:
                result = eval(self.current_input)
                self.display.setText(str(result))
                self.current_input = str(result)
            except:
                self.display.setText("Error")
                self.current_input = ""
        else:
            self.current_input += char
            self.display.setText(self.current_input)