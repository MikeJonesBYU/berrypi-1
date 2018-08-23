"""
Server script.
"""
import logging
import sys

from berry import server, utilities

logging.getLogger().setLevel(utilities.LOG_LEVEL)


if __name__ == '__main__':

    try:
        port = int(utilities.SERVER_PORT)
    except ValueError:
        logging.error('Invalid port', utilities.SERVER_PORT)
        sys.exit(-1)

    logging.info('Starting server on port {}'.format(port))

    server.ThreadedServer('', port).listen()
