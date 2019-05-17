#!/usr/bin/env python

print("initializing")

import board
import busio
import adafruit_ssd1306 as ssd1306
import time


spi = busio.SPI(clock=board.SCLK, MOSI=board.MOSI, MISO=board.MISO)


display = ssd1306.SSD1306_SPI(
    width=128,
    height=64,
    spi=spi,
    cs=digitalio.DigitalInOut(board.CE0),
    dc=digitalio.DigitalInOut(board.D27),
    rst=digitalio.DigitalInOut(board.D17),
)

print("Starting loop")


display.fill(0)
display.show()

time.sleep(1)

display.pixel(0, 0, 1)
display.pixel(64, 16, 1)
display.pixel(127, 31, 1)
display.show()
