"""
FSR class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
from ..berrybase import BerryBase

import threading
import time


class BerryFSR(BerryBase):
    _sensor = None
    _divisor = 0.005
    _sampling_rate = 0.1  # 100ms
    _test_force = 0.5  # Used for internal testing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._average_force = 0.001

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

        # Start force loop thread
        threading.Thread(target=self.force_loop).start()

    def _force_loop(self):
        """
        Thread that polls to get the current force on the FSR. Populates the
        self._average_force value.
        """
        NUM_SAMPLES = 10.0

        # Get the initial readings
        time.sleep(1)
        readings = []
        for i in range(0, int(NUM_SAMPLES)):
            readings.insert(0, self._sensor.value)
            time.sleep(self._sampling_rate)

        self._average_force = sum(r for r in readings) / NUM_SAMPLES

        # Average the readings
        while True:
            readings.insert(0, self._sensor.value)
            readings.pop()

            self._average_force = sum(r for r in readings) / NUM_SAMPLES

            time.sleep(self._sampling_rate)

    def force(self):
        """
        Part of force API. Returns a number with the scaled force (which should
        end up being between 0 and about 5 based on my testing).
        """
        return self._divisor / self._average_force

    def raw_force(self):
        """
        Part of force API. Returns a number with the raw pressure.
        """
        if self.live:
            return self._sensor.value

        # For testing
        return self._test_raw_force
