#!/usr/bin/env python3

print("initializing")

import board
import busio
import digitalio
import time

from adafruit_rgb_display import color565
import adafruit_rgb_display.st7735 as st7735

spi = busio.SPI(clock=board.SCLK, MOSI=board.MOSI, MISO=board.MISO)

display = st7735.ST7735(
    spi,
    cs=digitalio.DigitalInOut(board.D17),
    dc=digitalio.DigitalInOut(board.D22),
    rst=digitalio.DigitalInOut(board.D27),
)

print("Starting loop")
print(dir(display.spi_device))

while True:
    print("filling black, red pixel")
    display.fill(0x7521)
    display.pixel(64, 64, 0)
    display.fill(0)

    display.pixel(120, 160, color565(255, 0, 0))

    time.sleep(2)

    print("filling blue")
    display.fill(color565(0, 0, 255))

    time.sleep(2)
