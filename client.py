"""
Client script.
"""
from uuid import getnode

from berry import client, BerryBase


if __name__ == '__main__':
    # Listen for a reply on the same port. TCP for replies.
    this_berry = BerryBase('button', 'left_button', getnode().__str__())
    fas = client.find_a_server(this_berry)
