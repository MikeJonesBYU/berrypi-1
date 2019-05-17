import time


def setup(self, global_state, widgets):
    # Run whenever the client code is loaded. Optional.
    pass


def loop(self, global_state, widgets):
    # Looped over in its own thread. Use for widget logic if needed.
    time.sleep(1)


def on_global_state_change(self, global_state, widgets):
    # Called whenever the state is updated
    pass
