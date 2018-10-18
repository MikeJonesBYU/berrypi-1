"""
RemoteBerries and BerryProps classes, used to reference remote berries in
client code.
"""
import json


class RemoteBerries(object):
    """
    Parent class. Example usage:

        berries = RemoteBerries(client)

        berries.button_berry.on_press = my_func
        berries.led_berry.on()

        if berries.light_sensor.lux > 200:
            print('Things are bright')
    """
    _client = None

    def __init__(self, client):
        self._client = client

    def __getattr__(self, attr):
        """
        Returns a BerryProps instance for the referenced berry (since any
        attribute access at this level is for a berry).
        """
        print('remote', attr)
        # Ignore anything that starts with an underscore
        if attr.startswith('_'):
            return super().getattr(attr)

        return self.BerryProps(attr, self._client)

    class BerryProps(object):
        """
        Class for handling method/property-level attribute access.
        """
        _name = None
        _client = None

        def __init__(self, berry_name, client):
            self._name = berry_name
            self._client = client

        def __getattr__(self, attr):
            """
            Sends a message to the server with the referenced values.

            Handles usages like:

                berries.led_berry.on()

                if berries.light_sensor.lux > 200:
                    pass:
            """
            print('props', attr)
            # Ignore anything that starts with an underscore
            if attr.startswith('_'):
                return super().getattr(attr)

            # Prep the remote command message
            message = {
                'command': 'remote-command',
                'destination': self._name,
                'source': self._client._berry.name,
                'attribute': attr,
            }
            print('sending message', message)
            print('client', self._client)

            # Send it to the server
            self._client.send_message_to_server(message=message)

            # Now wait for a response
            # TODO: figure out how to ignore other possible messages that the
            # client may receive here
            message = self._client.wait_for_message()

            return self.parse_response_message(message)

        def __setattr__(self, attr, value):
            """
            Sends a message to the server with the referenced values.

            Handles usages like:

                berries.button_berry.on_press = my_func
            """
            print('props', attr)
            # Ignore anything that starts with an underscore
            if attr.startswith('_'):
                return super().__setattr__(attr, value)

            message = {
                'command': 'remote-command',
                'destination': self._name,
                'source': self._client._berry.name,
                'attribute': attr,
                'payload': value,
            }

            # If value is a callable, stash it for later reference and don't
            # send it (the value) to the server
            if callable(value):
                # Save a reference to the code so we can call it when the
                # event is triggered
                key = '{}|{}'.format(self._name, attr)
                self._client.code[key] = value

                # Remove the callable from the payload, since we can't
                # serialize it into JSON, and instead send the key
                message['payload'] = None
                message['code-key'] = key

            print('sending message setattr', message)
            print('client', self._client)

            # Send it to the server
            self._client.send_message_to_server(message=message)

        def __call__(self):
            """
            Handles method calls on remote berries. We don't need to do
            anything here because we already handled things in __getattr__.
            """
            pass

        def parse_response_message(self, message):
            """
            Parses a response message and returns the actual response.
            """
            response = json.loads(message)

            if 'payload' in response:
                return response['payload']

            return None
