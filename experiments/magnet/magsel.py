#!/usr/bin/env python3

print("initializing")

import time
import board
import busio

import adafruit_lsm303


MAG_CHANGE_RATE_THRESHOLD = 2

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm303.LSM303(i2c)

# Get initial reading by first waiting two seconds (so we ignore
# the useless initial value) and then watch for 600ms (200ms three
# times) and average the values together
print("waiting")
time.sleep(2) 
mag_readings = []
for i in range(0, 3):
    mag_readings.insert(0, sensor.magnetic)
    time.sleep(0.2)

average_x = sum([r[0] for r in mag_readings]) / 3.0
average_y = sum([r[1] for r in mag_readings]) / 3.0
average_z = sum([r[2] for r in mag_readings]) / 3.0


print("starting loop")
while True:
    mag = sensor.magnetic

    try:
        change_rate_x = mag[0] / average_x
    except Exception:
        change_rate_x = 0

    try:
        change_rate_y = mag[1] / average_y
    except Exception:
        change_rate_y = 0

    try:
        change_rate_z = mag[2] / average_z
    except Exception:
        change_rate_z = 0

    # Check if we're above threshold and if so, send the message
    if (
        abs(change_rate_x) > MAG_CHANGE_RATE_THRESHOLD
        or
        abs(change_rate_y) > MAG_CHANGE_RATE_THRESHOLD
        or
        abs(change_rate_z) > MAG_CHANGE_RATE_THRESHOLD
    ):
        print("\nselected!")
        print(change_rate_x, change_rate_y, change_rate_z, "threshold", MAG_CHANGE_RATE_THRESHOLD)

    # Update the average
    # TODO: make this more elegant
    mag_readings.insert(0, mag)
    mag_readings.pop()

    average_x = sum([r[0] for r in mag_readings]) / 3.0
    average_y = sum([r[1] for r in mag_readings]) / 3.0
    average_z = sum([r[2] for r in mag_readings]) / 3.0

    # Wait 100ms
    time.sleep(0.1)
