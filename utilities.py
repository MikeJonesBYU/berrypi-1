import socket
from uuid import getnode

__server_address__ = 'localhost' #'10.24.66.223'
__port_number__ = 1234
__initialization_port__ = 4321
__verbose__ = True


def getMyIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipaddress = s.getsockname()[0]
    s.close()
    return ipaddress

def getMyGUID () :
    return getnode().__str__()

def sendWithTCP (message, recvAddress, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((recvAddress, port))
    s.send(message.encode("utf-8"))
    d.dprint("sent: " + message)
    d.dprint("to  : " + recvAddress + ":" + port.__str__())
    s.close()

def BlockingRecieveFromTCP (port):
    d.dprint("waiting to receive on port " + port.__str__())
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.bind(('', port))
    tcpsock.listen(1)
    client, address = tcpsock.accept()
    client.settimeout(60)
    d.dprint("someone is connecting " + address.__str__())
    message = " "
    while True:
        try:
            data = client.recv(512)
            if data:
                # Set the response to echo back the recieved data
                message = data
            else:
                print("client at " + address.__str__() + " closed")
                client.close()
                tcpsock.close()
                break
        except Exception as e:
            print("some kind of excceptoin on receive")
            print(type(e))
            client.close()
            return False
    d.dprint ("received : " + message.decode("utf-8"))
    d.dprint ("from     : " + address.__str__() + ":"+port.__str__())
    return (message)

class d:
    @staticmethod
    def dprint (message):
        if (__verbose__):
            print (message)
