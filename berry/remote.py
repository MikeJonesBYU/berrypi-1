"""
RemoteBerries and BerryProps classes, used to reference remote berries in
client code.
"""
import json
import logging


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
        # Ignore anything that starts with an underscore
        if attr.startswith('_'):
            return super().getattr(attr)

        # walk me through this one mdj.
        # if the name doesn't exist, create it?  in __init__
        # if that's the case, how does the getattr get called after the init?
        # if the name does exist, get it?  in __getattr__

        # [bmc] The __init__ just attaches the client (the widget) so that we
        # can send a message to the server later on.
        # [bmc] __getattr__ gets called whenever the name is accessed, whether
        # or not it exists (so remote.jefopwjfpowej gets called the same as
        # remote.ledwidget). What we do is take the name (`attr`) and create a
        # new BerryProps instance that knows about that name and has a ref to
        # the client. The name is just a string and isn't "created" in any real
        # sense.
        return self.BerryProps(attr, self._client)

    # need a better name here.  mdj.
    # [bmc] Agreed, definitely. RemoteInner? RemoteProperty? RemoteWidgetProps?
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
            # Ignore anything that starts with an underscore
            if attr.startswith('_'):
                return super().getattr(attr)

            # Make sure response list key exists
            key = '{}|{}'.format(self._name, attr)
            self._client.create_response_key(key)

            # Prep the remote command message
            message = {
                'command': 'remote-command',
                'destination': self._name,
                'source': self._client._berry.name,
                'attribute': attr,
                'key': key,
            }

            # Send it to the server
            self._client.send_message_to_server(message=message)

            # Now keep checking the responses dictionary until we get something
            response = self._client.get_response(key)

            # Wrap our response in an empty function so that it can be callable
            # by the user code (otherwise it'll die)
            # mdj walk me through this...
            # [bmc] In remote.ledwidget.on(), the `on` object needs to be a
            # callable, otherwise the () part will cause it to die. If we just
            # returned the response itself, we wouldn't be returning a callable,
            # and it would die. So we return a function that (on being called)
            # returns the response (via a closure).
            def response_wrapper():
                return response

            return response_wrapper

        def __setattr__(self, attr, value):
            """
            Sends a message to the server with the referenced values.

            Handles usages like:

                berries.button_berry.on_press = my_func
            """
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
                logging.info('Callable used in setattr')

                # Save a reference to the code so we can call it when the
                # event is triggered
                key = '{}|{}'.format(self._name, attr)
                logging.info('Key: {}'.format(key))

                self._client.set_code(key, value)
                logging.info('Saved code')
                logging.info(self._client.get_code(key))

                # Remove the callable from the payload, since we can't
                # serialize it into JSON, and instead send the key
                message['payload'] = None
                message['code-key'] = key

                logging.info('message')
                logging.info(message)

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
