"""
Client script. Intended solely for testing.
"""
import logging
import sys
import threading
from uuid import getnode

from berry.client import BerryClient
from berry.utilities import CLIENT_PORT, LOG_LEVEL


logging.getLogger().setLevel(LOG_LEVEL)


if __name__ == '__main__':
    # Get the port number to run this client on
    try:
        port = int(sys.argv[1])
    except:
        # Default port
        port = 6666

    # Create GUID
    guid = getnode().__str__() + str(port)

    # Set up berry
    from berry.berries import BerryButton
    berry = BerryButton(
        berry_type='button',
        name='other_berry',
        guid=guid,
    )

    # Initialize the client
    client = BerryClient(berry=berry, port=port)

    # Start debug input mode thread
    threading.Thread(target=client.input_loop).start()

    # Start thread to watch lux value
    threading.Thread(target=client.light_loop).start()

    # Listen for a reply on the same port. TCP for replies.
    response = client.find_a_server()

    # Client loop (waiting for events or incoming messages)
    while True:
        # Blocking wait for incoming TCP messages
        message = client.wait_for_message()

        # And process the message
        client.process_message(message=message)