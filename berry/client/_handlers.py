"""
Button handlers

Name: led_button

"""
from .client import send_message_to_server


def on_press(remote):
    """
    Handler called when the button is pressed. The remote parameter gives
    access to other berries' functionality.
    """
    print("Button 1 pressed!")

    # Send a message to the server
    send_message_to_server(
        message='button_pressed',
    )


def on_release(remote):
    """
    Handler called when the button is released. The remote parameter gives
    access to other berries' functionality.
    """
    print("Button 1 released!")

    # Send a message to the server
    send_message_to_server(
        message='button_released',
    )
