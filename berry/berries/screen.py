"""
Screen class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
import logging

from ..berrybase import BerryBase


class BerryScreen(BerryBase):
    _canvas = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers. (Technically this is I2C and not
        GPIO, btw.)
        """
        # Import
        try:
            from luma.core.interface.serial import i2c
            from luma.core.render import canvas
            from luma.oled.device import ssd1306

            serial = i2c(port=0)
            device = ssd1306(serial, bcm_DC=27, bcm_RST=17)

            self._canvas = canvas(device)
        except:
            # Things failed, must be running locally, not on a berry, so don't
            # bother initializing GPIO
            return

    def point(self, xy, fill=None):
        """
        Draws a point. See the PIL ImageDraw reference for details.
        """
        self._canvas.point(xy, fill)

    def line(self, xy, fill=None, width=1):
        """
        Draws a line. See the PIL ImageDraw reference for details.
        """
        self._canvas.line(xy, fill, width)

    def rectangle(self, xy, fill=None, outline=None):
        """
        Draws a rectangle. See the PIL ImageDraw reference for details.
        """
        self._canvas.rectangle(xy, fill, outline)

    def ellipse(self, xy, fill=None, outline=None):
        """
        Draws an ellipse. See the PIL ImageDraw reference for details.
        """
        self._canvas.ellipse(xy, fill, outline)

    def text(self, xy, text, fill=None):
        """
        Draws text. See the PIL ImageDraw reference for details.
        """
        self._canvas.text(xy, text, fill)
