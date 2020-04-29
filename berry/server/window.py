"""
Berry window class. Used for editing code
"""
import logging

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QAction,
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CodeEditor(QTextEdit):
    """
    QTextEdit for editing code.
    """
    def __init__(self, parent=None, server=None):
        QTextEdit.__init__(self, parent)

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        flash_action = QAction("Flash", self)
        flash_action.triggered.connect(self.flash)
        self.addAction(flash_action)

    def set_server(self, server, window):
        self._server = server
        self._window = window

    def flash(self):
        """
        Sends the flash message.
        """
        # Get selected text and put in name
        name = self._window.get_selected_text()

        payload = {
            'name': name,
        }

        # Flashes the client
        self._server.flash_client(payload)


class WidgetNameEditor(QLineEdit):
    """
    QLineEdit for editing the widget name.
    """
    def __init__(self, parent=None, server=None):
        QTextEdit.__init__(self, parent)

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        flash_action = QAction("Flash", self)
        flash_action.triggered.connect(self.flash)
        self.addAction(flash_action)

    def set_server(self, server, window):
        self._server = server
        self._window = window

    def flash(self):
        """
        Sends the flash message.
        """
        # Get selected text and put in name
        name = self._window.get_selected_text()

        payload = {
            'name': name,
        }

        # Flashes the client
        self._server.flash_client(payload)


class EditWindow(QMainWindow):
    """
    Window for editing code.
    """

    def __init__(self, sidebar=False):
        super().__init__()
        self.init_ui(sidebar=sidebar)

    def init_ui(self, sidebar=False):
        font = QtGui.QFont('Monaco')
        font.setPointSize(21)

        self._name_textbox = WidgetNameEditor(parent=self)
        self._code_textbox = CodeEditor(parent=self)

        self._name_textbox.setFont(font)
        self._code_textbox.setFont(font)

        self._save_button = QPushButton("Save Changes")
        self._save_button.clicked.connect(self.save_code_handler)

        # Container
        vbox = QVBoxLayout()

        vbox.addWidget(QLabel("Widget Name"))
        vbox.addWidget(self._name_textbox)

        vbox.addWidget(QLabel("Widget Handler Code"))
        vbox.addWidget(self._code_textbox)

        vbox.addWidget(self._save_button)

        if sidebar:
            # Use the sidebar wrapper
            self._widget_dock = QVBoxLayout()
            self.setStyleSheet("""
                .QVBoxLayout {
                    background-color: rgb(255, 0, 0);
                }
            """)

            # Dock
            self._dock = QDockWidget("Widgets", self)
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._dock)
            self._dock_widget = QWidget(self)
            self._dock.setWidget(self._dock_widget)
            self._dock_widget.setLayout(self._widget_dock)

            # Button references
            self._widget_buttons = {}

        frame_widget = QWidget(self)
        frame_widget.setLayout(vbox)
        self.setCentralWidget(frame_widget)

        # Window settings
        self.resize(800, 800)
        self.setWindowTitle('Edit Code')

    def set_server(self, server):
        """
        Saves a reference to the server instance. Used in save_code_handler().
        """
        self._server = server
        self._name_textbox.set_server(server=server, window=self)
        self._code_textbox.set_server(server=server, window=self)

        # Set up Qt signals
        self._server._load_code_signal.connect(self.load_code)
        self._server._insert_name_signal.connect(self.insert_name)
        self._server._dock_widget_signal.connect(self.add_widget_to_dock)
        self._server._show_window_signal.connect(self.show_window)

    @QtCore.pyqtSlot(dict)
    def load_code(self, payload):
        """
        Loads the code into the QTextEdit instance.
        """
        self._guid = payload['guid']
        self._name_textbox.setText(payload['name'])
        self._code_textbox.setText(payload['code'])

        if not self._server._sidebar:
            self.show()

        self._code_textbox.setFocus()

        if not self._server._sidebar:
            self.raise_()

    @QtCore.pyqtSlot(str)
    def insert_name(self, name):
        """
        Inserts the berry name into the QTextEdit instance at the cursor.
        """
        cursor = self._code_textbox.textCursor()
        cursor.insertText(name)

        # Make sure the window is on top
        if not self._server._sidebar:
            self.show()
            self.raise_()

    @QtCore.pyqtSlot(dict)
    def add_widget_to_dock(self, payload):
        """
        Adds a button for the given widget.
        """
        def click():
            """
            Handler for clicking widget, using a closure to capture vars.
            """
            code = self._server._code[payload['guid']]
            widget = self._server.get_berry(guid=payload['guid'])

            self._server.select_widget(
                payload['guid'],
                widget['name'],
                code=code,
            )

        button = QPushButton(payload['name'])
        button.clicked.connect(click)
        self._widget_buttons[payload['guid']] = button

        # Add to dock
        logging.info('Adding to dock for real')
        self._widget_dock.addWidget(button)

    @QtCore.pyqtSlot(dict)
    def show_window(self, payload):
        """
        Shows the code window.
        """
        self.show()
        self.raise_()

    def save_code_handler(self):
        """
        Handler for when the Save Code button is clicked.
        """
        name = self._name_textbox.text()

        payload = {
            'guid': self._guid,
            'name': name,
            'code': self._code_textbox.toPlainText(),
        }

        # Send code back to client
        self._server.send_edited_code(payload)

        # Sidebar
        if self._server._sidebar:
            # Clear out the code
            self._name_textbox.setText('')
            self._code_textbox.setText('')

            # And update the widget name (if necessary)
            widget = self._server.get_berry(guid=self._guid)
            widget['name'] = name
            self.update_widget_button(self._guid, name)
        else:
            # Hide the window
            self.hide()

    def update_widget_button(self, guid, name):
        """
        Updates the widget specified by guid to have the name specified by
        name, in the sidebar list.
        """
        button = self._widget_buttons[guid]
        button.setText(name)

    def get_selected_text(self):
        """
        Gets the selected text in the code textbox.
        """
        cursor = self._code_textbox.textCursor()
        return cursor.selectedText()
