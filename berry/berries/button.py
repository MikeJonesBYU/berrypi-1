"""
Button class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
from ..berrybase import BerryBase


class BerryButton(BerryBase):
    _button = None

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers.
        """
        # Import
        try:
            from gpiozero import Button
            on_berry = True
        except:
            # Things failed, must be running locally, not on a berry
            on_berry = False

        # Check if we're running on a berry or not
        if on_berry:
            # Hook up to gpiozero, using pin GP17
            self._button = Button(17)

            # Hook in handlers
            self._button.when_pressed = self.on_press
            self._button.when_released = self.on_release

    def on_press(self):
        """
        Stub for the on_press handler. Activated when the button is pressed.
        Returns nothing.
        """
        self.call_handler('on_press')

    def on_release(self):
        """
        Stub for the on_release handler. Activated when the button is released.
        Returns nothing.
        """
        self.call_handler('on_release')
