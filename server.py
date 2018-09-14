"""
Server script.
"""
import logging
import sys
import threading

from PyQt5.QtWidgets import (
    QApplication,
)

from berry import server, utilities

logging.getLogger().setLevel(utilities.LOG_LEVEL)


if __name__ == '__main__':

    try:
        port = int(utilities.SERVER_PORT)
    except ValueError:
        logging.error('Invalid port', utilities.SERVER_PORT)
        sys.exit(-1)

    logging.info('Setting up Qt')
    app = QApplication(sys.argv)
    app.setApplicationName('Code Editor')
    edit_window = server.window.EditWindow()

    logging.info('Starting server on port {}'.format(port))

    # Start thread for server
    threading.Thread(
        target=lambda: server.ThreadedServer('', port, edit_window).listen()
    ).start()

    sys.exit(app.exec_())
