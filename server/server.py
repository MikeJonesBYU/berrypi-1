import socket
import threading
import utilities
from utilities import d

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(256)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 64
        d.print ("someone is connecting:")
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    print ("received: "+ data.decode("utf-8") )
                    response = data
                else:
                    print ("client at "+ address.__str__() + " closed")
                    client.close()
                    break
            except Exception as e:
                print ("some kind of excceptoin")
                print (type(e))
                client.close()
                return False
        print ("out of receive loop")


if __name__ == "__main__":
    while True:
        port_num = utilities.__port_number__
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    print ("starting server on port "+ port_num.__str__())
    ThreadedServer('',port_num).listen()