"""
Pressure sensor handlers

To initialize a new pressure sensor widget, copy this file to
berry/client/_handlers.py and delete this line.

"""
import time


def setup(state, remote, berry):
    """
    Run whenever the client code is loaded. Optional.
    """
    # -------------------------------------
    # Fill in your code here
    print('Setup')
    # -------------------------------------


def loop(state, remote, berry):
    """
    If present, looped over in its own thread. Use for widget logic where
    needed.
    """
    # -------------------------------------
    # Fill in your code here
    print('Looping')
    time.sleep(1)
    # -------------------------------------


def on_state(state, remote, berry):
    """
    Handler called whenever state is updated.
    """
    # -------------------------------------
    # Fill in your code here
    print('State')
    # val = state.get('value')
    # print('on_state, val = {}'.format(val))
    # -------------------------------------
