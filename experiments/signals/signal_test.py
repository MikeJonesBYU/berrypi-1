import sys
import threading
import time

from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout
)


app = QApplication(sys.argv)
app.setApplicationName('Code Editor')


class MainThreadWidget(QWidget):
    """
    GUI widget on main thread.
    """
    _load_code_signal = QtCore.pyqtSignal(dict, name='load_code')
    _save_code_signal = QtCore.pyqtSignal(dict, name='save_code')

    def __init__(self):
        super().__init__()
        self.init_ui()

        self._load_code_signal.connect(self.load_code)

    def init_ui(self):
        self._save_button = QPushButton("Save Code")
        self._save_button.clicked.connect(self.save_code_handler)

        # Container
        vbox = QVBoxLayout()
        vbox.addWidget(self._save_button)
        self.setLayout(vbox)

        # Window settings
        self.resize(500, 500)
        self.setWindowTitle('Edit Code')

    def save_code_handler(self):
        print('Clicked save code on GUI thread, emitting save code to worker:')

        self._worker._save_code_signal.emit({
            'signal': 'save-code',
            'code': 'blah blah blah',
        })

    @QtCore.pyqtSlot(dict)
    def load_code(self, message):
        print('Main GUI thread, loading code, message=', message)
        print('Loaded code into GUI')
        

class WorkerThread(QObject):
    _window = None


    def __init__(self, window):
        super().__init__()

        self._window = window
        self._window._worker = self
        # self._window._save_code_signal = self._save_code_signal
        self._window._save_code_signal.connect(self.save_code)

    def listen(self):
        print('Listening on worker thread, emitting load code to GUI thread')

        self._window._load_code_signal.emit({
            'file': 'that file',
            'code': 'Garbanzo Bean',
        })

        while 1:
            pass

    @QtCore.pyqtSlot(dict)
    def save_code(self, message):
        print('On worker thread, saving code, message=', message)
        print('Saved code')


# Start GUI on main thread
window = MainThreadWidget()
window.show()

# Start worker thread
t = threading.Thread(target=lambda: WorkerThread(window).listen())
t.daemon = True
t.start()

sys.exit(app.exec_())
