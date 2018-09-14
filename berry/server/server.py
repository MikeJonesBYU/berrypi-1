"""
Berry server class.
"""
import json
import logging
import socket
import threading

from .. import utilities
from . import window


class ThreadedServer(object):
    _berries = {}

    def __init__(self, host, port, edit_window):
        self._berries = {}

        self._host = host
        self._port = port
        self._edit_window = edit_window

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
            logging.info('Received via UDP: {}'.format(message))

            threading.Thread(
                target=self.register_new_berry,
                args=(data,)
            ).start()

    def add_berry(self, berry):
        """
        Adds a new berry to the list.
        """
        self._berries[berry['guid']] = berry

    def get_berry(self, guid):
        """
        Gets a berry from the list, by guid.
        """
        if guid in self._berries:
            return self._berries[guid]

        return None

    def get_berries(self, guid):
        """
        Gets all berries from the list.
        """
        return self._berries

    def register_new_berry(self, data):
        """
        Registers a new berry.
        """
        berry = json.loads(data.decode('utf-8'))

        logging.info('Berry name: ' + berry['name'])

        # Add to berry list
        self.add_berry(berry)

        # Open a TCP connection and send server address to client
        response = {
            'ip': utilities.get_my_ip_address(),
        }

        self.send_message_to_berry(guid=berry['guid'], message=response)

        # Debug:
        logging.info('\nBerries: {}'.format(self._berries))

    def listen(self):
        """
        Server listener. Used by the server.py in the root directory.
        """
        self._sock.listen(256)

        while True:
            client, address = self._sock.accept()
            client.settimeout(60)

            threading.Thread(
                target=self.listen_to_client,
                args=(client, address),
            ).start()

    def listen_to_client(self, client, address):
        """
        Receiver.
        """
        size = 64
        logging.info('Someone is connecting:')

        message = ''
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the received data
                    logging.info('\nReceived: ' + data.decode('utf-8'))
                    message += data.decode('utf-8')
                else:
                    logging.info('Client at ' + address.__str__() + ' closed')
                    client.close()
                    break
            except Exception as e:
                logging.error('Exception: {} ({})'.format(e, type(e)))
                client.close()
                return False

        logging.info('Out of receive loop')

        self.process_message(message)

    def process_message(self, message):
        """
        Processes an incoming message.
        """
        print('process', message)

        message = json.loads(str(message))

        if 'type' not in message:
            logging.error('Error, message missing type')
            return

        m_type = message['type']

        if m_type == 'code-edit':
            logging.info('Code editing message')

            self.open_edit_code_window(message['code'], message['guid'])
        elif m_type == 'other-message':
            pass

    def send_message_to_berry(self, guid, message):
        """
        Sends a message (an object, not yet serialized) to the berry with the
        matching guid.
        """
        berry = self.get_berry(guid)

        # If the guid hasn't been registered, berry will be None
        if berry is None:
            return

        utilities.send_with_tcp(
            json.dumps(message),
            berry['ip'],
            berry['port'],
        )

    def broadcast_message(self, message):
        """
        Sequentially sends a message (an object, not yet serialized) to all
        berries in the list.
        """
        for berry in self.get_berries():
            self.send_message_to_berry(berry['guid'], message)

    def open_edit_code_window(self, code, guid):
        """
        Opens the window for editing code, loading needed data first.
        """
        self._edit_window.load_code(code)
        self._edit_window.set_guid(guid)
        self._edit_window.set_server(self)
        self._edit_window.show()

    def send_edited_code(self, code, guid):
        """
        Sends the edited code back to the client via the code-save message.
        """
        logging.debug('Now sending the code-save message to the server')

        message = {
            'type': 'code-save',
            'code': code,
        }

        self.send_message_to_berry(self, guid, message)
