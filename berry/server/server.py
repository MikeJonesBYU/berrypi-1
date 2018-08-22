"""
Berry server class.
"""
import json
import logging
import socket
import threading

from .. import utilities


class ThreadedServer(object):
    _berries = {}

    def __init__(self, host, port):
        self._berries = {}

        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._udpsocket.bind(('', utilities.REGISTRATION_PORT))
        self._sock.bind((self._host, self._port))

        # Start up a separate thread to listen for broadcasts from new berries.
        threading.Thread(target=self.listen_for_new_berries).start()

    def listen_for_new_berries(self):
        while True:
            data = self._udpsocket.recv(256)
            message = data.decode('utf-8')
            logging.info(f'Received via UDP: {message}')

            threading.Thread(
                target=self.communicate_with_new_berry,
                args=(data,)
            ).start()

    def add_berry(self, berry):
        """
        Adds a new berry to the list.
        """
        self._berries[berry['guid']] = berry

    def communicate_with_new_berry(self, data):
        berry_info = json.loads(data.decode('utf-8'))

        logging.info('Berry name: ' + berry_info['name'])

        # Add to berry list
        self.add_berry(berry_info)

        # Open a TCP connection and send server address to client
        response = {
            'ip': utilities.get_my_ip_address(),
        }

        utilities.send_with_tcp(
            json.dumps(response),
            berry_info['ip'],
            berry_info['port'],
        )

        # Debug:
        logging.info(f'\nBerries: {self._berries}')

    def listen(self):
        self._sock.listen(256)
        while True:
            client, address = self._sock.accept()
            client.settimeout(60)

            threading.Thread(
                target=self.listen_to_client,
                args=(client, address),
            ).start()

    def listen_to_client(self, client, address):
        size = 64
        logging.info('Someone is connecting:')

        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    logging.info('\nReceived: ' + data.decode('utf-8'))
                    response = data
                else:
                    logging.info('Client at ' + address.__str__() + ' closed')
                    client.close()
                    break
            except Exception as e:
                logging.error('Exception: {} ({})'.format(e, type(e)))
                client.close()
                return False

        logging.info('Out of receive loop')

        return response
