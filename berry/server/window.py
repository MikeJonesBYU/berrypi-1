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

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self._textbox = QTextEdit()
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
