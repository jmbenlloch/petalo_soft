import ctypes

from petalo_daq.network.command_utils import encode_register_address
from petalo_daq.network.command_utils import decode_register_address
from petalo_daq.network.command_utils import encode_error_value
from petalo_daq.network.command_utils import parse_first_parameter_in_response
from petalo_daq.network.commands      import status_codes

def test_encode_and_decode_register_address():
    # The expected structure is:
    # 31...,.16,15.....0
    # |--RG---||--RID--|
    register_group   = 0x1234
    register_id      = 0x5678
    expected_address = 0x12345678

    address = encode_register_address(register_group, register_id)
    assert address == expected_address

    r_group, r_id = decode_register_address(address)
    assert r_group == register_group
    assert r_id    == register_id


def test_encode_error_value():
    # Uses ctypes to check negative values are properley encoded
    for status in status_codes:
        if status.name.startswith('ERR'):
            error_code = encode_error_value(status)
            assert ctypes.c_int32(error_code).value == status.value


def test_parse_first_parameter_in_response():
    # Check all the errors
    for status in status_codes:
        if status.name.startswith('ERR'):
            error_code = encode_error_value(status)
            result = parse_first_parameter_in_response(error_code)
            assert result == status

    #Check some register value
    register_group   = 0x1234
    register_id      = 0x5678
    value = encode_register_address(register_group, register_id)
    result = parse_first_parameter_in_response(value)
    assert register_group == result.group
    assert register_id    == result.id
