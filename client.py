"""
Client script.
"""
import logging
import sys
import threading
from uuid import getnode

from berry.client import BerryClient, get_berry
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
    berry = get_berry(guid=guid)

    # Initialize the client
    client = BerryClient(berry=berry, port=port)

    # Start debug input mode thread
    threading.Thread(target=client.input_loop).start()

    # Start main loop thread (loop() handler)
    t = threading.Thread(target=client.main_loop).start()
    client._loop_thread = t

    # Start threads for sensors
    if berry.live:
        # Start light loop thread
        threading.Thread(target=client.light_loop).start()

        # Start magnet loop thread
        threading.Thread(target=client.magnet_loop).start()

    # Listen for a reply on the same port. TCP for replies.
    response = client.find_a_server()

    # Client loop (waiting for events or incoming messages)
    while True:
        # Blocking wait for incoming TCP messages
        message = client.wait_for_message()

        # And process the message
        client.process_message(message=message)
