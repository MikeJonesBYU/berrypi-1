"""
Client handlers
"""
import logging
import time

def on_press(self, global_state, widgets):
    """
    Handler called when the button is pressed. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('On Press Running')


def on_release(self, global_state, widgets):
    """
    Handler called when the button is released. The remote parameter gives
    access to other berries' functionality.
    """
    widgets.my_berry.on_release
    logging.info('On Release Running')


def setup(self, global_state, widgets):
    """
    Run whenever the client code is loaded. Optional.
    """
    logging.info('setup')


def loop(self, global_state, widgets):
    """
    If present, looped over in its own thread. Use for widget logic where
    needed.
    """
    logging.info('looping')
    time.sleep(1)

def on_global_state(self, global_state, widgets):
    """
    Handler called whenever global state is updated.
    """
    val = global_state.get('value')
    logging.info('on_global_state_change, val = {}'.format(val))
