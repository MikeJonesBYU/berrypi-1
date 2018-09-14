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

    def __init__(self, code, guid, server):
        super().__init__()
        self.init_ui(code)

        self._guid = guid
        self._server = server

    def init_ui(self, code):
        self._textbox = QTextEdit()
        self._textbox.setText(code)

        self._save_button = QPushButton("Save Code")
        self._save_button.clicked.connect(self.save_code_handler)

        # Container
        vbox = QVBoxLayout()
        vbox.addWidget(self._textbox)
        vbox.addWidget(self._save_button)
        self.setLayout(vbox)

        # Window settings
        self.resize(800, 800)
        self.setWindowTitle('Edit Code')
        self.show()

    def save_code_handler(self):
        """
        Handler for when the Save Code button is clicked.
        """
        code = self._save_button.text()
        guid = self._guid

        # Send code back to client
        self._server.send_edited_code(code, guid)
