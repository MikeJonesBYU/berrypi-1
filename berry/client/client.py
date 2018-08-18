"""
Berry client functions.
"""
import json
import socket

from .. import utilities
from ..utilities import d

server_ip_address = '255.255.255.255'


def find_a_server(berry):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    output = berry._convert_to_json()
    d.dprint('Sending via udp broadcast...\n' + output)

    sock.sendto(
        output.encode('utf-8'),
        (
            '255.255.255.255',
            utilities.__initialization_port__,
        ),
    )
    sock.close()

    # Wait for a TCP connection from the server.
    response = utilities.blocking_receive_from_tcp(
        utilities.__initialization_port__,
    )

    server_response = json.loads(response)
    server_ip_address = server_response['ip_address']

    d.dprint('server is at ' + server_ip_address)
