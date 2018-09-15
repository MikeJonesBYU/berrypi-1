"""
Berry window class. Used for editing code
"""
import logging

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

    def set_server(self, server):
        """
        Saves a reference to the server instance. Used in save_code_handler().
        """
        self._server = server

        # Set up Qt signals
        self._server._load_code_signal.connect(self.load_code)

    def load_code(self, payload):
        """
        Loads the code into the QTextEdit instance.
        """
        logging.info('loading code', payload)

        self._textbox.setText(payload['code'])
        self._guid = payload['guid']

    def save_code_handler(self):
        """
        Handler for when the Save Code button is clicked.
        """
        payload = {
            'guid': self._guid,
            'code': self._textbox.text(),
        }

        # Send code back to client
        self._server._save_code_signal.emit(payload)
