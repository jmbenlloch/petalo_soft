import threading
import sys
import socket
import logging
from time import sleep

# absolute imports to execute as standalone program
from petalo_daq.network.petalo_network import MESSAGE
from petalo_daq.network.commands       import commands     as cmd

from petalo_daq.mock_server                  import server_data
from petalo_daq.mock_server.binary_responses import build_connection_success_response
from petalo_daq.mock_server.binary_responses import build_connection_failure_response
from petalo_daq.mock_server.server_commands  import read_sw_register
from petalo_daq.mock_server.server_commands  import read_hw_register
from petalo_daq.mock_server.server_commands  import write_sw_register
from petalo_daq.mock_server.server_commands  import write_hw_register


class PetaloMockServer():
    """
    Class to define a virtual Petalo server. To be used in testing functions.
    The expected behaviour should be similar to that of a real DAQ card.
    """

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 9116
        self.clients = {} # Initialize client list as an empty list
        self.sw_registers = server_data.sw_registers # DAQ SW registers
        self.hw_registers = server_data.hw_registers # DAQ HW registers

        # Configure logger to stdout
        self.logger = logging.getLogger('daq_server')
        fh = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(fh)
        self.logger.info("Running DAQ mock server")

    def run(self):
        s = socket.socket()         # Create a socket object
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))        # Bind to the port
        s.listen(5)                 # Now wait for client connection.

        self.logger.info('Server started!')
        self.logger.info('Waiting for clients...')

        while True:
           c, addr = s.accept()     # Establish connection with client.

           self.clients[addr] = True
           self.logger.debug(''.format(self.clients))
           self.logger.info ('Got connection from {}'.format(addr))

           threading.Thread(target=on_new_client,
                            args=(c, addr, self),
                           ).start()
        s.close()


def on_new_client(clientsocket,addr, petalo_server):
    # No more than one client at the same time
    if len(petalo_server.clients) > 1:
        connect_response = build_connection_failure_response(petalo_server, addr)
        one_client = False
    else:
        connect_response = build_connection_success_response()
        one_client = True

    clientsocket.send(connect_response)
    message = MESSAGE()

    while True and one_client:
        # Run until 0xfafafafa is recieved from the client
        try:
            msg = clientsocket.recv(1024)
            petalo_server.logger.debug("msg: {}".format(msg))
        except ConnectionResetError:
            print("ConnectionResetError")
            break

        if msg:
            if msg == b'\xfa\xfa\xfa\xfa': #keyword to disconnect
                break


            data = message(msg)
            petalo_server.logger.debug('{}'.format(data))

            cmd_functions = {
                cmd.SOFT_REG_W: write_sw_register,
                cmd.HARD_REG_W: write_hw_register,
                cmd.SOFT_REG_R: read_sw_register,
                cmd.HARD_REG_R: read_hw_register,
            }

            fn = cmd_functions[data['command']]
            response = fn(petalo_server, data['L1_id'], data['params'])
            clientsocket.send(response)

        sleep(0.2)

    clientsocket.close()
    petalo_server.logger.debug("socket closed")
    if addr in petalo_server.clients:
        del petalo_server.clients[addr]
        petalo_server.logger.debug("client {} removed".format(addr))
        petalo_server.logger.debug("client list: {}".format(petalo_server.clients))


if __name__ == '__main__':
    petalo_server = PetaloMockServer()
    petalo_server.logger.setLevel(level=logging.DEBUG)
    petalo_server.run()
