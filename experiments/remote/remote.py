"""
RemoteBerries and BerryProps classes, used to reference remote berries in
client code.
"""


class ClientTest():
    def __init__(self):
        self.code = {}

    def call_remote_command(self, key, payload=None):
        if key in self.code:
            self.code[key](payload)


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
        if attr.startswith('_'):
            return super().getattr(attr)

        # walk me through this one mdj.  what's the _client?
        # the _ prefix means "this is an attribute for the local class and souldn't
        # be forwarded on to hte server"?  mdj
        # _client is the code to communiate with the server and gets passed around to the different
        # parts of the code here mdj
        print('get remote', attr)
        return self.BerryProps(attr, self._client)

    class BerryProps(object):
        """
        Class for handling method/property-level attribute access.
        """
        _name = None
        _client = None

        # is _name the variable name or the name of that type of berry?
        # I would guess variable name mdj.
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
            if attr.startswith('_'):
                return super().getattr(attr)

            # I'm really verbose so I would have put in a command name,
            # but so far I can parse your commands. mdj
            message = {
                'berry': self._name,
                'attribute': attr,
            }

            print('get props, {}, sending message to server'.format(attr), message)

            return self

        def __setattr__(self, attr, value):
            """
            Sends a message to the server with the referenced values.

            Handles usages like:

                berries.button_berry.on_press = my_func
            """
            if attr.startswith('_'):
                return super().__setattr__(attr, value)

            message = {
                'berry': self._name,
                'attribute': attr,
                'payload': value,
            }

            # If value is a callable, stash it for later reference and don't
            # send it to the server
            if callable(value):
                # Save a reference to the code so we can call it when the
                # event is triggered
                # what does the f do here? mdj
                key = f'{self._name}|{attr}'
                self._client.code[key] = value

                # Remove the callable from the payload, since we can't
                # serialize it into JSON, and instead send the key
                message['payload'] = None
                message['code-key'] = key

            print('set props, {}, to {}, sending message to server'.format(attr, value), message)
            print('code', self._client.code)

        def __call__(self):
            """
            Handles method calls on remote berries. We don't need to do
            anything here because we already handled things in __getattr__.
            """
            pass


client = ClientTest()
berries = RemoteBerries(client)


# for testing I assume? or default functions implemented by all berries? mdj
def my_func(payload):
    print('in my_func')
    if 'number' in payload:
        print('number', payload['number'])


print('berries.button_berry.on_press = my_func')
berries.button_berry.on_press = my_func

print('\nberries.led_berry.on()')
berries.led_berry.on()

print('\nberries.light_sensor.lux')
print(berries.light_sensor.lux)

print('\nberries.light_sensor.lux = 50')
berries.light_sensor.lux = 50

print('\nclient.call_remote_command')
payload = {
    'number': 499,
}
client.call_remote_command('button_berry|on_press', payload)
