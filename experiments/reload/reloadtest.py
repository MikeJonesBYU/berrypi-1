#!/usr/bin/env python

import importlib

import handlers.on_press

handlers.on_press.on_press()

with open('handlers/on_press.py', 'r') as f:
    data = f.read()

data = data.replace('apple', 'orange')

with open('handlers/on_press.py', 'w') as f:
    f.write(data)

importlib.reload(handlers.on_press)

handlers.on_press.on_press()
