#!/usr/bin/env python

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

serial = spi(device=0, port=0)
device = ssd1306(serial, bcm_DC=27, bcm_RST=17)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
