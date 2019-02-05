#!/usr/bin/env python
"""
Script to easily set up (or reset) a widgetj.
"""
import shutil
import sys

if len(sys.argv) < 2:
    print('Usage: python3 setupwidget.py [TYPE]')
    print('Types: button | led | fsr | accelerometer | speaker | screen')
    sys.exit(-1)

# Get the slug
slug = sys.argv[1]
print('Setting up {} widget'.format(slug))

# First, copy the handler sample over
print('Clearing out handlers')

src_path = 'berry/berries/{}_handlers.py'.format(slug)
dest_path = 'berry/client/_handlers.py'

try:
    shutil.copyfile(src_path, dest_path)
except OSError as ex:
    print('Error copying handlers: {}'.format(ex))

# Then update the config (changing the class name appropriately)
print('Updating config')

sample_config = 'berry/client/_widget_config_sample.py'
output_config = 'berry/client/_widget_config.py'

try:
    with open(sample_config, 'r') as f:
        text = f.read()
except OSError as ex:
    print('Error reading sample config: {}'.format(ex))

replacements = {
    'button': 'Button',
    'led': 'LED',
    'fsr': 'FSR',
    'accelerometer': 'Accelerometer',
    'speaker': 'Speaker',
    'screen': 'Screen',
}

text = text.replace('BerryButton', 'Berry{}'.format(replacements[slug]))

try:
    with open(output_config, 'w') as f:
        f.write(text)
except OSError as ex:
    print('Error writing widget config: {}'.format(ex))

print('Done!')
