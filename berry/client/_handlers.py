"""
Button handlers

Name: led_button

"""
import logging

from .client import send_message_to_server


def on_press(remote):
    """
    Handler called when the button is pressed. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('Button pressed, now turning on LED')

    remote.led_berry.on()


def on_release(remote):
    """
    Handler called when the button is released. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('Button released, now turning off LED')

    remote.led_berry.off()


def on_test(remote):
    """
    Test handler.
    """
    print("In test handler")

    print('remote.other_berry.test_attr')
    foo = remote.other_berry.test_attr
    print(foo)
