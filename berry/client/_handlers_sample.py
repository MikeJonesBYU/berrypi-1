"""
Client handlers.
"""
import logging
import time

from .client import send_message_to_server


def on_press(global_state, remote, berry):
    """
    Handler called when the button is pressed. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('Button pressed, now turning on LED')

    remote.led_berry.off()


def on_release(global_state, remote, berry):
    """
    Handler called when the button is released. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('Button released, now turning off LED')

    remote.led_berry.on()


def setup(global_state, remote, berry):
    """
    Run whenever the client code is loaded. Optional.
    """
    logging.info('setup')


def loop(global_state, remote, berry):
    """
    If present, looped over in its own thread. Use for widget logic where
    needed.
    """
    logging.info('looping')
    time.sleep(1)


def on_global_state_change(global_state, remote, berry):
    """
    Handler called whenever global state is updated.
    """
    val = global_state.get('value')
    logging.info('on_global_state_change, val = {}'.format(val))
