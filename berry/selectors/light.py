"""
Light selection class, using TSL2561.
"""
import logging

from .base import SelectBase


LIGHT_CHANGE_RATE_THRESHOLD = 4

# How long to wait between sensor checks
INITIAL_LIGHT_SENSOR_DELAY = 0.1
LIGHT_SENSOR_DELAY = 0.1


class LightSelect(SelectBase):

    # No need to override setup(), since it already starts the thread

    def loop(self):
        """
        Light sensor loop. Watches the TSL2561 lux value and, if it jumps by
        a great enough threshold, initiates the berry-selected message.
        """
        logging.info('looping light now')

        try:
            import board
            import busio
            import adafruit_tsl2561
            import time

            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_tsl2561.TSL2561(i2c)
            count = 0

            # Get initial reading by first waiting two seconds (so we ignore
            # the useless initial value) and then watch for 600ms (200ms three
            # times) and average the values together
            time.sleep(1)
            lux_readings = []
            for i in range(0, 3):
                lux_readings.insert(0, sensor.lux)
                time.sleep(INITIAL_LIGHT_SENSOR_DELAY)

            average_lux = sum(lux_readings) / 3.0

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
                    average_lux = sum(lux_readings) / 3.0

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
