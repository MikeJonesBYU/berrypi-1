"""
Accelerometer class, for LSM303. Each stub method calls the appropriate
function in the handlers module (so that we can reload the module dynamically
and update code).
"""
import logging
import math

from ..berrybase import BerryBase


class BerryAccelerometer(BerryBase):
    _sensor = None

    # Used for internal testing
    _test_state = (0.5, -0.2, 0.7)

    def __init__(self, **kwargs):
        kwargs['berry_type'] = 'accelerometer'

        super().__init__(**kwargs)

    def _initialize_hardware(self):
        """
        Initializes the widget hardware.
        """
        # Import
        try:
            import board
            import busio
            import adafruit_lsm303
        except Exception as ex:
            logging.error('Error importing Adafruit libraries: {}'.format(ex))

            # Things failed, so we must be running locally, not on a widget;
            # don't bother hooking up the LSM303
            return

        # Initialize I2C and LSM303
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self._sensor = adafruit_lsm303.LSM303(i2c)
        except Exception as ex:
            logging.error('Error initializing I2C/LSM303: {}'.format(ex))

    def _mag(self, tup):
        """
        Calculates magnitude of a three-part tuple.
        """
        return math.sqrt(pow(tup[0], 2) + pow(tup[1], 2) + pow(tup[2], 2))

    def magnitude(self):
        """
        Part of accelerometer API. Returns magnitude of accelerometer reading.
        """
        if self.live:
            return self._mag(self.acceleration())

        return self._mag(self._test_state)

    def raw_magnitude(self):
        """
        Part of accelerometer API. Returns magnitude of raw accelerometer
        reading.
        """
        if self.live:
            return self._mag(self.raw_acceleration())

        return self._mag(self._test_state)

    def _dir(self, tup):
        """
        Calculates predominant direction of a three-part tuple.
        """
        abs_x = abs(tup[0])
        abs_y = abs(tup[1])
        abs_z = abs(tup[2])
        dir = 'x'
        max_abs = abs_x
        i = 0

        if abs_y > max_abs:
            dir = 'y'
            i = 1

        if abs_z > max_abs:
            dir = 'z'
            i = 2

        return '{}{}'.format(dir, '+' if tup[i] >= 0 else '-')

    def direction(self):
        """
        Part of accelerometer API. Returns 'x+', 'x-', 'y+', 'y-', 'z+', or
        'z-' based on the predominant direction of the accelerometer reading.
        """
        if self.live:
            return self._dir(self.acceleration())

        return self._dir(self._test_state)

    def acceleration(self):
        """
        Part of accelerometer API. Returns value of accelerometer reading.
        """
        if self.live:
            return self._sensor.acceleration

        return self._test_state

    def raw_acceleration(self):
        """
        Part of accelerometer API. Returns raw value of accelerometer reading.
        """
        if self.live:
            return self._sensor.raw_acceleration

        return self._test_state

    def x(self):
        """
        Part of accelerometer API. Returns x value of accelerometer reading.
        """
        if self.live:
            x, _, _ = self.acceleration()
            return x

        return self._test_state[0]

    def raw_x(self):
        """
        Part of accelerometer API. Returns raw x value of accelerometer reading.
        """
        if self.live:
            raw_x, _, _ = self.raw_acceleration()
            return raw_x

        return self._test_state[0]

    def y(self):
        """
        Part of accelerometer API. Returns x value of accelerometer reading.
        """
        if self.live:
            y, _, _ = self.acceleration()
            return y

        return self._test_state[1]

    def raw_y(self):
        """
        Part of accelerometer API. Returns raw x value of accelerometer reading.
        """
        if self.live:
            raw_y, _, _ = self.raw_acceleration()
            return raw_y

        return self._test_state[1]

    def z(self):
        """
        Part of accelerometer API. Returns x value of accelerometer reading.
        """
        if self.live:
            z, _, _ = self.acceleration()
            return z

        return self._test_state[2]

    def raw_z(self):
        """
        Part of accelerometer API. Returns raw x value of accelerometer reading.
        """
        if self.live:
            raw_z, _, _ = self.raw_acceleration()
            return raw_z

        return self._test_state[2]
