#!/usr/bin/env python3

from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

# Camera warmup time
time.sleep(2)

camera.capture('test.jpg')
 
