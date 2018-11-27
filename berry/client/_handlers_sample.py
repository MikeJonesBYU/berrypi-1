"""
Client handlers.
"""
import logging
import time

from .client import send_message_to_server


def on_press(state, remote):
    """
    Handler called when the button is pressed. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('Button pressed, now turning on LED')

    remote.led_berry.off()


def on_release(state, remote):
    """
    Handler called when the button is released. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('Button released, now turning off LED')

    remote.led_berry.on()


def setup(state, remote):
    """
    Run whenever the client code is loaded. Optional.
    """
    logging.info('setup')


def loop(state, remote):
    """
    If present, looped over in its own thread. Use for widget logic where
    needed.
    """
    logging.info('looping')
    time.sleep(1)


def on_state(state, remote):
    """
    Handler called whenever state is updated.
    """
    val = state.get('value')
    logging.info('on_state, val = {}'.format(val))
