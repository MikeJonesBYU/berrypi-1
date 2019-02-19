import time


def setup(global_state, remote, widget):
    # Run whenever the client code is loaded. Optional.
    pass


def loop(global_state, remote, widget):
    # Looped over in its own thread. Use for widget logic if needed.
    time.sleep(1)


def on_global_state_change(global_state, remote, widget):
    # Called whenever the state is updated
    pass


def on_press(global_state, remote, widget):
    # Called when the button is pressed
    pass


def on_release(global_state, remote, widget):
    # Called when the button is released
    pass
