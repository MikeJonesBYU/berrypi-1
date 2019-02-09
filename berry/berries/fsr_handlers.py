import time


def setup(state, remote, widget):
    # Run whenever the client code is loaded. Optional.
    pass


def loop(state, remote, widget):
    # Looped over in its own thread. Use for widget logic if needed.
    time.sleep(1)


def on_statechange(state, remote, widget):
    # Called whenever the state is updated
    val = state.get('value')
    print(val)
