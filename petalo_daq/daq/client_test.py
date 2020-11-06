#  from DAQ_control_Lib.py_comm_lib import SCK_TXRX
from petalo_daq.daq.petalo_network import SCK_TXRX
from queue import Queue, Empty
from threading import Thread, Event

import threading
from time import sleep

from pytest import raises
from pytest import mark

from petalo_daq.daq.commands import status_codes as status
from petalo_daq.daq.commands import commands     as cmd


def test_connection_incorrect_address(petalo_test_server):
    cfg_data = {'port'           :9116,
                'buffer_size'    :1024,
                'localhost'      :'127.0.0.1',
                'ext_ip'         :'127.1.1.1',
               }

    tx_queue = Queue()
    rx_queue = Queue()
    stopper  = Event()

    with raises(ConnectionRefusedError):
        thread_TXRX  = SCK_TXRX(cfg_data,tx_queue,rx_queue,stopper)
        thread_TXRX.start()


def test_connection_one_client():
    cfg_data = {'port'           :9116,
                'buffer_size'    :1024,
                'localhost'      :'127.0.0.1',
                'ext_ip'         :'127.0.0.1',
               }

    tx_queue = Queue()
    rx_queue = Queue()
    stopper  = Event()

    thread_TXRX  = SCK_TXRX(cfg_data,tx_queue,rx_queue,stopper)
    thread_TXRX.start()

    while not stopper.is_set():
        message = rx_queue.get()
        print(
            "Consumer storing message: {} (size={})".format(message, rx_queue.qsize())
        )
        if(message):
            stopper.set()

            assert message['command'] == cmd.CON_STATUS
            assert message['L1_id']   == 0
            assert message['n_params']   == 3
            assert len(message['params'])   == 1
            assert message['params'][0]   == 0

    end_connection_word = 0xfafafafa.to_bytes(length=4, byteorder='little')
    tx_queue.put(end_connection_word)

    thread_TXRX.join()
    #  sleep(8)


def test_connection_error_with_several_clients():
    end_connection_word = 0xfafafafa.to_bytes(length=4, byteorder='little')
    cfg_data = {'port'           :9116,
                'buffer_size'    :1024,
                'localhost'      :'127.0.0.1',
                'ext_ip'         :'127.0.0.1',
               }

    tx_queue = Queue()
    rx_queue = Queue()
    stopper  = Event()

    thread_TXRX_1  = SCK_TXRX(cfg_data,tx_queue,rx_queue,stopper)
    thread_TXRX_1.start()

    sleep(1)

    tx_queue_2 = Queue()
    rx_queue_2 = Queue()
    stopper_2  = Event()

    with raises(ConnectionRefusedError) as e_info:
        thread_TXRX_2  = SCK_TXRX(cfg_data,tx_queue_2,rx_queue_2,stopper_2)
        thread_TXRX_2.start()

    tx_queue.put(end_connection_word)
    tx_queue_2.put(end_connection_word)

    stopper.set()
    thread_TXRX_1.join()

