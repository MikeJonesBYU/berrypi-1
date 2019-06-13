"""
Server script. Usage: python3 server.py

To start with the button sidebar: python3 server.py sidebar
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
        logging.error('Invalid port: {}'.format(utilities.SERVER_PORT))
        sys.exit(-1)

    sidebar = False
    if len(sys.argv) > 1 and sys.argv[1] == 'sidebar':
        sidebar = True

    app = QApplication(sys.argv)
    app.setApplicationName('Code Editor')
    edit_window = server.window.EditWindow(sidebar=sidebar)

    start_string = 'Starting server on port {}'.format(port)
    if sidebar:
        start_string += ', with sidebar'

    logging.info(start_string)

    # Start thread for server
    t = threading.Thread(
        target=lambda: server.ThreadedServer(
            '',
            port,
            edit_window,
            sidebar=sidebar,
        ).listen()
    )
    t.daemon = True
    t.start()

    sys.exit(app.exec_())
