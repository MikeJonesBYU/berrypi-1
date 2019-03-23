"""
BerryBase class used as a base class for berries.
"""
import importlib
import json
import logging
import os
import shutil
import types

from . import remote
from . import utilities


WIDGET_TYPES = [
    'button',
    'led',
    'screen',
    'accelerometer',
    'distance',
    'fsr',  # force sensitive resistor
    'speaker',
]

WIDGET_BASE_PATH = 'berry/client'
WIDGET_IMPORT_PATH = 'berry.client._handlers'


class BerryBase():
    berry_type = 'none'
    name = 'none'
    guid = 'none'
    ip_address = 'none'
    live = False

    def __init__(self, berry_type, live, guid, name=None, path=None,
                import_path=None):
        if berry_type in WIDGET_TYPES:
            self.berry_type = berry_type
        else:
            logging.error(
                '\n   *** ERROR, invalid type to berry constructor {}'.format(
                    berry_type,
                ),
            )
            self.berry_type = 'invalid'

        self.guid = guid
        self.ip_address = utilities.get_my_ip_address()

        # Whether the berry is live (on a Pi) or not (testing locally)
        self.live = live

        # Set up default path
        if path is None:
            path = WIDGET_BASE_PATH

        # And configure paths
        self._widget_name_path = '{}/_widget_name.txt'.format(path)
        self._widget_handlers_path = '{}/_handlers.py'.format(path)
        self._widget_handlers_tmp_path = '{}/_handlers_tmp.py'.format(path)

        # Set up default import path
        if import_path is None:
            self._widget_import_path = WIDGET_IMPORT_PATH
        else:
            self._widget_import_path = import_path

        # Load the berry name from the parameter if present or from disk
        if name is not None:
            self.name = name
        else:
            # Load from disk
            self.get_berry_name()

        # Import the handlers
        self.import_handlers()

        # Initialize hardware (if we're on an actual widget)
        if self.live and hasattr(self, '_initialize_hardware'):
            logging.info('Initializing hardware')
            self._initialize_hardware()
            logging.info('Done initializing hardware')

    def _as_json(self):
        """
        Serializes the berry to JSON.
        """
        berry = {
            'guid': self.guid,
            'name': self.name,
            'type': self.berry_type,
            'ip': self.ip_address,
        }

        logging.info('Berry as an object: {}'.format(json.dumps(berry)))

        return berry

    def methods(self):
        """
        Returns a list of the class's public methods. TODO: should this be
        hardcoded for each berry type?
        """
        # List of methods not to include
        exception_list = [
            'call_handler',
            'get_berry_name',
            'import_handlers',
            'initialize_hardware',
            'load_handler_code',
            'methods',
            'reload_handlers',
            'save_berry_name',
            'update_handler_code',
        ]

        return [
            f
            for f in dir(self)
            if (
                f[0] != '_'
                and
                f not in exception_list
                and
                isinstance(getattr(self, f), types.MethodType)
            )
        ]

    def import_handlers(self):
        """
        Imports the berry's handlers from client/handlers. Stashes the imported
        handlers in self._handlers, since that's how importlib works (and it
        conveniently makes it far easier to reference the imported handlers
        in the subclasses).
        """
        try:
            self._handlers = importlib.import_module(self._widget_import_path)
        except SyntaxError as ex:
            self._handlers = {}
            logging.error(
                '\n   *** ERROR, syntax error loading handlers: {}'.format(ex),
            )

    def reload_handlers(self):
        """
        Reloads the berry's handlers from client/handlers.
        """
        try:
            new_handlers = importlib.reload(self._handlers)
            self._handlers = new_handlers

        except SyntaxError as ex:
            self._handlers = {}
            logging.error(
                '\n   *** ERROR, syntax error reloading handlers: {}'.format(
                    ex,
                ),
            )

        except TypeError as ex:
            # Reloading handlers that were never loaded to begin with, so import
            # them instead
            self.import_handlers()

        # Now that we've got the handlers, set up the client
        self.setup_client()

    def setup_client(self):
        """
        Code that needs to run when a client is initially set up and also when
        the handlers are reloaded. Called in client's and in BerryBase's
        reload_handlers method.
        """
        # Reload the user handler code since the old code is no longer
        # applicable; if self._client doesn't exist yet, we're on initial
        # load and don't need to worry
        self._client.wipe_user_handlers()

        # Run the client's setup() function if it exists
        self.call_handler('setup')

    def loop_client(self):
        """
        Code that needs to run when a client is initially set up and also when
        the handlers are reloaded. Called in client's and in BerryBase's
        reload_handlers method.
        """
        # Run the client's loop() function if it exists
        self.call_handler('loop')

    def call_handler(self, name, *args, **kwargs):
        """
        Wrapper method to call a given handler.
        """
        # Get the state
        state = self._client.get_state()

        # Instantiate RemoteBerries
        remote_berries = remote.RemoteBerries(self._client)

        # Get the handler function from the berry.client.handlers module
        try:
            handler = getattr(self._handlers, name)
        except AttributeError:
            handler = None

        if not handler:
            if name == 'setup':
                # Setup is optional, so just return without an error
                return

            if name == 'loop':
                # No loop handler
                self._client._looping = False

            # Raise an exception since the handler doesn't exist
            logging.error('\n   *** ERROR, handler not found: {}'.format(name))
            return None

        # Call the handler, passing in the state and the RemoteBerries instance
        # and any other arguments
        try:
            return handler(
                state,
                remote_berries,
                self,  # the berry itself
                *args,
                **kwargs,
            )
        except Exception:
            # If there was an exception running the handler, bail out
            return None

    def load_handler_code(self):
        """
        Returns the handler code in client/handlers.py. Used for code editing.
        """
        with open(self._widget_handlers_path, 'r') as f:
            code = f.read()

        return code

    def update_handler_code(self, code):
        """
        Updates the handler code in client/handlers.py. Used for code editing.
        """
        temp_path = self._widget_handlers_tmp_path
        dest_path = self._widget_handlers_path

        # Write out to the temp copy
        with open(temp_path, 'w') as f:
            f.write(code)

        # Make sure it worked
        with open(temp_path, 'r') as f:
            disk_code = f.read()

        if code != disk_code:
            logging.error('\n   *** ERROR, code written to disk doesn\'t match')
            return

        # Move the temp copy over the real copy
        shutil.copy(temp_path, dest_path)
        os.remove(temp_path)

        logging.info('Code updated, now reloading handlers')
        self.reload_handlers()

    def get_berry_name(self):
        """
        Reads in the widget name and returns it.
        """
        with open(self._widget_name_path, 'r') as f:
            name = f.read()

        self.name = name.strip()

        return self.name

    def save_berry_name(self, name):
        """
        Saves the name to disk.
        """
        self.name = name

        with open(self._widget_name_path, 'w') as f:
            f.write(self.name)

    def send_message_to_server(self, message):
        """
        Wrapper for sending a message to the server.
        """
        self._client.send_message_to_server(message)

    def send_email(self, to, subject, body):
        """
        Wrapper for sending an email via the server.
        """
        self._client.send_email(to, subject, body)

    def on_global_state_change(self):
        """
        Function allowing the user code to implement an
        on_global_state_change() handler that's called whenever the client
        receives a new state update.
        """
        # Run the client's on_global_state_change() function if it exists
        self.call_handler('on_global_state_change')

    def on_test(self):
        """
        Function calling the on_test() handler, used for debugging.
        """
        # Run the client's on_test() function if it exists
        self.call_handler('on_test')
