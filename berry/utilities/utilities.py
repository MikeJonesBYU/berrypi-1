import socket

# The port to listen on via UDP for registrations
REGISTRATION_PORT = 5555

# The port to run the server on
SERVER_PORT = 4444

# Whether to log everything
VERBOSE = True


def get_my_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))

    ip_address = s.getsockname()[0]

    s.close()

    return ip_address


def send_with_tcp(message, recv_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((recv_address, port))

    s.send(message.encode('utf-8'))

    d.dprint('sent: ' + message)
    d.dprint('to  : ' + recv_address + ':' + port.__str__())

    s.close()


def blocking_receive_from_tcp(port):
    d.dprint('waiting to receive on port ' + port.__str__())

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.bind(('', port))
    tcpsock.listen(1)

    client, address = tcpsock.accept()
    client.settimeout(60)

    d.dprint('someone is connecting')

    message = ''
    while True:
        try:
            data = client.recv(512)
            if data:
                # Set the response to echo back the recieved data
                message += data.decode('utf-8')
            else:
                print(f'client at {address} closed')
                client.close()
                tcpsock.close()
                break
        except Exception as e:
            print('Exception: {} ({})'.format(e, type(e)))
            client.close()
            return False

    print(f'received: {message}')
    print(f'from    : {address}:{port}')

    return message


class d:
    @staticmethod
    def dprint(message):
        if (VERBOSE):
            print(message)
