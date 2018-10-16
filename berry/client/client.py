"""
Berry client class.
"""
import json
import logging
import socket

from .. import utilities

server_ip_address = 0

LIGHT_CHANGE_RATE_THRESHOLD = 15


class BerryClient():
    _berry = None
    _port = None
    _code = None

    def __init__(self, berry, port):
        self._berry = berry
        self._port = int(port)

        # Maps berry/event handlers to functions, for use in user code
        self._code = {}

    def find_a_server(self):
        """
        Finds server and initiates handshake.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        output = self._berry._as_json()
        output['port'] = self._port
        output = json.dumps(output)

        logging.info('Sending via udp broadcast...\n' + output)

        sock.sendto(
            output.encode('utf-8'),
            ('255.255.255.255', utilities.REGISTRATION_PORT),
        )
        sock.close()

        # Wait for a TCP connection from the server.
        response = utilities.blocking_receive_from_tcp(self._port)

        server_response = json.loads(response)

        global server_ip_address
        server_ip_address = server_response['ip']

        logging.info('Server IP is {}'.format(server_ip_address))

        return server_response

    def wait_for_message(self):
        """
        Waits for messages to come through in TCP. Part of the main client
        loop.
        """
        # Wait for a TCP connection from the server.
        return utilities.blocking_receive_from_tcp(self._port)

    def process_message(self, message):
        """
        Processes an incoming message.
        """
        message = json.loads(message)

        if 'command' not in message:
            logging.error('Error, message missing command')
            return

        command = message['command']

        if command == 'code-save':
            # Update the code
            if 'code' in message:
                self._berry.update_handler_code(message['code'])

            # And update the name
            if 'name' in message:
                self._berry.save_berry_name(message['name'])
        elif command == 'other-message':
            pass

    def input_loop(self):
        """
        Debug mode input loop. Processes keyboard input and acts accordingly.
        Make sure to hit enter after each command.

        Usage:
            e -- sends 'code-edit' message to server
        """
        while True:
            command = input('> ').strip()

            if command == 'e':
                # Edit code
                self.send_code_edit_message()
            elif command == '':
                # Allow empty input (for spacing apart output)
                pass
            else:
                print('Unrecognized input, please try again\n')

    def send_code_edit_message(self):
        """
        Sends the code edit message to the server. Used in input loop and
        light loop.
        """
        code = self._berry.load_handler_code()

        message = {
            'command': 'code-edit',
            'code': code,
            'name': self._berry.name,
            'guid': self._berry.guid,
        }

        send_message_to_server(message=message)

    def light_loop(self):
        """
        Light sensor loop. Watches the TSL2561 lux value and, if it jumps by
        a great enough threshold, initiates the code-edit message.
        """
        try:
            import board
            import busio
            import adafruit_tsl2561
            import time

            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_tsl2561.TSL2561(i2c)

            # Get initial reading by first waiting two seconds (so we ignore
            # the useless initial value) and then watch for three seconds and
            # average the values together
            time.sleep(2)
            lux_readings = []
            for i in range(0, 3):
                lux_readings.insert(0, sensor.lux)
                time.sleep(1)

            average_lux = sum(lux_readings) / 3.0

            while True:
                lux = sensor.lux

                # Check if we're above threshold and if so, send the message
                change_rate = lux / average_lux
                if change_rate > LIGHT_CHANGE_RATE_THRESHOLD:
                    self.send_code_edit_message()

                # Update the average
                # TODO: make this more elegant
                lux_readings.insert(0, lux)
                lux_readings.pop()
                average_lux = sum(lux_readings) / 3.0

                # Wait half a second (don't need to check quite so often)
                time.sleep(0.5)
        except Exception as ex:
            print('Light sensor thread died', ex)

    def call_remote_command(self, key, payload=None):
        """
        Calls a remote command, passing in an optional payload. Used by user
        code.
        """
        if key in self.code:
            self.code[key](payload)


def send_message_to_server(message):
    logging.info("Sending message to server: {}".format(message))

    utilities.send_with_tcp(
        json.dumps(message),
        server_ip_address,
        utilities.SERVER_PORT,
    )
