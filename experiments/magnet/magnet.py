#!/usr/bin/env python3
import time
import board
import busio

import adafruit_lsm303

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm303.LSM303(i2c)

while True:
        raw_mag_x, raw_mag_y, raw_mag_z = sensor.raw_magnetic
        mag_x, mag_y, mag_z = sensor.magnetic
        print('Magnetometer raw: ({0:6d}, {1:6d}, {2:6d}), (gauss): ({3:10.3f}, {4:10.3f}, {5:10.3f})'.format(raw_mag_x, raw_mag_y, raw_mag_z, mag_x, mag_y, mag_z))

        # raw_accel_x, raw_accel_y, raw_accel_z = sensor.raw_acceleration
        # accel_x, accel_y, accel_z = sensor.acceleration

        # print('Acceleration raw: ({0:6d}, {1:6d}, {2:6d}), (m/s^2): ({3:10.3f}, {4:10.3f}, {5:10.3f})'.format(raw_accel_x, raw_accel_y, raw_accel_z, accel_x, accel_y, accel_z))

        time.sleep(0.1)
