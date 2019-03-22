"""
SelectBase class used as a base class for selection methods.
"""
import logging
import threading


# How long to wait (in cycles) after a selection before the user can make
# another selection of this widget
SELECTION_DELAY_COUNT = 25


class SelectBase():
    def __init__(self, widget):
        self._widget = widget

    def setup(self):
        """
        Starts the loop thread. Can be overridden to not do this (for buttons).
        """
        threading.Thread(target=self.loop).start()

    def loop(self):
        """
        Overridden by child class.
        """
        pass

    def select(self):
        """
        Used by child classes to select the widget.
        """
        self._widget.send_berry_selected_message()
