import struct
import ctypes
from petalo_daq.network.commands import code_to_status
from petalo_daq.network.commands import register_tuple

def encode_register_address(register_group, register_id):
    """
    Encode register address.
    16-bit higher part: register group
    16-bit lower  part: register id

    Parameters:
    register_group (int): Register group (up to 16 bits).
    register_id    (int): Register id    (up to 16 bits)..

    Returns:
    tuple: register_group (int) and register_id (int)
    """
    register_address = bytearray()
    register_address.extend(bytearray(struct.pack('<H', register_id)))
    register_address.extend(bytearray(struct.pack('<H', register_group)))

    address = int.from_bytes(register_address, 'little')
    return address

def decode_register_address(register_address):
    """
    Decode register address.
    16-bit higher part: register group
    16-bit lower  part: register id

    Parameters:
    register_address (int): 32-bit int with the address.

    Returns:
    tuple: register_group (int) and register_id (int)
    """
    bytestream     = register_address.to_bytes(length=4, byteorder='little')
    register_group = struct.unpack('<H', bytestream[2:4])[0]
    register_id    = struct.unpack('<H', bytestream[0:2])[0]
    return register_group, register_id


def encode_error_value(error_code):
    """
    Encode negative error values as C signed int

    Parameters:
    error_code (int): Error code, negative value

    Returns:
    int: Error code encoded as 32-bit signed int.
    """
    code = error_code.value & 0xFFFFFFFF # mask negative value
    return code


def parse_first_parameter_in_response(value):
    """
    In all Read and Write commands the first parameter in the response
    is either an error (negative value) or an encoded register address.
    This function decodes both and returns the corresponding object.

    Paramenters:
    value (int): 32-bit int with the value read from the response

    Returns:
    object: if the value is and error a status_code is return. Otherwise
            a register_tuple is returned.
    """
    signed_value = ctypes.c_int32(value).value
    result = None

    if signed_value < 0:
        result = code_to_status[signed_value]
    else:
        r_group, r_id = decode_register_address(value)
        result = register_tuple(r_group, r_id)

    return result
