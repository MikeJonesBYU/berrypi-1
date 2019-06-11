"""
Client script. Intended solely for testing.
"""
import logging
import sys
import threading
from uuid import getnode

#from berry.client import BerryClient
from berry.client_for_testing import BerryClient
from berry.utilities import LOG_LEVEL
from berry.utilities import FIXED_SERVER_IP_ADDRESS
from berry.utilities import SERVER_PORT

logging.getLogger().setLevel(LOG_LEVEL)


if __name__ == '__main__':
    # Get the port number to run this client on
    # I believe this port is unique to a berry.  It's the
    # port this specific berry users to listen for messages from
    # the server -- mdj 5/20
    try:
        port = int(sys.argv[1])
    except:
        # Default port
        port = 6666

    # Create GUID
    guid = getnode().__str__() + str(port)

    # Set up berry
    from berry import berries
    berry = berries.BerryButton(
        live=False,
        guid=guid,
        path='berry/client_for_testing',
        import_path='berry.client_for_testing._handlers_sample',
    )

    # Initialize the client
    client = BerryClient(berry=berry, port=port)



    # Start debug input mode thread
    threading.Thread(target=client.input_loop).start()

    # Start thread to watch lux value
    if berry.live:
        threading.Thread(target=client.light_loop).start()

    # Listen for a reply on the same port. TCP for replies.
    # response, tcpsock = client.find_a_server()
    response, tcpsock = client.use_this_server(FIXED_SERVER_IP_ADDRESS)
    client.send_code()
    # Client loop (waiting for events or incoming messages)
    while True:
        # Blocking wait for incoming TCP messages
        message, tcpsock = client.wait_for_message(tcpsock)

        # And process the message
        client.process_message(message=message)
