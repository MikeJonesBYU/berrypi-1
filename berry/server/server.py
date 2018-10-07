"""
Berry server class.
"""
import json
import logging
import socket
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import QObject

from .. import utilities


class ThreadedServer(QObject):
    # Maps GUIDs to berry instances
    _berries = {}

    # Maps berry names to berry instances
    _berry_names = {}

    # Qt signals for sending messages from worker thread to main (GUI) thread
    _load_code_signal = QtCore.pyqtSignal(dict, name='load_code')

    def __init__(self, host, port, edit_window):
        super().__init__()

        self._berries = {}
        self._berry_names = {}

        self._host = host
        self._port = port

        self._edit_window = edit_window
        self._edit_window.set_server(self)

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
        self._berry_names[berry['name']] = berry

    def get_berry(self, guid=None, name=None):
        """
        Gets a berry from the list, by either guid or name.
        """
        if guid and guid in self._berries:
            return self._berries[guid]

        if name and name in self._berry_names:
            return self._berry_names[name]

        # Didn't find it either way
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

        logging.info('Registering berry (name=' + berry['name'] + ')')

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
        message = json.loads(str(message))

        if 'command' not in message:
            logging.error('Error, message missing command')
            return

        command = message['command']

        if command == 'code-edit':
            # Edit code
            self.open_edit_code_window(message['code'], message['guid'])
        else:
            # Anything else
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

    def open_edit_code_window(self, guid, name, code):
        """
        Opens the window for editing code, loading needed data first.
        """
        self._load_code_signal.emit({
            'guid': guid,
            'name': name,
            'code': code,
        })

    def send_edited_code(self, payload):
        """
        Sends the edited code back to the client via the code-save message.
        """
        message = {
            'command': 'code-save',
            'name': payload['name'],
            'code': payload['code'],
        }

        self.send_message_to_berry(payload['guid'], message)
