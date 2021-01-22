import socket
import struct

from petalo_daq.network.petalo_network import MESSAGE

from petalo_daq.network.commands import commands     as cmd
from petalo_daq.network.commands import status_codes as status
from petalo_daq.network.command_utils import encode_register_address
from petalo_daq.network.command_utils import encode_error_value

def build_connection_success_response():
    """
    Create a connection success response command

    Returns:
    bytearray: Connection success command.
    """
    message = MESSAGE()
    data = message({'command': cmd.CON_STATUS,
                    'L1_id'  : 0,
                    'params' : [status.STA_CONNECTION_ACCEPT.value]})
    return data


def build_connection_failure_response(petalo_server, addr):
    """
    Create a connection failure response command

    If there is already a client connected, the server rejects new connections.
    In the response is included the IP address of the first client.

    Parameters:
    petalo_server (PetaloMockServer): Running server
    addr (tuple): address obtain from the socket

    Returns:
    bytearray: Connection failure command with the connected IP
    """
    message = MESSAGE()
    addr_hex = socket.inet_aton(addr[0])
    addr_int = int.from_bytes(addr_hex, 'big')
    data = message({'command' : cmd.CON_STATUS,
                    'L1_id'   : 0,
                    'params'  : [status.STA_CONNECTION_REJECT.value,
                                 addr_int]})
    return data


def build_sw_register_write_response(daq_id, register_group, register_id, error_code):
    """
    Create a SW register write response

    If there is no error, error_code should be None

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Software Register Group identifier, check DAQ docs
    register_id    (int): Software Register identifier, chech DAQ docs
    error_code     (int): Error code if needed (32 bits), otherwise None

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    value = encode_register_address(register_group, register_id)

    if error_code:
        value = encode_error_value(error_code)

    message = MESSAGE()
    m = message({'command': cmd.SOFT_REG_W_r,
                 'L1_id'  : daq_id,
                 'params' : [value]})
    return m


def build_hw_register_write_response(daq_id, register_group, register_id, error_code):
    """
    Create a HW register write response

    If there is no error, error_code should be None

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Software Register Group identifier, check DAQ docs
    register_id    (int): Software Register identifier, chech DAQ docs
    error_code     (int): Error code if needed (32 bits), otherwise None

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    value = encode_register_address(register_group, register_id)
    if error_code:
        value = encode_error_value(error_code)

    message = MESSAGE()
    m = message({'command': cmd.HARD_REG_W_r,
                 'L1_id'  : daq_id,
                 'params' : [value]})
    return m


def build_sw_register_read_response(daq_id, register_group, register_id, value, error_code):
    """
    Create a SW register read response

    If there is no error, error_code should be None

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Software Register Group identifier, check DAQ docs
    register_id    (int): Software Register identifier, chech DAQ docs
    value          (int): 32 bit value with the value read
    error_code     (int): Error code if needed (32 bits), otherwise None

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    address = encode_register_address(register_group, register_id)

    params = [address, value]
    if error_code:
        error = encode_error_value(error_code)
        params = [error, 0]

    message = MESSAGE()
    m = message({'command': cmd.SOFT_REG_R_r,
                 'L1_id'  : daq_id,
                 'params' : params})
    return m


def build_hw_register_read_response(daq_id, register_group, register_id, value, error_code):
    """
    Create a HW register read response

    If there is no error, error_code should be None

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Software Register Group identifier, check DAQ docs
    register_id    (int): Software Register identifier, chech DAQ docs
    value          (int): 32 bit value with the value read
    error_code     (int): Error code if needed (32 bits), otherwise None

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    address = encode_register_address(register_group, register_id)

    params = [address, value]
    if error_code:
        error = encode_error_value(error_code)
        params = [error, 0]

    message = MESSAGE()
    m = message({'command': cmd.HARD_REG_R_r,
                 'L1_id'  : daq_id,
                 'params' : params})
    return m
