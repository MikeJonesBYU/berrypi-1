#!/usr/bin/env python3

import time

from gpiozero import MCP3008

divisor = 0.0004885197850512668
divisor = 0.005
pot = MCP3008(channel=0)

time.sleep(1)
readings = []
for i in range(0, 10):
    readings.insert(0, pot.value)
    time.sleep(0.05)

average_force = sum(r for r in readings) / 10.0

while True:
    readings.insert(0, pot.value)
    readings.pop()

    average_force = sum(r for r in readings) / 10.0
    scaled_force = divisor / average_force

    print(round(scaled_force, 1))
    time.sleep(0.1)
