"""
Client script.
"""
import sys
from uuid import getnode

from berry.client import BerryClient
from berry.berries import BerryButton


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python client.py PORT')
        sys.exit(-1)

    # Get the port number to run this client on
    try:
        port = int(sys.argv[1])
    except:
        print('Invalid port', port)
        sys.exit(-1)

    # Test berry
    this_berry = BerryButton(
        berry_type='button',
        name='left_button',
        guid=getnode().__str__(),
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
