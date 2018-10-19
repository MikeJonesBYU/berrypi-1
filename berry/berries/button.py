"""
Button class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
import logging

from ..berrybase import BerryBase


class BerryButton(BerryBase):
    _button = None
    _gpio = False  # Whether we're using GPIO (vs. testing locally)
    _test_state = False  # Used for internal testing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._gpio = False

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers.
        """
        # Import
        try:
            from gpiozero import Button
            self._gpio = True
        except:
            # Things failed, must be running locally, not on a berry, so don't
            # bother initializing GPIO
            return

        # Hook up to gpiozero, using pin GP17
        self._button = Button(17)

        # Hook in handlers
        self._button.when_pressed = self.on_press
        self._button.when_released = self.on_release

    def is_pressed(self):
        """
        Part of button API. Returns True or False depending on whether the
        button is pressed.
        """
        if self._gpio:
            return self._button.is_pressed

        # For testing
        return self._test_state

    def on_press(self):
        """
        Stub for the on_press handler. Activated when the button is pressed.
        Returns nothing.
        """
        logging.info('Button on press')

        self.call_handler('on_press')

        # For testing
        self._test_state = True

    def on_release(self):
        """
        Stub for the on_release handler. Activated when the button is released.
        Returns nothing.
        """
        logging.info('Button on release')

        self.call_handler('on_release')

        # For testing
        self._test_state = False
