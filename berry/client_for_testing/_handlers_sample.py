"""
TestClient handlers.
"""
import logging
import time



def on_press(self, global_state, widgets):
    """
    Handler called when the button is pressed. The remote parameter gives
    access to other berries' functionality.
    """
    logging.info('Button pressed, now turning on LED')

    widgets.led_berry.off()


def on_release(self, global_state, widgets):
    """
    Handler called when the button is released. The remote parameter gives
    access to other berries' functionality.
    """
    log
