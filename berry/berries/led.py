"""
LED class.
"""
import logging

from ..berrybase import BerryBase


class BerryLED(BerryBase):
    _led = None
    _gpio = False  # Whether we're using GPIO (vs. testing locally)
    _test_state = False  # For internal testing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._gpio = False

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers.
        """
        # Import
        try:
            from gpiozero import LED
            self._gpio = True
        except:
            # Things failed, must be running locally, not on a berry, so don't
            # bother initializing GPIO
            return

        # Hook up to gpiozero, using pin GP17
        self._led = LED(17)

    def is_lit(self):
        """
        Part of LED API. Returns True or False depending on whether the LED
        is lit.
        """
        if self._gpio:
            return self._led.is_lit

        # For testing
        return self._test_state

    def off(self):
        """
        Wrapper for the LED's off() function. Returns nothing.
        """
        logging.info('Turning LED off')

        self._led.off()

        # For testing
        self._test_state = False

    def on(self):
        """
        Wrapper for the LED's on() function. Returns nothing.
        """
        logging.info('Turning LED on')

        self._led.on()

        # For testing
        self._test_state = True

    def toggle(self):
        """
        Wrapper for the LED's toggle() function. Returns nothing.
        """
        logging.info('Toggling LED')

        self._led.toggle()

        # For testing
        self._test_state = not self._test_state
