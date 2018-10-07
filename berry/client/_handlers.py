"""
Button handlers

Name: led_button

"""
from .client import send_message_to_server


def on_press():
    """
    Handler called when the button is pressed.
    """
    print("Button 1 pressed!")

    # Send a message to the server
    send_message_to_server(
        message='button_pressed',
    )


def on_release():
    """
    Handler called when the button is released.
    """
    print("Button 1 released!")

    # Send a message to the server
    send_message_to_server(
        message='button_released',
    )
