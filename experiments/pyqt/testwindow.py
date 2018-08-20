#!/usr/bin/env python

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
)



class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Berry Test'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(
            self.left,
            self.top,
            self.width,
            self.height,
        )

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        self.button = QPushButton('Save', self)
        self.button.move(20, 80)

        self.button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        val = self.textbox.text()
        print('Val: {}'.format(val))


app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
