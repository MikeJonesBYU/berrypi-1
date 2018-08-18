"""
Client script.
"""
import sys
from uuid import getnode

from berry.client import BerryClient
from berry.berries import BerryButton
from berry.utilities import CLIENT_PORT


if __name__ == '__main__':
    # Get the port number to run this client on
    try:
        port = int(sys.argv[1])
    except:
        port = CLIENT_PORT

    # Test berry
    this_berry = BerryButton(
        berry_type='button',
        name='left_button',
        guid=getnode().__str__() + str(port),
    )

    client = BerryClient(berry=this_berry, port=port)

    # Listen for a reply on the same port. TCP for replies.
    response = client.find_a_server()

    # TODO: Import handlers? Or does this happen somewhere else?

    # Run the server
    while True:
        # Wait for incoming TCP messages
        message = client.wait_for_message()

        # And process the message
        client.process_message(message=message)
