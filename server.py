"""
Server script.
"""
from berry import server, utilities

if __name__ == '__main__':
    while True:
        port_num = utilities.__port_number__
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    print(f'starting server on port {port_num}')

    server.ThreadedServer('', port_num).listen()
