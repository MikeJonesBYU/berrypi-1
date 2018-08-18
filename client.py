"""
Client script.
"""
import sys
from uuid import getnode

from berry import client
from berry.berries import BerryButton


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python client.py PORT')
        sys.exit(-1)

    port = sys.argv[1]

    # Test berry
    this_berry = BerryButton(
        berry_type='button',
        name='left_button',
        guid=getnode().__str__(),
    )

    # Listen for a reply on the same port. TCP for replies.
    response = client.find_a_server(berry=this_berry, port=port)

    # TODO: Import handlers? Or does this happen somewhere else?

    # Run the server
    while True:
        # Wait for incoming TCP messages
        message = client.wait_for_message(port=port)

        # And process the message
        client.process_message(
            message=message,
            berry=this_berry,
            port=port,
        )
