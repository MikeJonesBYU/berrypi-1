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
    """
    Server class.
    """

    # Qt signals for sending messages from worker thread to main (GUI) thread
    _load_code_signal = QtCore.pyqtSignal(dict, name='load_code')

    def __init__(self, host, port, edit_window):
        super().__init__()

        self._host = host
        self._port = port

        # Maps GUIDs to berry instances
        self._berries = {}

        # Maps berry names to berry instances
        self._berry_names = {}

        # Reference to Qt window for editing code
        self._edit_window = edit_window
        self._edit_window.set_server(self)

        # Whether we're currently editing code
        self._editing_code = False

        # Registration mapping for user handlers
        self._registered_berries = {}

        # Set up sockets
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
            if not self._editing_code:
                # Set mode (so we don't keep opening the window)
                self._editing_code = True

                # Open the code editing window
                self.open_edit_code_window(
                    message['guid'],
                    message['name'],
                    message['code'],
                )

        elif command == 'remote-command':
            # Send remote command message to destination berry

            # First check to see if the code-key exists; if so, we're just
            # registering an event handler, not actually executing a command
            if 'code-key' in message:
                logging.info('Code key in message: {}'.format(message['code-key']))
                # Register this code key for the source berry
                key = message['code-key']
                registrations = self._registered_berries

                # Initialize the list
                if key not in registrations:
                    registrations[key] = {}

                # Add key to the list if it's not already in there
                source = message['source']
                if source not in registrations[key]:
                    registrations[key][source] = True

                # self._registered_berries = registrations

                logging.info('Registrations')
                logging.info(self._registered_berries)
            else:
                # Get the berry GUID
                berry = self.get_berry(name=message['destination'])
                guid = berry['guid']

                # Prep the message to the destination berry
                response = {
                    'command': 'remote-command',
                    'source': message['source'],
                    'attribute': message['attribute'],
                    'key': message['key'],
                }

                if 'payload' in response:
                    message['payload'] = response['payload']

                self.send_message_to_berry(guid, response)

        elif command == 'remote-response':
            # Send response message back to the source berry

            # Get the berry GUID
            berry = self.get_berry(name=message['destination'])
            guid = berry['guid']

            # Prep the message to the source berry
            response = {
                'command': 'remote-response',
                'response': message['response'],
                'key': message['key'],
            }

            self.send_message_to_berry(guid, response)

        elif command == 'event':
            # Send event message to any berries registered for that
            # event/client pair
            logging.info('got event message')
            logging.info(message)

            key = '{}|{}'.format(message['name'], message['event'])

            # Prep the message
            message = {
                'command': 'event',
                'event': message['event'],
                'source': message['name'],
                'key': key,
            }

            # Send the message to each registered berry
            registered_berries = self._registered_berries[key].keys()
            for berry in registered_berries:
                berry = self.get_berry(name=berry)
                guid = berry['guid']

                self.send_message_to_berry(guid, message)

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

        self._editing_code = False
