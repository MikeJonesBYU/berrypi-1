import socket
from uuid import getnode
import json

# only at the beginning, the server adddress gets updated on start.
__server_address__ = " "
__port_number__ = 1234
__initialization_port__ = 4321
__verbose__ = True
__testing_without_gpio_pins__ = True


# the point here is that we have a code completion
# to make sure we used the same strings on both sides
# of the conversation.
tokens = {'command': 'cmd',
           'sender address': 'myip',
          'get table':'gettable',
          'new table': 'newtable'}


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

def setServerAddress (ipaddr):
    global __server_address__
    __server_address__ = ipaddr

def sendObjWithTCP (object, recv_address, port):
    message = json.dumps(object)
    sendWithTCP(message,recv_address,port)

def sendObjToServerWithTCP (object):
    sendObjWithTCP(object,__server_address__,__port_number__)

def sendToServerTCP (message):
    sendWithTCP(message, __server_address__,__port_number__)

def blocking_recieve_from_server_TCP ():
    return BlockingRecieveFromTCP(__port_number__)

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
    return message, address[0]

class d:
    @staticmethod
    def dprint (message):
        if (__verbose__):
            print (message)
