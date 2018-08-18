"""
Button class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
from ..berrybase import BerryBase

import berry.berries.button_handlers


class BerryButton(BerryBase):
    def on_press():
        """
        Stub for the on_press handler. Activated when the button is pressed.
        """
        button_handlers.on_press()

    def on_release():
        """
        Stub for the on_release handler. Activated when the button is released.
        """
        button_handlers.on_release()
