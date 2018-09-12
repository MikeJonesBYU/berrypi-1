"""
Berry client class.
"""
import json
import logging
import socket

from .. import utilities

server_ip_address = 0


class BerryClient():
    _berry = None
    _port = None

    def __init__(self, berry, port):
        self._berry = berry
        self._port = int(port)

    def find_a_server(self):
        """
        Finds server and initiates handshake.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        output = self._berry._as_json()
        output['port'] = self._port
        output = json.dumps(output)

        logging.info('Sending via udp broadcast...\n' + output)

        sock.sendto(
            output.encode('utf-8'),
            ('255.255.255.255', utilities.REGISTRATION_PORT),
        )
        sock.close()

        # Wait for a TCP connection from the server.
        response = utilities.blocking_receive_from_tcp(self._port)

        server_response = json.loads(response)
        global server_ip_address
        server_ip_address = server_response['ip']

        logging.info('Server IP is {}'.format(server_ip_address))

        return server_response

    def wait_for_message(self):
        """
        Waits for messages to come through in TCP. Part of the main client
        loop.
        """
        # Wait for a TCP connection from the server.
        return utilities.blocking_receive_from_tcp(self._port)

    def listen(self):
        """
        Listen for messages from the server.
        """
        return utilities.tcp_listen(self._port, self.process_message)

    def process_message(self, message):
        """
        Processes an incoming message.
        """
        message = json.loads(message)

        if 'type' not in message:
            logging.error('Error, message missing type')
            return

        m_type = message['type']

        if m_type == 'code-edit':
            # TODO: implement
            logging.info('Code editing message')
        elif m_type == 'other-message':
            pass


def send_message_to_server(message):
    logging.info("Sending message to server: {}".format(message))

    logging.debug('SERVER IP: {}'.format(server_ip_address))

    utilities.send_with_tcp(
        json.dumps(message),
        server_ip_address,
        utilities.SERVER_PORT,
    )
