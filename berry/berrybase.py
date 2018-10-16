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


BERRY_TYPES = ['button', 'slider', 'led']

BERRY_BASE_PATH = 'berry/client'

BERRY_NAME_PATH = '{}/_berry_name.txt'.format(BERRY_BASE_PATH)
BERRY_HANDLERS_PATH = '{}/_handlers.py'.format(BERRY_BASE_PATH)
BERRY_HANDLERS_TMP_PATH = '{}/_handlers_tmp.py'.format(BERRY_BASE_PATH)


class BerryBase():
    berry_type = 'none'
    name = 'none'
    guid = 'none'
    ip_address = 'none'

    def __init__(self, berry_type, guid, name=None):
        if berry_type in BERRY_TYPES:
            self.berry_type = berry_type
        else:
            logging.error('invalid type to berry constructor {}'.format(
                berry_type,
            ))
            self.berry_type = 'invalid'

        self.guid = guid
        self.ip_address = utilities.get_my_ip_address()

        # Load the berry name from the parameter if present or from disk
        if name is not None:
            self.name = name
        else:
            # Load from disk
            self.get_berry_name()

        # Import the handlers
        self.import_handlers()

        # Initialize GPIO (if we're on a berry)
        if hasattr(self, 'initialize_gpio'):
            logging.info('Initializing GPIO')
            self.initialize_gpio()

    def _as_json(self):
        """
        Serializes the berry to JSON.
        """
        berry = {
            'guid': self.guid,
            'name': self.name,
            'type': self.berry_type,
            'ip': self.ip_address,
            'handlers': self.methods(),
        }

        logging.info('this berry as an object: {}'.format(json.dumps(berry)))

        return berry

    def methods(self):
        """
        Returns a list of the class's public methods. TODO: should this be
        hardcoded for each berry type?
        """
        # List of methods not to include
        exception_list = [
            'call_handler',
            'import_handlers',
            'initialize_gpio',
            'methods',
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
        self._handlers = importlib.import_module('berry.client._handlers')

    def reload_handlers(self):
        """
        Reloads the berry's handlers from client/handlers.
        """
        new_handlers = importlib.reload(self._handlers)
        self._handlers = new_handlers

    def call_handler(self, name, *args, **kwargs):
        """
        Wrapper method to call a given handler.
        """
        # Instantiate RemoteBerries
        remote_berries = remote.RemoteBerries()

        # Get the handler function from the berry.client.handlers module
        handler = getattr(self._handlers, name)

        if not handler:
            # TODO: make this a more specific exception? Or leave it as a
            # KeyError?
            raise Exception

        # Call the handler, passing in the RemoteBerries instance and any
        # other arguments
        try:
            return handler(remote_berries, *args, **kwargs)
        except Exception:
            # If there was an exception running the handler, bail out
            return None

    def load_handler_code(self):
        """
        Returns the handler code in client/handlers.py. Used for code editing.
        """
        with open(BERRY_HANDLERS_PATH, 'r') as f:
            code = f.read()

        return code

    def update_handler_code(self, code):
        """
        Updates the handler code in client/handlers.py. Used for code editing.
        """
        temp_path = BERRY_HANDLERS_TMP_PATH
        dest_path = BERRY_HANDLERS_PATH

        # Write out to the temp copy
        with open(temp_path, 'w') as f:
            f.write(code)

        # Make sure it worked
        with open(temp_path, 'r') as f:
            disk_code = f.read()

        if code != disk_code:
            logging.error('Code written to disk doesn\'t match, try again')
            return

        # Move the temp copy over the real copy
        shutil.copy(temp_path, dest_path)
        os.remove(temp_path)

        logging.info('Code updated, now reloading handlers')
        self.reload_handlers()

    def get_berry_name(self):
        """
        Reads in the berry name from client/berry_name.txt and returns it.
        """
        with open(BERRY_NAME_PATH, 'r') as f:
            name = f.read()

        self.name = name.strip()

        return self.name

    def save_berry_name(self, name):
        """
        Saves the name to client/berry_name.txt.
        """
        self.name = name

        with open(BERRY_NAME_PATH, 'w') as f:
            f.write(self.name)
