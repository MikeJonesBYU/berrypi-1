import socket
import utilities
from utilities import d
from utilities import tokens
import json
from button import button
from button_internals import button_internals


def find_a_server ():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = json.dumps({'ipaddress':utilities.getMyIPAddress()});
    d.dprint("sending via udp broadcast...\n" + message)
    sock.sendto(message.encode('utf-8'), ('255.255.255.255', utilities.__initialization_port__))
    sock.close()
    # wait for a tcp connection from the server.
    response,senderIP = utilities.BlockingRecieveFromTCP(utilities.__initialization_port__)
    d.dprint ("response from server "+response.__str__())
    return senderIP


def beWhatYouAre (berrySoul):
    # load up the internals class and get that going.
    # spin off a thread that waits for interrupts on the pin.
    # i'm a button.
    me = button()
    if utilities.__testing_without_gpio_pins__:
        # wait for a keypress.
        test = input("type something in: ")
        # send it on.
        me.onPressed()
    else:
        # do proper gpio stuffs
        pass

def get_berry_list_from_server ():
    d.dprint("requesting berry table from server")
    command = {tokens['command']: tokens['get table'],
               tokens['sender address']: utilities.getMyIPAddress()}
    utilities.sendObjToServerWithTCP(command)
    tableJSON = utilities.blocking_recieve_from_server_TCP()
    d.dprint("got this table: \n"+tableJSON.decode("utf-8"))
    return "not a table yet :)"



if __name__ == "__main__":
    # listen for a reply on the same port.  tcp for replies.
    internal_button = button_internals.__init__("button","left_button",utilities.getMyGUID())
    utilities.__server_address__ = find_a_server()
    # great, now get the table of known berries.
    berry_list = get_berry_list_from_server ()
    # and initialize the local proxies for the remote berries.
    # and now set up the local berry to respond to interrupts.
    beWhatYouAre (internal_button)

    #sock.connect((utilities.__server_address__, utilities.__port_number__))
    #sock.send(b'hello over there ')
