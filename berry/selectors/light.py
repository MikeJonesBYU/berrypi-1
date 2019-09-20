"""
Light selection class, using TSL2561.
"""
import logging

from .base import SelectBase, SELECTION_DELAY_COUNT


LIGHT_CHANGE_RATE_THRESHOLD = 2

LIGHT_NUMBER_VALUES = 40

# How long to wait between sensor checks
INITIAL_LIGHT_SENSOR_DELAY = 0.1
LIGHT_SENSOR_DELAY = 0.1


class LightSelect(SelectBase):

    def setup(self):
        logging.info('Setting up light selector')
        super().setup()

    def loop(self):
        """
        Light sensor loop. Watches the TSL2561 lux value and, if it jumps by
        a great enough threshold, initiates the berry-selected message.
        """
        logging.info('Entering light selection loop')

        try:
            import board
            import busio
            import adafruit_tsl2561
            import time

            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_tsl2561.TSL2561(i2c)
            count = 0

            # Get initial reading by first waiting a bit (so we ignore the
            # useless initial value), then gathering the initial set of values
            # and averaging them together
            time.sleep(1)
            lux_readings = []
            for i in range(0, LIGHT_NUMBER_VALUES):
                lux_readings.insert(0, sensor.lux)
                time.sleep(INITIAL_LIGHT_SENSOR_DELAY)

            average_lux = sum([l for l in lux_readings if l is not None]) / float(LIGHT_NUMBER_VALUES)

            while True:
                lux = sensor.lux

                if lux is not None:
                    # Check if we're above threshold and if so, send the message
                    change_rate = lux / average_lux
                    if (
                        change_rate > LIGHT_CHANGE_RATE_THRESHOLD
                        and
                        count == 0
                    ):
                        self.select()

                        # Don't keep sending select messages until after the
                        # selection delay is over (decrement this each pass through
                        # the loop)
                        count = SELECTION_DELAY_COUNT

                    # Update the average
                    # TODO: make this more elegant
                    lux_readings.insert(0, lux)
                    lux_readings.pop()
                    average_lux = sum([l for l in lux_readings if l is not None]) / float(LIGHT_NUMBER_VALUES)

                # Wait
                time.sleep(LIGHT_SENSOR_DELAY)

                # Delay count
                if count > 0:
                    count -= 1
        except Exception as ex:
            logging.error(
                '\n   *** ERROR, light sensor thread died: {}'.format(
                    ex,
                ),
            )
