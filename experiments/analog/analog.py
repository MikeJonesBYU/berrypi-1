#!/usr/bin/env python3

import time

from gpiozero import MCP3008

pot = MCP3008(channel=0)

while True:
    print(0.0004885197850512668 / pot.value)
    time.sleep(0.1)
