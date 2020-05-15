"""
Button class. Each stub method calls the appropriate function in the handlers
module (so that we can reload the module dynamically and update code).
"""
import logging

from ..berrybase import BerryBase


class BerryButton(BerryBase):
    _button = None
    _test_state = False  # Used for internal testing

    def __init__(self, **kwargs):
        kwargs['berry_type'] = 'button'

        super().__init__(**kwargs)

    def _initialize_hardware(self):
        """
        Initializes the widget hardware.
        """
        # Import
        try:
            from gpiozero import Button
        except Exception as ex:
            logging.error('\n   *** ERROR importing gpiozero: {}'.format(ex))

            # Things failed, must be running locally, not on a widget, so don't
            # bother initializing GPIO
            return

        # Hook up to gpiozero, using pin GP17
        try:
            self._button = Button(17)

            # Hook in handlers
            self._button.when_pressed = self.on_press
            self._button.when_released = self.on_release
        except Exception as ex:
            logging.error('\n   *** ERROR initializing button: {}'.format(ex))

        self._initialize_id_led()

    def is_pressed(self):
        """
        Part of button API. Returns True or False depending on whether the
        button is pressed.
        """
        if self.live:
            return self._button.is_pressed

        # For testing
        return self._test_state

    def on_press(self):
        """
        Stub for the on_press handler. Activated when the button is pressed.
        Returns nothing.
        """
        logging.info('Button on press')

        # Call the user handler if it exists
        self.call_handler('on_press')

        # Send event message to server (for any registered clients)
        message = {
            'command': 'event',
            'event': 'on_press',
            'name': self.name,
        }
        self.send_message_to_server(message)

        # For testing
        self._test_state = True

    def on_release(self):
        """
        Stub for the on_release handler. Activated when the button is released.
        Returns nothing.
        """
        logging.info('Button on release')

        # Call the user handler if it exists
        self.call_handler('on_release')

        # Send event message to server (for any registered clients)
        message = {
            'command': 'event',
            'event': 'on_release',
            'name': self.name,
        }
        self.send_message_to_server(message)

        # For testing
        self._test_state = False

    def wipe_handlers(self):
        """
        Unhooks any user handlers so that reloading works as expected.
        """
        if self.live:
            self._button.when_pressed = None
            self._button.when_released = None
