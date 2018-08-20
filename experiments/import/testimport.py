#!/usr/bin/env python

import importlib
import os


def get_modules():
    modules = []

    with os.scandir('handlers') as it:
        for entry in it:
            if not entry.is_file():
                continue

            if entry.name.startswith('.') or entry.name.startswith('__'):
                continue

            modules.append(entry.name.replace('.py', ''))

    return modules


handlers = {}

# Import modules
for mod in get_modules():
    module_name = f'handlers.{mod}'
    handlers[mod] = importlib.import_module(module_name)

handlers['on_press'].on_press()
handlers['on_release'].on_release()
