"""
RemoteBerries and BerryProps classes, used to reference remote berries in
client code.
"""


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
            # Ignore anything that starts with an underscore
            if attr.startswith('_'):
                return super().getattr(attr)

            # Prep the remote command message
            message = {
                'command': 'remote-command',
                'berry': self._name,
                'attribute': attr,
            }

            self._client.send_message_to_server(message=message)

            return self

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
                'berry': self._name,
                'attribute': attr,
                'payload': value,
            }

            # TODO: if value is a callable, handle it differently
            if callable(value):
                pass
                # Save a reference to the code so we can call it when the
                # event is triggered
                # self._client.

            self._client.send_message_to_server(message=message)

        def __call__(self):
            """
            Handles method calls on remote berries. We don't need to do
            anything here because we already handled things in __getattr__.
            """
            pass
