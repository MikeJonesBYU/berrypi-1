"""
Screen class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
import logging

from ..berrybase import BerryBase


class BerryScreen(BerryBase):
    _canvas = None

    def __init__(self, **kwargs):
        kwargs['berry_type'] = 'screen'

        super().__init__(**kwargs)

    def _initialize_hardware(self):
        """
        Initializes the widget hardware.
        """
        # Import
        try:
            from luma.core.interface.serial import i2c
            from luma.core.render import canvas
            from luma.oled.device import ssd1306
        except Exception as ex:
            logging.error('\n   *** ERROR importing Luma: {}'.format(ex))

            # Things failed, must be running locally, not on a widget, so don't
            # bother initializing I2C
            return

        # Now initialize I2C
        try:
            serial = i2c(port=1, address=0x3C)
            device = ssd1306(serial)
        except Exception as ex:
            logging.error(
                '\n   *** ERROR initializing I2C/SSD1306: {}'.format(
                    ex,
                ),
            )

            return

        self._canvas = canvas(device)

    def point(self, xy, fill=None):
        """
        Draws a point. See the PIL ImageDraw reference for details.
        """
        with self._canvas as draw:
            draw.point(xy, fill)

    def line(self, xy, fill=None, width=1):
        """
        Draws a line. See the PIL ImageDraw reference for details.
        """
        with self._canvas as draw:
            draw.line(xy, fill, width)

    def rectangle(self, xy, fill=None, outline=None):
        """
        Draws a rectangle. See the PIL ImageDraw reference for details.
        """
        with self._canvas as draw:
            draw.rectangle(xy, fill, outline)

    def ellipse(self, xy, fill=None, outline=None):
        """
        Draws an ellipse. See the PIL ImageDraw reference for details.
        """
        with self._canvas as draw:
            draw.ellipse(xy, fill, outline)

    def text(self, xy, text, fill=None):
        """
        Draws text. See the PIL ImageDraw reference for details.
        """
        with self._canvas as draw:
            draw.text(xy, text, fill)
