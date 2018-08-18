"""
Server script.
"""
import sys

from berry import server, utilities

if __name__ == '__main__':
    try:
        port = int(utilities.SERVER_PORT)
    except ValueError:
        print('Invalid port', utilities.SERVER_PORT)
        sys.exit(-1)

    print(f'Starting server on port {port}')

    server.ThreadedServer('', port).listen()
