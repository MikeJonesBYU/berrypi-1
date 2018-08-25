"""
Button class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
from gpiozero import Button

from ..berrybase import BerryBase


class BerryButton(BerryBase):
    _button = None

    def __init__(self):
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
