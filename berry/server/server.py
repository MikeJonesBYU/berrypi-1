"""
Berry server class.
"""
import json
import logging
import socket
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import QObject

import pygame

from .. import utilities


class ThreadedServer(QObject):
    """
    Server class.
    """

    # Qt signals for sending messages from worker thread to main (GUI) thread
    _load_code_signal = QtCore.pyqtSignal(dict, name='load_code')
    _insert_name_signal = QtCore.pyqtSignal(str, name='insert-name')

    # Modes
    NORMAL_MODE = 0
    EDIT_MODE = 1

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

        # Which mode we're in
        self._mode = self.NORMAL_MODE

        # Shared state
        self._state = {}

        # Registration mapping for user handlers
        self._registered_berries = {}

        # Set up sockets
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udpsocket.bind(('', utilities.REGISTRATION_PORT))
        self._sock.bind((self._host, self._port))

        # Start up a separate thread to listen for broadcasts from new berries.
        threading.Thread(target=self.listen_for_new_berries).start()

        # Import pygame mixer for sounds
        pygame.mixer.init()

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

    def get_berries(self):
        """
        Gets all berries from the list.
        """
        return list(self._berries.values())

    def register_new_berry(self, data):
        """
        Registers a new berry.
        """
        if (not isinstance(data,str)):
            data = data.decode('utf-8')
        berry = json.loads(data)
        json.loads

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
                    # logging.info('\nReceived: ' + data.decode('utf-8'))
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
        logging.info(command)
        if command == 'newberry-via-fixedip':
            logging.info("new berry connected via fixed ip")
            self.register_new_berry(json.dumps(message['berry-body']))
            response = {
                'command': 'fixedip-ack',
                'ip': utilities.get_my_ip_address(),
                'source': message['source']
            }
            guid = message['berry-body']['guid']
            self.send_message_to_berry(guid, response)
        if command == 'berry-selected':
            logging.info("berry selected!")
            if self._mode == self.NORMAL_MODE:
                # Set mode (so we don't keep opening the window)
                self._mode = self.EDIT_MODE

                # Open the code editing window
                self.open_edit_code_window(
                    message['guid'],
                    message['name'],
                    message['code'],
                )

                threading.Thread(target=self._play_open_beep).start()

            elif self._mode == self.EDIT_MODE:
                # Insert the berry's name into the code editing window
                self._insert_name_signal.emit(message['name'])

                threading.Thread(target=self._play_insert_name_beep).start()

        elif command == 'remote-command':
            # Send remote command message to destination berry

            # First check to see if the code-key exists; if so, we're just
            # registering an event handler, not actually executing a command
            if 'code-key' in message:
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
            else:
                # Get the berry GUID
                berry = self.get_berry(name=message['destination'])

                if berry is not None:
                    guid = berry['guid']

                    # Prep the message to the destination berry
                    response = {
                        'command': 'remote-command',
                        'source': message['source'],
                        'attribute': message['attribute'],
                    }

                    if 'key' in message:
                        response['key'] = message['key']

                    if 'payload' in message:
                        response['payload'] = message['payload']

                    self.send_message_to_berry(guid, response)
                else:
                    # Nack the request
                    response = {
                        'command': 'remote-response',
                        'response': {
                            'error': 'widget-not-found',
                            'name': message['destination'],
                        }
                    }

                    widget = self.get_berry(name=message['source'])
                    guid = widget['guid']

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
            key = '{}|{}'.format(message['name'], message['event'])

            # Prep the message
            message = {
                'command': 'event',
                'event': message['event'],
                'source': message['name'],
                'key': key,
            }

            # Send the message to each registered berry (make sure first that
            # there is at least one registered berry)
            if key in self._registered_berries:
                registered_berries = self._registered_berries[key].keys()
                for berry in registered_berries:
                    berry = self.get_berry(name=berry)
                    guid = berry['guid']

                    self.send_message_to_berry(guid, message)

        elif command == 'update-state':
            # Update the shared state
            update_delta = message['state']
            self._state.update(update_delta)

            # Prep the message
            message = {
                'command': 'update-state',
                'state': self._state,
            }

            # Send the message to all berries
            self.broadcast_message(message)

        elif command == 'send-email':
            # Update the shared state
            to = message['to']
            subject = message['subject']
            body = message['body']

            self._send_email(to, subject, body)

        elif command == 'status':
            utilities.send_with_tcp(message = message, recv_address=utilities.FIXED_SERVER_IP_ADDRESS, port= 8080)


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

        # where does the port come from here?  mdj 5/20/2019
        # it is in <github>\berrypi\berry\client_for_testing\client.py
        # in package_self_as_json.
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
        # Play the beep
        self._play_save_changes_beep()

        message = {
            'command': 'code-save',
            'name': payload['name'],
            'code': payload['code'],
        }

        self.send_message_to_berry(payload['guid'], message)

        # Reset to normal mode now that we're no longer editing code
        self._mode = self.NORMAL_MODE

    def _play_open_beep(self):
        """
        Plays the beep for when the code window is opened.
        """
        try:
            s = pygame.mixer.Sound('berry/server/sounds/sfx_coin_cluster3.wav')
            s.play()
        except:
            logging.error('\n   *** ERROR playing open beep')

    def _play_insert_name_beep(self):
        """
        Plays the beep for when the name is inserted into the editor.
        """
        try:
            s = pygame.mixer.Sound('berry/server/sounds/sfx_coin_double4.wav')
            s.play()
        except Exception as ex:
            logging.error('\n   *** ERROR playing insert name beep')

    def _play_save_changes_beep(self):
        """
        Plays the beep for when changes are saved.
        """
        try:
            s = pygame.mixer.Sound(
                'berry/server/sounds/sfx_sound_neutral2.wav',
            )
            s.play()
        except Exception as ex:
            logging.error('\n   *** ERROR playing save changes beep')

    def _send_email(self, to, subject, body):
        """
        Sends a simple email.
        """
        import smtplib
        from email.message import EmailMessage

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['To'] = to
        msg['From'] = 'ben.crowder@gmail.com'

        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()
