#!/usr/bin/env python

import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

serial = i2c(port=1, address=0x3C)


# DIY OLED (yellow/blue)
# device = ssd1306(serial)

# while True:
#     with canvas(device) as draw:
#         draw.rectangle(device.bounding_box, outline="white", fill="black")
#         draw.text((30, 5), "It works!", fill="white")
#         draw.rectangle((50, 30, 20, 20), fill="white")
# 
#     time.sleep(0.1)


# Thin OLED

device = ssd1306(serial, width=128, height=32)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((30, 2), "Hello world", fill="white")
    draw.rectangle((10, 15, 20, 25), fill="white")

while True:
    time.sleep(0.1)
