from queue     import Queue, Empty
from threading import Thread, Event

from time import sleep

from pytest import raises
from pytest import mark
from pytest import fixture
import numpy as np

from . petalo_network  import SCK_TXRX
from . client_commands import build_sw_register_write_command
from . client_commands import build_hw_register_write_command
from . client_commands import build_sw_register_read_command
from . client_commands import build_hw_register_read_command
from . command_utils   import encode_register_address
from . command_utils   import encode_error_value

from . commands        import status_codes   as status
from . commands        import commands       as cmd
from . commands        import register_tuple



@fixture(scope='module')
def petalo_connection():
    cfg_data = {'port'           :9116,
                'buffer_size'    :1024,
                'localhost'      :'127.0.0.1',
                'ext_ip'         :'127.0.0.1',
               }

    tx_queue = Queue()
    rx_queue = Queue()
    stopper  = Event()

    thread_TXRX  = SCK_TXRX(cfg_data,tx_queue,rx_queue,stopper)
    thread_TXRX.daemon = True
    thread_TXRX.start()

    expected_response = {
        'command'  : cmd.CON_STATUS,
        'L1_id'    : 0,
        'n_params' : 1,
        'params'   : [status.STA_CONNECTION_ACCEPT.value]
    }


    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break

    yield tx_queue, rx_queue, stopper

    # Disconnect
    end_connection_word = 0xfafafafa.to_bytes(length=4, byteorder='little')
    tx_queue.put(end_connection_word)
    stopper.set()
    thread_TXRX.join()


def check_expected_response(response, expected_response):
    assert response['command']  == expected_response['command']
    assert response['L1_id']    == expected_response['L1_id']
    assert response['n_params'] == expected_response['n_params']
    assert response['n_params'] == len(response['params'])
    np.testing.assert_equal(response['params'], expected_response['params'])


def test_write_sw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id   = 0xffff
    register = register_tuple(group=0, id=2)
    value    = 0x98765432

    command = build_sw_register_write_command(daq_id, register.group, register.id, value)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.SOFT_REG_W_r,
        'L1_id'    : daq_id,
        'n_params' : 1,
        'params'   : [register]
    }

    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_write_invalid_sw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id = 0xffff
    register_group = 123
    register_id    = 45
    value          = 0x98765432

    command = build_sw_register_write_command(daq_id, register_group, register_id, value)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.SOFT_REG_W_r,
        'L1_id'    : daq_id,
        'n_params' : 1,
        'params'   : [status.ERR_INVALID_REGISTER]
    }

    while not stopper.is_set():
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_write_readonly_sw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id = 0xffff
    register_group = 0
    register_id    = 1
    value          = 0x98765432

    command = build_sw_register_write_command(daq_id, register_group, register_id, value)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.SOFT_REG_W_r,
        'L1_id'    : daq_id,
        'n_params' : 1,
        'params'   : [status.ERR_READ_ONLY]
    }

    while not stopper.is_set():
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_write_hw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id   = 0xffff
    register = register_tuple(group=2, id=1)
    value    = 0x98765432

    command = build_hw_register_write_command(daq_id, register.group, register.id, value)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.HARD_REG_W_r,
        'L1_id'    : daq_id,
        'n_params' : 1,
        'params'   : [register]
    }

    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_write_invalid_hw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id = 0xffff
    register_group = 123
    register_id    = 45
    value          = 0x98765432

    command = build_hw_register_write_command(daq_id, register_group, register_id, value)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.HARD_REG_W_r,
        'L1_id'    : daq_id,
        'n_params' : 1,
        'params'   : [status.ERR_INVALID_REGISTER]
    }

    while not stopper.is_set():
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_write_readonly_hw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id         = 0xffff
    register_group = 1
    register_id    = 1
    value          = 0x98765432

    command = build_hw_register_write_command(daq_id, register_group, register_id, value)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.HARD_REG_W_r,
        'L1_id'    : daq_id,
        'n_params' : 1,
        'params'   : [status.ERR_READ_ONLY]
    }

    while not stopper.is_set():
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break



def test_read_sw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id         = 0xffff
    register       = register_tuple(group=0, id=2)
    expected_value = 0x98765432

    command = build_sw_register_read_command(daq_id, register.group, register.id)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.SOFT_REG_R_r,
        'L1_id'    : daq_id,
        'n_params' : 2,
        'params'   : [register,
                      expected_value]
    }

    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_read_hw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id         = 0xffff
    register       = register_tuple(group=1, id=1)
    expected_value = 0x800300FF

    command = build_hw_register_read_command(daq_id, register.group, register.id)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.HARD_REG_R_r,
        'L1_id'    : daq_id,
        'n_params' : 2,
        'params'   : [register,
                      expected_value]
    }

    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_read_invalid_sw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id         = 0xffff
    register_group = 1234
    register_id    = 546

    command = build_sw_register_read_command(daq_id, register_group, register_id)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.SOFT_REG_R_r,
        'L1_id'    : daq_id,
        'n_params' : 2,
        'params'   : [status.ERR_INVALID_REGISTER, 0]
    }

    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_read_invalid_hw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id         = 0xffff
    register_group = 1234
    register_id    = 32546

    command = build_hw_register_read_command(daq_id, register_group, register_id)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.HARD_REG_R_r,
        'L1_id'    : daq_id,
        'n_params' : 2,
        'params'   : [status.ERR_INVALID_REGISTER, 0]
    }

    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break


def test_read_writeonly_hw_register(petalo_connection):
    tx_queue = petalo_connection[0]
    rx_queue = petalo_connection[1]
    stopper  = petalo_connection[2]

    daq_id         = 0xffff
    register_group = 1
    register_id    = 0

    command = build_hw_register_read_command(daq_id, register_group, register_id)
    tx_queue.put(command)

    expected_response = {
        'command'  : cmd.HARD_REG_R_r,
        'L1_id'    : daq_id,
        'n_params' : 2,
        'params'   : [status.ERR_WRITE_ONLY, 0]
    }

    while True:
        message = rx_queue.get()
        if(message):
            check_expected_response(message, expected_response)
            break

