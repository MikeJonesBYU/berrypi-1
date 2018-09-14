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
        self._save_button.clicked.connect(self.save_code_handler)

        # Container
        vbox = QVBoxLayout()
        vbox.addWidget(self._textbox)
        vbox.addWidget(self._save_button)
        self.setLayout(vbox)

        # Window settings
        self.resize(800, 800)
        self.setWindowTitle('Edit Code')

    def set_guid(self, guid):
        """
        Saves a copy of the guid. Used in save_code_handler().
        """
        self._guid = guid

    def set_server(self, server):
        """
        Saves a reference to the server instance. Used in save_code_handler().
        """
        self._server = server

    def load_code(self, code):
        """
        Loads the code into the QTextEdit instance.
        """
        self._textbox.setText(code)

    def save_code_handler(self):
        """
        Handler for when the Save Code button is clicked.
        """
        code = self._save_button.text()
        guid = self._guid

        # Send code back to client
        self._server.send_edited_code(code, guid)
