"""
Berry client functions.
"""
import json
import socket

from .. import utilities
from ..utilities import d

server_ip_address = '255.255.255.255'


def find_a_server(berry, port):
    """
    Finds server and initiates handshake.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    output = berry._convert_to_json()
    d.dprint('Sending via udp broadcast...\n' + output)

    sock.sendto(output.encode('utf-8'), ('255.255.255.255', port))
    sock.close()

    # Wait for a TCP connection from the server.
    response = utilities.blocking_receive_from_tcp(port)

    server_response = json.loads(response)
    server_ip_address = server_response['ip_address']

    d.dprint('server is at ' + server_ip_address)

    return server_response


def wait_for_message(port):
    """
    Waits for messages to come through in TCP. Part of the main client loop.
    """
    # Wait for a TCP connection from the server.
    return utilities.blocking_receive_from_tcp(port)


def process_message(message, berry):
    """
    Processes an incoming message.
    """
    message = json.loads(message)

    if 'type' not in message:
        d.dprint('Error, message missing type')
        return

    m_type = message['type']

    if m_type == 'code-edit':
        # TODO: implement
        d.dprint('Code editing message')
    elif m_type == 'other-message':
        pass
