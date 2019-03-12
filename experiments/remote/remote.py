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

        # [bmc] This isn't the real code, but it looks like you figured it out.
        # (This was the early experiment for it.)
        # [bmc] That said, _client is a reference to the BerryClient instance
        # (see berry/client/client.py) that runs the widget.
        # [bmc] _ is a Python convention that means "this is private to this
        # class", but yes, we also exclude any underscored properties from
        # being passed through the remote system, otherwise we wouldn't be able
        # to use _client.
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
        # [bmc] It's the widget name (e.g., button1), and yeah, I still need to
        # go in and rename all the "berry" stuff to be "widget"
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
            # [bmc] Ignore this; berry/remote.py has the real code (which does
            # have a command name)
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
                # [bmc] It's a Python 3.6+ format string, where you can use
                # Python expressions inside curly brackets for string
                # interpolation
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
# [bmc] Ignore, this was just my initial experiment to make sure the remote
# stuff worked before I put it into berry/remote.py
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
