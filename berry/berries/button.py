"""
Button class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
from ..berrybase import BerryBase


class BerryButton(BerryBase):
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
