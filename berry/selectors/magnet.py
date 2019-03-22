"""
Magnet selection class, using LSM303.
"""
import logging

from .base import SelectBase


MAG_CHANGE_RATE_THRESHOLD = 2

# How long to wait between sensor checks
INITIAL_MAGNET_SENSOR_DELAY = 0.1
MAGNET_SENSOR_DELAY = 0.1


class MagnetSelect(SelectBase):

    def setup(self):
        logging.info('Setting up magnet selector')
        super().setup()

    def loop(self):
        """
        Magnet sensor loop. Watches the LSM303 magnetometer values and, if they
        jump by a great enough threshold, initiates the berry-selected message.
        """
        logging.info('Entering magnet selection loop')

        try:
            import board
            import busio
            import time
            import adafruit_lsm303

            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_lsm303.LSM303(i2c)
            count = 0

            # Get initial reading by first waiting two seconds (so we ignore
            # the useless initial value) and then watch for 600ms (200ms three
            # times) and average the values together
            time.sleep(1)
            mag_readings = []
            for i in range(0, 3):
                mag_readings.insert(0, sensor.magnetic)
                time.sleep(INITIAL_MAGNET_SENSOR_DELAY)

            average_x = sum([r[0] for r in mag_readings]) / 3.0
            average_y = sum([r[1] for r in mag_readings]) / 3.0
            average_z = sum([r[2] for r in mag_readings]) / 3.0

            while True:
                mag = sensor.magnetic

                if mag is not None:
                    # Check if we're above threshold and if so, send the message
                    try:
                        change_rate_x = abs(mag[0] / average_x)
                    except Exception:
                        change_rate_x = 0

                    try:
                        change_rate_y = abs(mag[1] / average_y)
                    except Exception:
                        change_rate_y = 0

                    try:
                        change_rate_z = abs(mag[2] / average_z)
                    except Exception:
                        change_rate_z = 0

                    if (
                        change_rate_x > MAG_CHANGE_RATE_THRESHOLD
                        or
                        change_rate_y > MAG_CHANGE_RATE_THRESHOLD
                        or
                        change_rate_z > MAG_CHANGE_RATE_THRESHOLD
                    ) and count == 0:
                        self.select()

                        # Don't keep sending select messages until after the
                        # selection delay is over (decrement this each pass through
                        # the loop)
                        count = SELECTION_DELAY_COUNT

                    # Update the average
                    # TODO: make this more elegant
                    mag_readings.insert(0, mag)
                    mag_readings.pop()

                    average_x = sum([r[0] for r in mag_readings]) / 3.0
                    average_y = sum([r[1] for r in mag_readings]) / 3.0
                    average_z = sum([r[2] for r in mag_readings]) / 3.0

                # Wait
                time.sleep(MAGNET_SENSOR_DELAY)

                # Delay count
                if count > 0:
                    count -= 1
        except Exception as ex:
            logging.error(
                '\n   *** ERROR, magnet sensor thread died: {}'.format(
                    ex,
                ),
            )
