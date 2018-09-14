"""
Berry window class. Used for editing code
"""
from PyQt5.QtWidgets import (
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class EditWindow(QWidget):
    """
    Window for editing code.
    """

    def __init__(self, code):
        super().__init__()
        self.init_ui(code)

    def init_ui(self, code):
        self._textbox = QTextEdit()
        self._textbox.setText(code)

        self._save_button = QPushButton("Save Code")

        # Container
        vbox = QVBoxLayout()
        vbox.addWidget(self._textbox)
        vbox.addWidget(self._save_button)
        self.setLayout(vbox)

        # Window settings
        self.resize(800, 800)
        self.setWindowTitle('Edit Code')
        self.show()
