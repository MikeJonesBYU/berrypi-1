import socket
import threading
import utilities
from utilities import d
from utilities import tokens
import json

class ThreadedServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udpsocket.bind ((' ',utilities.__initialization_port__))
#        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        # starting up a seperate thread to listen for broadcasts from new berries.
        threading.Thread(target=self.listenForNewBerries).start()

    def listenForNewBerries(self):
        while True:
            data= self.udpsocket.recv(256)
            message = data.decode("utf-8")
            d.dprint("recieved via udp "+ message)
            threading.Thread(target=self.communicateWithNewBerry,args=(data,)).start()


    def communicateWithNewBerry (self,data):
        berryInfo = json.loads(data.decode("utf-8"))
        # open a tcp connection and send my address.
        responseObject = {'ipaddress': utilities.getMyIPAddress()}
        utilities.sendWithTCP (json.dumps(responseObject),berryInfo['ipaddress'],utilities.__initialization_port__)

    def listen(self):
        self.sock.listen(256)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 64
        d.dprint ("someone is connecting:")
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
        self.process_message (response)

    def process_message (self,messageJSON):
        message = json.loads(messageJSON)
        command = message[tokens['command']]
        d.dprint("processing command: "+command)
        if command == tokens['get table']:
            # send over the table.
            d.dprint("... it was a request for the table.  SEnding")
            self.send_berry_table(message[tokens['sender address']])
        else:
            d.dprint("not sure what command that was")

    def send_berry_table(self,targetIP):
        table_message_object = {tokens['command'] : tokens['new table']}
        utilities.sendObjWithTCP(table_message_object,targetIP,utilities.__port_number__)
        # done.

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