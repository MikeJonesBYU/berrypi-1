"""
LED class.
"""
from ..berrybase import BerryBase


class BerryLED(BerryBase):
    _led = None
    _gpio = False  # Whether we're using GPIO (vs. testing locally)

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

        # Testing mode, always false
        return False

    def off(self):
        """
        Wrapper for the LED's off() function. Returns nothing.
        """
        self._led.off()

    def on(self):
        """
        Wrapper for the LED's on() function. Returns nothing.
        """
        self._led.on()

    def toggle(self):
        """
        Wrapper for the LED's toggle() function. Returns nothing.
        """
        self._led.toggle()
