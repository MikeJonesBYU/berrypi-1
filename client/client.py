import socket
import utilities
from utilities import d
from BerryBase import BerryBase
from uuid import getnode
import json

server_ip_address = '255.255.255.255'

def find_a_server (berry):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    asJson = berry.convertToJSON()
    d.dprint("sending via udp broadcast...\n" + asJson)
    sock.sendto(asJson.encode('utf-8'), ('255.255.255.255', utilities.__initialization_port__))
    sock.close()
    # wait for a tcp connection from the server.
    response = utilities.BlockingRecieveFromTCP(utilities.__initialization_port__)
    serverResponse = json.loads(response)
    server_ip_address = serverResponse['ipaddress']
    d.dprint("server is at "+ server_ip_address)


if __name__ == "__main__":
    # listen for a reply on the same port.  tcp for replies.
    thisBerry = BerryBase("button","left_button", utilities.getMyGUID())
    fas = find_a_server(thisBerry)


    #sock.connect((utilities.__server_address__, utilities.__port_number__))
    #sock.send(b'hello over there ')