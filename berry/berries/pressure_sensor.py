"""
Pressure sensor class. Each stub method calls the appropriate function in the
handlers module (so that we can reload the module dynamically and update code).
"""
from ..berrybase import BerryBase


class BerryPressureSensor(BerryBase):
    _sensor = None
    _divisor = 200   # TODO: replace this with a real number 
    _test_pressure = 50  # Used for internal testing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers.
        """
        # Import
        try:
            from gpiozero import Pressure
        except:
            # Things failed, must be running locally, not on a berry, so don't
            # bother initializing GPIO
            return

        # Hook up to gpiozero, using pin GP17
        self._sensor = Pressure(17)

    def _scale(self, value):
        return value / self._divisor

    def pressure(self):
        """
        Part of pressure API. Returns a number with the raw pressure.
        """
        if self.live:
            return self._sensor.pressure()

        # For testing
        return self._test_pressure

    def scaled_pressure(self):
        """
        Part of pressure API. Returns a number with the scaled pressure (0–1).
        """
        return self._scale(self.pressure())
