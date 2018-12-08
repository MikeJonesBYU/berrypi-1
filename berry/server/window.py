"""
Berry window class. Used for editing code
"""
import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
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
        self._name_textbox = QLineEdit()
        self._code_textbox = QTextEdit()

        self._save_button = QPushButton("Save Changes")
        self._save_button.clicked.connect(self.save_code_handler)

        # Container
        vbox = QVBoxLayout()

        vbox.addWidget(QLabel("Widget Name"))
        vbox.addWidget(self._name_textbox)

        vbox.addWidget(QLabel("Widget Handler Code"))
        vbox.addWidget(self._code_textbox)

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
        self._server._insert_name_signal.connect(self.insert_name)

    @QtCore.pyqtSlot(dict)
    def load_code(self, payload):
        """
        Loads the code into the QTextEdit instance.
        """
        self._guid = payload['guid']
        self._name_textbox.setText(payload['name'])
        self._code_textbox.setText(payload['code'])

        self.show()
        self.raise_()

    @QtCore.pyqtSlot(str)
    def insert_name(self, name):
        """
        Inserts the berry name into the QTextEdit instance at the cursor.
        """
        cursor = self._code_textbox.textCursor()
        cursor.insertText(name)

        # Make sure the window is on top
        self.show()
        self.raise_()

    def save_code_handler(self):
        """
        Handler for when the Save Code button is clicked.
        """
        payload = {
            'guid': self._guid,
            'name': self._name_textbox.text(),
            'code': self._code_textbox.toPlainText(),
        }

        # Send code back to client
        self._server.send_edited_code(payload)

        # And close the window (doesn't work yet, it kills the whole app)
        # self.close()
