"""
BerryBase class used as a base class for berries.
"""
import importlib
import json
import logging
import os
import types

from . import utilities


BERRY_TYPES = ['button', 'slider', 'led']
HAS_USER_INTERRUPTS = ['button', 'slider']


class BerryBase():
    berry_type = 'none'
    name = 'none'
    guid = 'none'
    ip_address = 'none'

    def __init__(self, berry_type, name, guid):
        if berry_type in BERRY_TYPES:
            self.berry_type = berry_type
        else:
            logging.error('invalid type to berry constructor {}'.format(
                berry_type,
            ))
            self.berry_type = 'invalid'

        self.name = name
        self.guid = guid
        self.ip_address = utilities.get_my_ip_address()

        # Import the handlers
        self.import_handlers()

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

    def _has_user_interrupts(self):
        return self.berry_type in HAS_USER_INTERRUPTS

    def methods(self):
        """
        Returns a list of the class's public methods. TODO: should this be
        hardcoded for each berry type?
        """
        # List of methods not to include
        exception_list = [
            'methods',
            'import_handlers',
            'call_handler',
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

    def _get_modules(self):
        """
        Returns a list of all the modules in the client/handlers directory.
        Used by import_handlers().
        """
        modules = []
        files = os.scandir('berry/client/handlers')

        for entry in files:
            if not entry.is_file():
                continue

            if entry.name.startswith('.') or entry.name.startswith('__'):
                continue

            modules.append(entry.name.replace('.py', ''))

        return modules

    def import_handlers(self):
        """
        Imports the berry's handlers from client/handlers. Stashes the imported
        handlers in self._handlers, since that's how importlib works (and it
        conveniently makes it far easier to reference the imported handlers
        in the subclasses).
        """
        self._handlers = {}

        # Import modules
        for mod in self._get_modules():
            module_name = 'berry.client.handlers.{}'.format(mod)
            self._handlers[mod] = importlib.import_module(module_name)

    def call_handler(self, name, *args, **kwargs):
        """
        Wrapper method to call a given handler.
        """
        # TODO: make this a more specific exception? Or leave it as a KeyError?
        if name not in self._handlers:
            raise Exception

        # Get the handler module
        handler_mod = self._handlers[name]

        # Now get the function (same name as module)
        handler = getattr(handler_mod, name)

        # Call the handler, passing in any arguments
        return handler(*args, **kwargs)
