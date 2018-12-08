"""
FSR class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
from ..berrybase import BerryBase


class BerryFSR(BerryBase):
    _sensor = None
    _divisor = 0.0004885197850512668
    _test_force = 50  # Used for internal testing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers.
        """
        # Import
        try:
            from gpiozero import MCP3008

            self._sensor = MCP3008(channel=0)
        except:
            # Things failed, must be running locally, not on a berry, so don't
            # bother initializing GPIO
            return

    def _scale(self, value):
        return self._divisor / value

    def force(self):
        """
        Part of force API. Returns a number with the scaled force (which should
        end up being between 0 and 1 based on my testing).
        """
        return self._scale(self.force())

    def raw_force(self):
        """
        Part of force API. Returns a number with the raw pressure.
        """
        if self.live:
            return self._sensor.value

        # For testing
        return self._test_raw_force
