"""
Button selection class.
"""
import logging

from .base import SelectBase


class ButtonSelect(SelectBase):

    def setup(self):
        """
        Run on initialization. Sets up button handlers.
        """
        logging.info('Setting up button selector')
        # Import
        try:
            from gpiozero import Button
        except Exception as ex:
            logging.error('\n   *** ERROR importing gpiozero: {}'.format(ex))
            return

        # Hook up to gpiozero, using pin GP22
        try:
            self._button = Button(22)

            # Hook in handler
            self._button.when_pressed = self.select
        except Exception as ex:
            logging.error('\n   *** ERROR initializing button: {}'.format(ex))

    # No need to override loop(), since we don't use it
