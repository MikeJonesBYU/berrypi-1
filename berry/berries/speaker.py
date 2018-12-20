"""
Speaker class.
"""
import subprocess

from ..berrybase import BerryBase


class BerrySpeaker(BerryBase):
    _led = None
    _test_state = False  # For internal testing

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize_gpio(self):
        """
        Initializes GPIO pins and handlers.
        """
        # Nothing to do
        return

    def beep(self, freq=1400, duration=0.2):
        """
        Beeps.
        """
        if self.live:
            subprocess.run(
                ['play', '-b', '16', '-q', '-n', 'synth', str(duration), 'sin', str(freq)],  # noqa
                stderr=None,
                env={'AUDIODEV': 'hw:1'},
            )
        else:
            print('Beeped (freq={}, dur={})'.format(freq, duration))
