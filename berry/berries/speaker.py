"""
Speaker class.
"""
import logging
import subprocess

from ..berrybase import BerryBase


class BerrySpeaker(BerryBase):
    _led = None
    _test_state = False  # For internal testing

    def __init__(self, **kwargs):
        kwargs['berry_type'] = 'speaker'

        super().__init__(**kwargs)

    def _initialize_hardware(self):
        """
        Initializes the widget hardware.
        """
        # Initialize the ID LED
        self._initialize_id_led()

    def beep(self, freq=1400, duration=0.2):
        """
        Beeps.
        """
        if self.live:
            try:
                subprocess.run(
                    ['play', '-b', '16', '-q', '-n', 'synth', str(duration), 'sin', str(freq)],  # noqa
                    stderr=None,
                )
            except Exception as ex:
                logging.error('\n   *** ERROR beeping: {}'.format(ex))
        else:
            logging.info('Beeped (freq={}, dur={})'.format(freq, duration))

    def speak(self, text):
        """
        Says whatever is in text, using espeak.
        """
        try:
            if self.live:
                subprocess.run(
                    ['espeak', str(text)],
                    stderr=None,
                    env={'AUDIODEV': 'hw:1'},
                )
            else:
                subprocess.run(
                    ['say', '-v', 'Karen', str(text)],
                    stderr=None,
                    env={'AUDIODEV': 'hw:1'},
                )
        except Exception as ex:
            logging.error('\n   *** ERROR speaking: {}'.format(ex))

    def play_mp3(self, filename):
        """
        Plays a MP3.
        """
        if self.live:
            try:
                subprocess.run(
                    ['play', filename],  # noqa
                    stderr=None,
                )
            except Exception as ex:
                logging.error('\n   *** ERROR playing mp3: {}'.format(ex))
        else:
            logging.info('Played mp3 {}'.format(filename))
