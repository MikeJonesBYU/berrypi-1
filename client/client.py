import socket
import utilities
from utilities import d
from BerryBase import BerryBase
from uuid import getnode

server_ip_address = '255.255.255.255'

def find_a_server (berry):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    asJson = berry.convertToJSON()
    d.dprint("sending...\n" + asJson)
    sock.sendto(asJson.encode('utf-8'), ('255.255.255.255', utilities.__initialization_port__))
    sock.close()
    # wait for a tcp connection from the server.
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.bind(('',utilities.__initialization_port__))
    tcpsock.listen(1)
    client,address = tcpsock.accept()
    client.settimeout(60)
    d.dprint("someone is connecting:")
    while True:
        try:
            data = client.recv(512)
            if data:
                # Set the response to echo back the recieved data
                print("received: " + data.decode("utf-8"))
                response = data
            else:
                print("client at " + address.__str__() + " closed")
                client.close()
                tcpsock.close()
                break
        except Exception as e:
            print("some kind of excceptoin")
            print(type(e))
            client.close()
            return False
    print("out of receive loop")

if __name__ == "__main__":
    # listen for a reply on the same port.  tcp for replies.
    thisBerry = BerryBase("button","left_button", getnode().__str__())
    fas = find_a_server(thisBerry)


    #sock.connect((utilities.__server_address__, utilities.__port_number__))
    #sock.send(b'hello over there ')