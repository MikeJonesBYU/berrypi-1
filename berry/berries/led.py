"""
LED class.
"""
import logging

from ..berrybase import BerryBase


class BerryLED(BerryBase):
    _led = None
    _test_state = False  # For internal testing

    def __init__(self, **kwargs):
        kwargs['berry_type'] = 'led'

        super().__init__(**kwargs)

    def _initialize_hardware(self):
        """
        Initializes the widget hardware.
        """
        # Import
        try:
            from gpiozero import LED
        except Exception as ex:
            logging.error('Error importing gpiozero: {}'.format(ex))

            # Things failed, must be running locally, not on a widget, so don't
            # bother initializing GPIO
            return

        # Hook up to gpiozero, using pin GP17
        try:
            self._led = LED(17)
        except Exception as ex:
            logging.error('Error initializing LED: {}'.format(ex))

    def is_lit(self):
        """
        Part of LED API. Returns True or False depending on whether the LED
        is lit.
        """
        if self.live:
            return self._led.is_lit

        # For testing
        return self._test_state

    def off(self):
        """
        Wrapper for the LED's off() function. Returns nothing.
        """
        logging.info('Turning LED off')

        if self.live:
            self._led.off()

        # For testing
        self._test_state = False

    def on(self):
        """
        Wrapper for the LED's on() function. Returns nothing.
        """
        logging.info('Turning LED on')

        if self.live:
            self._led.on()

        # For testing
        self._test_state = True

    def toggle(self):
        """
        Wrapper for the LED's toggle() function. Returns nothing.
        """
        logging.info('Toggling LED')

        if self.live:
            self._led.toggle()

        # For testing
        self._test_state = not self._test_state
