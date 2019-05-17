"""
State class.
"""
import logging


class ClientState(dict):
    """
    Class for holding client state.
    """
    _state = {}

    def __init__(self, client=None):
        self._state = {}
        self._client = client

    def get(self, attr, default=None):
        """
        Returns the value for the specified key.
        """
        logging.info('get {} {}'.format(attr, self._state.get(attr, None)))

        return self._state.get(attr, default)

    def _replace_state(self, state):
        """
        Replaces the state dictionary. Called by the server.
        """
        logging.info('replace state')
        self._state = state

    def update(self, data):
        """
        Takes an update delta dictionary and sends it to the server.
        """
        logging.info('update state', data)
        self._client.update_state(data)

        # Also locally update our state so things aren't out of sync
        self._state.update(data)
