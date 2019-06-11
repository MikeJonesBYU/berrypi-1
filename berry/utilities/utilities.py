"""
Utility functions.
"""
import logging
import socket

# The port to listen on via UDP for registrations
REGISTRATION_PORT = 5555

# The default client port
CLIENT_PORT = 24601

# If the client sends a message to ther server via tcp it will
# be on this port. todo: check if that's true.
SERVER_PORT = 8080

# if we are going hardcoded server, use this ip address.
FIXED_SERVER_IP_ADDRESS = "10.37.50.105"

# How much to log
LOG_LEVEL = logging.DEBUG
# LOG_LEVEL = logging.ERROR


def get_my_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))

    ip_address = s.getsockname()[0]

    s.close()

    return ip_address


def send_with_tcp(message, recv_address, port):
    # logging.info('sending to {} on port {}'.format(recv_address,port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((recv_address, port))

    s.send(message.encode('utf-8'))

    logging.info('Sent: {}'.format(message))
    logging.info('To: {}:{}'.format(recv_address, port))

    s.close()


def blocking_receive_from_tcp(port, tcpsock=None):
    logging.info('Waiting to receive on port {}'.format(port))

    if tcpsock is None:
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind(('', port))
        tcpsock.listen(1)

    client, address = tcpsock.accept()
    client.settimeout(60)

    logging.info('Someone is connecting')

    message = ''
    while True:
        try:
            data = client.recv(500000)

            if data:
                message += data.decode('utf-8')
                break
            else:
                logging.info('Client at {} closed'.format(address))
                client.close()
                # tcpsock.close()
                break
        except Exception as e:
            logging.error('Exception: {} ({})'.format(e, type(e)))
            client.close()
            return False, tcpsock

    logging.info('Received: {}'.format(message))
    logging.info('From:     {}:{}'.format(address, port))

    return message, tcpsock
