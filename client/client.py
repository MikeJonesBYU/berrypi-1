import socket
import utilities
from utilities import d

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((utilities.__server_address__, utilities.__port_number__))
    sock.send(b'hello over there ')