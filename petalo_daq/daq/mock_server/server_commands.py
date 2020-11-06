import struct

from petalo_daq.daq.commands import status_codes as status

from petalo_daq.daq.mock_server.binary_responses import build_sw_register_read_response
from petalo_daq.daq.mock_server.binary_responses import build_hw_register_read_response
from petalo_daq.daq.mock_server.binary_responses import build_sw_register_write_response
from petalo_daq.daq.mock_server.binary_responses import build_hw_register_write_response
from petalo_daq.daq.command_utils import decode_register_address


def write_register(registers, reg_group, reg_id, value):
    """
    Write value in register

    Check whether the address is valid and proper permisssions are set.

    Parameters:
    registers (dict): Dictionary with either SW or HW registers
    reg_group (int): Software Register Group identifier, check DAQ docs
    reg_id    (int): Software Register identifier, chech DAQ docs
    value     (int): Value to be written (32 bits)

    Returns:
    error_code (status_code): None if no error. Error code otherwise
    """
    error_code = None
    try:
        if registers [reg_group][reg_id]['permissions']['write']:
            registers[reg_group][reg_id]['value'] = value
        else:
            error_code = status.ERR_READ_ONLY
    except KeyError:
        error_code = status.ERR_INVALID_REGISTER

    return error_code


def read_register(registers, reg_group, reg_id):
    """
    Read value from register

    Check whether the address is valid and proper permisssions are set.

    Parameters:
    registers (dict): Dictionary with either SW or HW registers
    reg_group (int): Software Register Group identifier, check DAQ docs
    reg_id    (int): Software Register identifier, chech DAQ docs

    Returns:
    error_code (status_code): None if no error. Error code otherwise
    """
    value = -1
    error_code = None
    try:
        if registers[reg_group][reg_id]['permissions']['read']:
            value = registers[reg_group][reg_id]['value']
        else:
            error_code = status.ERR_WRITE_ONLY
    except KeyError:
        error_code = status.ERR_INVALID_REGISTER
    return value, error_code


def write_sw_register(petalo_server, daq_id, params):
    """
    Write value to SW register

    Parameters:
    petalo_server (PetaloMockServer): Runnging server
    daq_id        (int) : L1 ID
    params        (list): List of integers with all the command parameters

    Returns:
    bytearray: Command response encoded in a bytearray
    """
    register   = params[0]
    value      = params[1]
    error_code = write_register(petalo_server.sw_registers, register.group, register.id, value)
    response   = build_sw_register_write_response(daq_id, register.group, register.id, error_code)
    return response


def write_hw_register(petalo_server, daq_id, params):
    """
    Write value to HW register

    Parameters:
    petalo_server (PetaloMockServer): Runnging server
    daq_id        (int) : L1 ID
    params        (list): List of integers with all the command parameters

    Returns:
    bytearray: Command response encoded in a bytearray
    """
    register   = params[0]
    value      = params[1]
    error_code = write_register(petalo_server.hw_registers, register.group, register.id, value)
    response   = build_hw_register_write_response(daq_id, register.group, register.id, error_code)
    return response


def read_sw_register(petalo_server, daq_id, params):
    """
    Read value to HW register

    Parameters:
    petalo_server (PetaloMockServer): Runnging server
    daq_id        (int) : L1 ID
    params        (list): List of integers with all the command parameters

    Returns:
    bytearray: Command response encoded in a bytearray
    """
    register = params[0]
    value, error_code = read_register(petalo_server.sw_registers, register.group, register.id)
    response = build_sw_register_read_response(daq_id, register.group, register.id, value, error_code)
    return response


def read_hw_register(petalo_server, daq_id, params):
    """
    Read value to HW register

    Parameters:
    petalo_server (PetaloMockServer): Runnging server
    daq_id        (int) : L1 ID
    params        (list): List of integers with all the command parameters

    Returns:
    bytearray: Command response encoded in a bytearray
    """
    register = params[0]
    value, error_code = read_register(petalo_server.hw_registers, register.group, register.id)
    response = build_hw_register_read_response(daq_id, register.group, register.id, value, error_code)
    return response

