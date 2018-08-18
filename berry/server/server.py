"""
Berry server class.
"""
import json
import socket
import threading

from .. import utilities
from ..utilities import d


class ThreadedServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsocket.bind(('', utilities.__initialization_port__))
        self.sock.bind((self.host, self.port))

        # Start up a separate thread to listen for broadcasts from new berries.
        threading.Thread(target=self.listen_for_new_berries).start()

    def listen_for_new_berries(self):
        while True:
            data = self.udpsocket.recv(256)
            message = data.decode('utf-8')
            d.dprint(f'Received via UDP: {message}')

            threading.Thread(
                target=self.communicate_with_new_berry,
                args=(data,)
            ).start()

    def communicate_with_new_berry(self, data):
        berry_info = json.loads(data.decode('utf-8'))

        d.dprint('berry name is ' + berry_info['name'])

        # Open a TCP connection and send my address.
        response = {'ip_address': utilities.get_my_ip_address()}

        utilities.send_with_tcp(
            json.dumps(response),
            berry_info['ip_address'],
            utilities.__initialization_port__,
        )

    def listen(self):
        self.sock.listen(256)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)

            threading.Thread(
                target=self.listen_to_client,
                args=(client, address),
            ).start()

    def listen_to_client(self, client, address):
        size = 64
        d.dprint('someone is connecting:')

        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    print('received: ' + data.decode('utf-8'))
                    response = data
                else:
                    print('client at ' + address.__str__() + ' closed')
                    client.close()
                    break
            except Exception as e:
                print('Exception: {} ({})'.format(e, type(e)))
                client.close()
                return False

        print('out of receive loop')

        return response
