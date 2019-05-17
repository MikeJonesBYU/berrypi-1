"""
Distance sensor class, for VL6180X. Each stub method calls the appropriate
function in the handlers module (so that we can reload the module dynamically
and update code).
"""
import logging

from ..berrybase import BerryBase


class BerryDistance(BerryBase):
    _sensor = None

    # Used for internal testing (in mm)
    _test_state = 15

    def __init__(self, **kwargs):
        kwargs['berry_type'] = 'distance'

        super().__init__(**kwargs)

    def _initialize_hardware(self):
        """
        Initializes the widget hardware.
        """
        # Import
        try:
            import board
            import busio
            import adafruit_vl6180x
        except Exception as ex:
            logging.error(
                '\n   *** ERROR importing Adafruit libraries: {}'.format(
                    ex,
                ),
            )

            # Things failed, so we must be running locally, not on a widget;
            # don't bother hooking up the VL6180X
            return

        # Initialize I2C and VL6180X
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self._sensor = adafruit_vl6180x.VL6180X(i2c)
        except Exception as ex:
            logging.error(
                '\n   *** ERROR initializing I2C/LSM303: {}'.format(ex),
            )

    def range(self):
        """
        Part of distance sensor API. Returns range in mm.
        """
        if self.live:
            return self._sensor.range

        return self._test_state

    def range_status(self):
        """
        Part of distance sensor API. Returns range status.
        """
        if self.live:
            return self._sensor.range_status

        return 0
