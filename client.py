"""
Client script.
"""
import logging
import sys
import threading
from uuid import getnode

#from berry.selectors import LightSelect, MagnetSelect, ButtonSelect
from berry.selectors import LightSelect
from berry.client import BerryClient, get_widget, get_selector
from berry.utilities import CLIENT_PORT, LOG_LEVEL


logging.getLogger().setLevel(LOG_LEVEL)


if __name__ == '__main__':
    # Get the port number to run this client on
    try:
        port = int(sys.argv[1])
    except:
        # Default port
        port = CLIENT_PORT

    # Create GUID
    guid = getnode().__str__() + str(port)

    # Get berry from config
    berry = get_widget(guid=guid)

    # Initialize the client
    client = BerryClient(berry=berry, port=port)

    # Start debug input mode thread
    threading.Thread(target=client.input_loop).start()

    # Start thread for selector, if needed
    if berry.live:
        # Get selector
        selector = get_selector(client)
        selector.setup()

    # Listen for a reply on the same port. TCP for replies.
    response, tcpsock = client.find_a_server()

    # Client loop (waiting for events or incoming messages)
    while True:
        # Blocking wait for incoming TCP messages
        message, tcpsock = client.wait_for_message(tcpsock)

        # And process the message in a new thread
        threading.Thread(
            target=client.process_message,
            kwargs={ 'message': message },
        ).start()
