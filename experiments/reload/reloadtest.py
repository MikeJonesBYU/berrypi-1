#!/usr/bin/env python

import importlib

handler = importlib.import_module('handlers.on_press')

handler.on_press()

with open('handlers/on_press.py', 'r') as f:
    data = f.read()

data = data.replace('apple', 'orange')

with open('handlers/on_press.py', 'w') as f:
    f.write(data)

handler = importlib.reload(handler)

handler.on_press()
