"""
Package home, including BerryBase class.
"""
import json

from . import utilities
from .utilities import d

BERRY_TYPES = ['button', 'slider', 'led']
HAS_USER_INTERRUPTS = ['button', 'slider']


class BerryBase():
    berry_type = 'none'
    name = 'none'
    guid = 'none'
    ipaddress = 'none'

    def __init__(self, berry_type, name, guid):
        if berry_type in BERRY_TYPES:
            self.berry_type = berry_type
        else:
            d.dprint(f'invalid type to berry constructor {type}')
            self.berry_type = 'invalid'

        self.name = name
        self.guid = guid
        self.ipaddress = utilities.get_my_ip_address()

    def convert_to_json(self):
        berry = {
            'guid': self.guid,
            'name': self.name,
            'type': self.berry_type,
            'ipaddress': self.ipaddress,
        }

        output = json.dumps(berry)
        d.dprint(f'this berry as an object: {output}')

        return output

    def has_user_interrupts(self):
        return self.berry_type in HAS_USER_INTERRUPTS
