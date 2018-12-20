#!/usr/bin/env/python

import subprocess


def beep(freq=1400, duration=0.2):
    subprocess.run(
        ['play', '-b', '16', '-q', '-n', 'synth', str(duration), 'sin', str(freq)],
        stderr=None,
        env={'AUDIODEV': 'hw:1'},
    )


beep()

beep(freq=2400, duration=0.4)

beep(freq=2000, duration=0.2)
beep(freq=1800, duration=0.2)
beep(freq=1600, duration=0.2)
beep(freq=1400, duration=1)
