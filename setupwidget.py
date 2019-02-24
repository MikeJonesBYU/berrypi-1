#!/usr/bin/env python
"""
Script to easily set up (or reset) a widgetj.
"""
import shutil
import sys

src_path = 'berry/berries/SLUG_handlers.py'
dest_path = 'berry/client/_handlers.py'

sample_config = 'berry/client/_widget_config_sample.py'
output_config = 'berry/client/_widget_config.py'

widget_name_file = 'berry/client/_widget_name.txt'

setup_path = 'widget.cfg'

###############################################################################

num = None

if len(sys.argv) >= 2:
    # Use command-line parameters

    # Get the slug
    slug = sys.argv[1]

    # Get the number, if present
    if len(sys.argv) >= 3:
        num = sys.argv[2]
else:
    # Try to use config, otherwise print usage
    try:
        with open(setup_path, 'r') as f:
            lines = f.readlines()

        slug = lines[0].strip()

        if len(lines) > 1:
            num = lines[1].strip()

    except FileNotFoundError:
        print('Usage: python3 setupwidget.py [TYPE] [NUM]')
        print('Types: button | led | fsr | accelerometer | speaker | screen')
        sys.exit(-1)

###############################################################################

src_path = src_path.replace('SLUG', slug)

# Prep the widget name (with optional number)
widget_name = slug
if num is not None:
    widget_name += str(num)

print('Setting up widget: {}'.format(widget_name))

###############################################################################

# First, copy the handler sample over
print('Clearing out handlers')

try:
    shutil.copyfile(src_path, dest_path)
except OSError as ex:
    print('Error copying handlers: {}'.format(ex))

###############################################################################

# Then update the config (changing the class name appropriately)
print('Updating config')

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

###############################################################################

# Then update the widget name
print('Updating widget name: {}'.format(widget_name))

try:
    with open(widget_name_file, 'w') as f:
        f.write(widget_name)
except OSError as ex:
    print('Error writing widget name: {}'.format(ex))

print('Done!')
