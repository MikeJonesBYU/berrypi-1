"""
LED class.
"""
import logging

from ..berrybase import BerryBase


class BerryLED(BerryBase):
    _led = None
    _test_state = False  # For internal testing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers.
        """
        # Import
        try:
            from gpiozero import LED
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

    def on_test(self):
        """
        Stub for the dummy on_test handler.
        """
        logging.info('on_test()')

        # Call the user handler if it exists
        self.call_handler('on_test')

        # Send event message to server (for any registered clients)
        message = {
            'command': 'event',
            'event': 'on_test',
            'name': self.name,
        }
        self.send_message_to_server(message)

        # For testing
        self._test_state = False
