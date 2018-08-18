"""
BerryBase class used as a base class for berries.
"""
import json
import types

from . import utilities
from .utilities import d

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
            d.dprint(f'invalid type to berry constructor {type}')
            self.berry_type = 'invalid'

        self.name = name
        self.guid = guid
        self.ip_address = utilities.get_my_ip_address()

    def _as_json(self):
        """
        Serializes the berry to JSON.
        """
        berry = {
            'guid': self.guid,
            'name': self.name,
            'type': self.berry_type,
            'ip': self.ip_address,
            'methods': self.methods(),
        }

        d.dprint(f'this berry as an object: {json.dumps(berry)}')

        return berry

    def _has_user_interrupts(self):
        return self.berry_type in HAS_USER_INTERRUPTS

    def methods(self):
        """
        Returns a list of the class's public methods.
        """
        return [
            f
            for f in dir(self)
            if (
                f[0] != '_'
                and
                f != 'methods'
                and
                isinstance(getattr(self, f), types.MethodType)
            )
        ]
