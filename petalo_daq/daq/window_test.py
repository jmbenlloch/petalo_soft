import sys
from pytest import fixture
from pytest import raises
from pytest import mark
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from time import sleep
import numpy as np
import re


from petalo_daq.daq.commands import commands
from petalo_daq.daq.commands import status_codes
from petalo_daq.daq.commands import register_tuple
from petalo_daq.gui.types    import LogError
from petalo_daq.daq.petalo_network    import MESSAGE

from petalo_daq.daq.command_utils import encode_error_value

from petalo_daq.daq.responses import check_write_response
from petalo_daq.daq.process_responses import temperature_conversion_1
from petalo_daq.daq.process_responses import temperature_conversion_1_celsius
from petalo_daq.daq.process_responses import temperature_conversion_2
from petalo_daq.daq.process_responses import temperature_tofpet_to_ch
from petalo_daq.daq.commands import sleep_cmd

from PETALO_v7 import PetaloRunConfigurationGUI
# from Libraries import database as db

def close_connection(window):
    end_connection_word = 0xfafafafa.to_bytes(length=4, byteorder='little')
    window.tx_queue.put(end_connection_word)
    window.tx_stopper.set()
    window.rx_stopper.set()
    window.thread_TXRX.join()
    #  window.rx_consumer.join()


def check_pattern_present_in_log(window, pattern, expected_matches, escape=True):
    if escape:
        pattern = re.escape(pattern)

    text = window.textBrowser.toPlainText()
    r = re.search(f'({pattern})', text, re.DOTALL)
    try:
        n_groups = len(r.groups())
    except AttributeError:
        n_groups = 0

    assert n_groups == expected_matches


def test_check_write_response(qtbot, petalo_test_server):
    """
    Write response commands must raise LogError if status code is
    an error code.
    """
    window = PetaloRunConfigurationGUI(test_mode=True)

    cmds = [commands.SOFT_REG_W_r, commands.HARD_REG_W_r]

    for cmd in cmds:
        for status in status_codes:
            if status.name.startswith('ERR'):
                with raises(LogError):
                    check_write_response(window, cmd, [status])
    close_connection(window)


def test_read_network_responses_logerror(qtbot, petalo_test_server):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    cmd   = commands.SOFT_REG_W_r
    error = status_codes.ERR_INVALID_REGISTER

    command_with_error = {
        'command'  : cmd,
        'L1_id'    : 0,
        'n_params' : 1,
        'params'   : [error]
    }

    window.rx_queue.put(command_with_error)
    sleep(0.1)

    # check error is shown in log
    pattern = '{} register error {}'.format(cmd.name, error.name)
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    close_connection(window)


def test_temperature_conversion_1():
    # TODO add hypothesis
    # TODO define range of operation
    samples = np.random.uniform(0, 0.8, 100)

    for temperature in samples:
        value_temp = np.round(temperature * 2**24 / 1.65).astype(np.int32)
        value      = (value_temp << 5) | 0xF000001F
        temp_converted = temperature_conversion_1(value)

        np.testing.assert_almost_equal(temperature, temp_converted, decimal=4)


def test_temperature_conversion_1_celsius():
    # TODO add hypothesis
    # TODO define range of operation
    samples = np.random.uniform(-50, 150, 300)

    for temperature in samples:
        voltage = 1777.3 - (10.888 * (temperature-30)) - (0.00347 * (temperature-30)**2)
        temp_converted = temperature_conversion_1_celsius(voltage/1000)
        print(temperature, voltage, temp_converted)
        np.testing.assert_almost_equal(temperature, temp_converted, decimal=4)



def test_temperature_conversion_2():
    # TODO add hypothesis
    # TODO define range of operation
    samples = np.random.uniform(0, 0.8, 100)

    for temperature in samples:
        value_temp = np.round((temperature + 273) * 1570 * 32 / 3.3).astype(np.int32)
        value      = value_temp | 0xF0000000
        temp_converted = temperature_conversion_2(value)

        np.testing.assert_almost_equal(temperature, temp_converted, decimal=4)


def test_read_temperatures(qtbot, petalo_test_server):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Temp_read, QtCore.Qt.LeftButton)

    # wait for results
    sleep(6)

    # check all temperatures
    np.testing.assert_almost_equal(window.lcdNumber_Temp_0.value(), 117.983, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_1.value(), 118.543, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_2.value(), 140.897, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_3.value(),   0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_4.value(), 118.634, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_5.value(),   0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_6.value(), 123.020, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_7.value(), 118.578, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_8.value(),  38.842, decimal=3)

    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_0.value(),  0.792, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_1.value(),  0.786, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_2.value(),  0.527, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_3.value(),  0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_4.value(),  0.785, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_5.value(),  0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_6.value(),  0.734, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_7.value(),  0.786, decimal=3)


    # check errors are shown in log
    pattern = 'Temperature configuration sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)
    pattern = 'Temperature error. Register register_tuple(group=2, id=1) has not 00 in bits 30, 31'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)
    pattern = 'Temperature error. Register register_tuple(group=2, id=2), input signal out of ADC range'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    close_connection(window)


def test_read_temperatures_send_correct_commands(qtbot, petalo_test_server):
    window = PetaloRunConfigurationGUI(test_mode=True)
    close_connection(window)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Temp_read, QtCore.Qt.LeftButton)

    assert window.tx_queue.qsize() == 18 # 9 channels + 9 sleeps

    message  = MESSAGE()
    for i in range(window.tx_queue.qsize()):
        # The sequence must be one (read cmd, sleep), 9 times
        cmd = window.tx_queue.get(i)
        if (i % 2) == 0:
            cmd      = message(cmd)
            params   = cmd['params']
            register = params[0]
            print(cmd)

            assert cmd['command' ] == commands.SOFT_REG_R
            assert cmd['L1_id'   ] == 0
            assert cmd['n_params'] == 1
            assert len(params)     == cmd['n_params']
            assert register.group  == 2
            assert register.id     == temperature_tofpet_to_ch[i/2]

        else:
            assert isinstance(cmd, sleep_cmd)


def test_temperature_control_register(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Temp_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'Temperature configuration sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]
    print(cmd_binary)
    print(cmd)

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 0
    assert register.id     == 0
    #TODO test register content somehow...


def test_power_control_register(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Power_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'Power control register sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]
    print(cmd_binary)
    print(cmd)

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 1
    assert register.id     == 0
    #TODO test register content somehow...


def test_power_status_register_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Power_status_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'Power status command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]

    assert cmd['command' ] == commands.HARD_REG_R
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 1
    assert len(params)     == cmd['n_params']
    assert register.group  == 1
    assert register.id     == 1
    #TODO test register content somehow... and test GUI update


def test_clock_status_register_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Clock_status_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'Clock status command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]

    assert cmd['command' ] == commands.HARD_REG_R
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 1
    assert len(params)     == cmd['n_params']
    assert register.group  == 2
    assert register.id     == 2
    #TODO test register content somehow... and test GUI update


def test_link_status_register_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Link_status_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'Link status command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]

    assert cmd['command' ] == commands.HARD_REG_R
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 1
    assert len(params)     == cmd['n_params']
    assert register.group  == 3
    assert register.id     == 1
    #TODO test register content somehow... and test GUI update


def test_start_run_register_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
    pattern = 'Run has started'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]
    print(cmd_binary)
    print(cmd)

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 4
    assert register.id     == 0
    #TODO test register content somehow...


def test_stop_run_register_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.STOP, QtCore.Qt.LeftButton)
    pattern = 'The run is stopped'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]
    print(cmd_binary)
    print(cmd)

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 4
    assert register.id     == 0
    #TODO test register content somehow...


def test_clock_control_register_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Clock_control_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'Clock control command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]
    print(cmd_binary)
    print(cmd)

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 2
    assert register.id     == 0
    #TODO test register content somehow...


def test_lmk_control_register_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Clock_LMK_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'LMK control command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]
    print(cmd_binary)
    print(cmd)

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 2
    assert register.id     == 1
    #TODO test register content somehow...


def test_link_control_register_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TOFPET_LINK_CONTROL, QtCore.Qt.LeftButton)
    pattern = 'Link control command sent'

    print("log: ", window.textBrowser.toPlainText())

    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]
    print(cmd_binary)
    print(cmd)

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 3
    assert register.id     == 0
    #TODO test register content somehow...


def test_tofpet_status_register_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TOFPET_STATUS, QtCore.Qt.LeftButton)
    pattern = 'TOFPET status command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]

    assert cmd['command' ] == commands.HARD_REG_R
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 1
    assert len(params)     == cmd['n_params']
    assert register.group  == 3
    assert register.id     == 4
    #TODO test register content somehow... and test GUI update
    #TODO check effect on GUI


def test_tofpet_config_value_register_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TOPFET_CONF_VALUE, QtCore.Qt.LeftButton)
    pattern = 'TOFPET configuration value sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 3
    assert register.id     == 3
    #TODO test register content somehow... and test GUI update


def test_tofpet_config_register_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TOPFET_CONF, QtCore.Qt.LeftButton)
    pattern = 'TOFPET configuration command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)

    message  = MESSAGE()
    cmd      = message(cmd_binary)
    params   = cmd['params']
    register = params[0]

    assert cmd['command' ] == commands.HARD_REG_W
    assert cmd['L1_id'   ] == 0
    assert cmd['n_params'] == 2
    assert len(params)     == cmd['n_params']
    assert register.group  == 3
    assert register.id     == 2
    #TODO test register content somehow... and test GUI update


def test_leds_status_register_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_LEDs_read, QtCore.Qt.LeftButton)
    pattern = 'LEDs status command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 2

    message  = MESSAGE()
    for i in range(window.tx_queue.qsize()):
        # The sequence must be write and read
        cmd_binary = window.tx_queue.get(i)
        cmd       = message(cmd_binary)
        params    = cmd['params']
        register  = params[0]

        if i == 0:
            assert cmd['command' ] == commands.SOFT_REG_W
            assert cmd['L1_id'   ] == 0
            assert cmd['n_params'] == 2
            assert len(params)     == cmd['n_params']
            assert register.group  == 1
            assert register.id     == 0
            assert params[1]       == 0xFFFFFFFF
        if i == 1:
            assert cmd['command' ] == commands.SOFT_REG_R
            assert cmd['L1_id'   ] == 0
            assert cmd['n_params'] == 1
            assert len(params)     == cmd['n_params']
            assert register.group  == 1
            assert register.id     == 0
            #TODO test register content somehow... and test GUI update


import petalo_daq.daq.mock_server.binary_responses as srv_cmd

@mark.parametrize(('value', 'activated_field'),
                 ((1 << 16, 'LINK_STATUS_IDL_ready'),
                  (1 << 15, 'LINK_STATUS_ALIGNING_7'),
                  (1 << 14, 'LINK_STATUS_ALIGNING_6'),
                  (1 << 13, 'LINK_STATUS_ALIGNING_5'),
                  (1 << 12, 'LINK_STATUS_ALIGNING_4'),
                  (1 << 11, 'LINK_STATUS_ALIGNING_3'),
                  (1 << 10, 'LINK_STATUS_ALIGNING_2'),
                  (1 <<  9, 'LINK_STATUS_ALIGNING_1'),
                  (1 <<  8, 'LINK_STATUS_ALIGNING_0'),
                  (1 <<  7, 'LINK_STATUS_ALIGNED_7'),
                  (1 <<  6, 'LINK_STATUS_ALIGNED_6'),
                  (1 <<  5, 'LINK_STATUS_ALIGNED_5'),
                  (1 <<  4, 'LINK_STATUS_ALIGNED_4'),
                  (1 <<  3, 'LINK_STATUS_ALIGNED_3'),
                  (1 <<  2, 'LINK_STATUS_ALIGNED_2'),
                  (1 <<  1, 'LINK_STATUS_ALIGNED_1'),
                  (1      , 'LINK_STATUS_ALIGNED_0')))
def test_link_status_gui(qtbot, value, activated_field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # Check RDY IDLYCTRL
    cmd = srv_cmd.build_hw_register_read_response(daq_id=0, register_group=3, register_id=1, value=value, error_code=None)
    message = MESSAGE()
    cmd = message(cmd)
    print(cmd)

    window.rx_queue.put(cmd)
    sleep(0.1)

    fields = ['LINK_STATUS_IDL_ready',
              'LINK_STATUS_ALIGNED_0',
              'LINK_STATUS_ALIGNED_1',
              'LINK_STATUS_ALIGNED_2',
              'LINK_STATUS_ALIGNED_3',
              'LINK_STATUS_ALIGNED_4',
              'LINK_STATUS_ALIGNED_5',
              'LINK_STATUS_ALIGNED_6',
              'LINK_STATUS_ALIGNED_7',

              'LINK_STATUS_ALIGNING_0',
              'LINK_STATUS_ALIGNING_1',
              'LINK_STATUS_ALIGNING_2',
              'LINK_STATUS_ALIGNING_3',
              'LINK_STATUS_ALIGNING_4',
              'LINK_STATUS_ALIGNING_5',
              'LINK_STATUS_ALIGNING_6',
              'LINK_STATUS_ALIGNING_7']

    for field in fields:
        widget = getattr(window, f'checkBox_{field}')
        if field == activated_field:
            assert widget.isChecked() == True
        else:
            assert widget.isChecked() == False


@mark.parametrize(('value', 'activated_field'),
                 (((1 << 31) ^ 0x000000FF, 'PWR_STATUS_CONF_DONE'),
                  ((1 << 30) ^ 0x000000FF, 'PWR_STATUS_CONF_ON'),
                  ((1 << 18) ^ 0x000000FF, 'PWR_STATUS_18DIS'),
                  ((1 << 17) ^ 0x000000FF, 'PWR_STATUS_25EN_1'),
                  ((1 << 16) ^ 0x000000FF, 'PWR_STATUS_25EN_2'),
                  ((1 << 15) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_7'),
                  ((1 << 14) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_6'),
                  ((1 << 13) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_5'),
                  ((1 << 12) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_4'),
                  ((1 << 11) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_3'),
                  ((1 << 10) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_2'),
                  ((1 <<  9) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_1'),
                  ((1 <<  8) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCCEN_0'),

                  ((1 <<  7) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_7'),
                  ((1 <<  6) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_6'),
                  ((1 <<  5) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_5'),
                  ((1 <<  4) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_4'),
                  ((1 <<  3) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_3'),
                  ((1 <<  2) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_2'),
                  ((1 <<  1) ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_1'),
                  ( 1        ^ 0x000000FF, 'PWR_STATUS_TOFPET_VCC25EN_0')))
def test_power_status_gui(qtbot, value, activated_field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # Check RDY IDLYCTRL
    cmd = srv_cmd.build_hw_register_read_response(daq_id=0, register_group=1, register_id=1, value=value, error_code=None)
    message = MESSAGE()
    cmd = message(cmd)
    print(cmd)

    window.rx_queue.put(cmd)
    sleep(0.1)

    fields = ['PWR_STATUS_CONF_DONE',
              'PWR_STATUS_CONF_ON',
              'PWR_STATUS_18DIS',
              'PWR_STATUS_25EN_1',
              'PWR_STATUS_25EN_2',
              'PWR_STATUS_TOFPET_VCCEN_0',
              'PWR_STATUS_TOFPET_VCCEN_1',
              'PWR_STATUS_TOFPET_VCCEN_2',
              'PWR_STATUS_TOFPET_VCCEN_3',
              'PWR_STATUS_TOFPET_VCCEN_4',
              'PWR_STATUS_TOFPET_VCCEN_5',
              'PWR_STATUS_TOFPET_VCCEN_6',
              'PWR_STATUS_TOFPET_VCCEN_7',
              'PWR_STATUS_TOFPET_VCC25EN_0',
              'PWR_STATUS_TOFPET_VCC25EN_1',
              'PWR_STATUS_TOFPET_VCC25EN_2',
              'PWR_STATUS_TOFPET_VCC25EN_3',
              'PWR_STATUS_TOFPET_VCC25EN_4',
              'PWR_STATUS_TOFPET_VCC25EN_5',
              'PWR_STATUS_TOFPET_VCC25EN_6',
              'PWR_STATUS_TOFPET_VCC25EN_7']


    for field in fields:
        widget = getattr(window, f'checkBox_{field}')
        if field == activated_field:
            assert widget.isChecked() == True
        else:
            assert widget.isChecked() == False


@mark.parametrize(('value', 'activated_field'),
                 ((1 << 7, 'TOFPET_STATUS_ERR_CRC_GL'),
                  (1 << 6, 'TOFPET_STATUS_ERR_CFG_GL'),
                  (1 << 5, 'TOFPET_STATUS_ERR_CRC_CH'),
                  (1 << 4, 'TOFPET_STATUS_ERR_CFG_CH'),
                  (1 << 3, 'TOFPET_STATUS_ERR_ACK_CREAD'),
                  (1 << 2, 'TOFPET_STATUS_ERR_ACK_CWRITE'),
                  (1 << 1, 'TOFPET_STATUS_ERR_ACK_GREAD'),
                  (1     , 'TOFPET_STATUS_ERR_ACK_GWRITE')))
def test_tofpet_conf_status_gui(qtbot, value, activated_field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # Check RDY IDLYCTRL
    cmd = srv_cmd.build_hw_register_read_response(daq_id=0, register_group=3, register_id=4, value=value, error_code=None)
    message = MESSAGE()
    cmd = message(cmd)
    print(cmd)

    window.rx_queue.put(cmd)
    sleep(0.1)

    fields = ['TOFPET_STATUS_ERR_CRC_GL',
              'TOFPET_STATUS_ERR_CFG_GL',
              'TOFPET_STATUS_ERR_CRC_CH',
              'TOFPET_STATUS_ERR_CFG_CH',
              'TOFPET_STATUS_ERR_ACK_CREAD',
              'TOFPET_STATUS_ERR_ACK_CWRITE',
              'TOFPET_STATUS_ERR_ACK_GREAD',
              'TOFPET_STATUS_ERR_ACK_GWRITE']

    for field in fields:
        widget = getattr(window, f'checkBox_{field}')
        if field == activated_field:
            assert widget.isChecked() == True
        else:
            assert widget.isChecked() == False


@mark.parametrize(('value', 'activated_field'),
                 ((1 << 7, 'LED_7'),
                  (1 << 6, 'LED_6'),
                  (1 << 5, 'LED_5'),
                  (1 << 4, 'LED_4'),
                  (1 << 3, 'LED_3')))
def test_leds_status_gui(qtbot, value, activated_field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # Check RDY IDLYCTRL
    cmd = srv_cmd.build_sw_register_read_response(daq_id=0, register_group=1, register_id=0, value=value, error_code=None)
    message = MESSAGE()
    cmd = message(cmd)
    print(cmd)

    window.rx_queue.put(cmd)
    sleep(0.1)

    fields = ['LED_7', 'LED_6', 'LED_5','LED_4','LED_3']

    for field in fields:
        assert window.lcdNumber_LED_Link_Alignment.value() == 0
        widget = getattr(window, f'checkBox_{field}')
        if field == activated_field:
            assert widget.isChecked() == True
        else:
            assert widget.isChecked() == False


def test_leds_status_selected_link_gui(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for value in range(0, 8):
        cmd = srv_cmd.build_sw_register_read_response(daq_id=0, register_group=1, register_id=0,
                                                      value=value, error_code=None)
        message = MESSAGE()
        cmd = message(cmd)
        print(cmd)

        window.rx_queue.put(cmd)
        sleep(0.1)

        assert window.lcdNumber_LED_Link_Alignment.value() == value
        assert window.checkBox_LED_7.isChecked() == False
        assert window.checkBox_LED_6.isChecked() == False
        assert window.checkBox_LED_5.isChecked() == False
        assert window.checkBox_LED_4.isChecked() == False
        assert window.checkBox_LED_3.isChecked() == False
        assert window.checkBox_LED_7.isChecked() == False


@mark.parametrize(('value', 'activated_field'),
                 ((1 << 15, 'CLK_STAT_1'),
                  (1 << 14, 'CLK_STAT_0'),
                  (1 << 13, 'CLK_SEL_1'),
                  (1 << 12, 'CLK_SEL_0'),
                  (1 << 11, 'CLK_CONF_DONE'),
                  (1 << 10, 'CLK_CONF_ON'),
                  (1 <<  9, 'CLK_REG_PROG_DONE'),
                  (1 <<  8, 'CLK_REG_PROG_READY')))
def test_clock_status_gui(qtbot, value, activated_field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # Check RDY IDLYCTRL
    cmd = srv_cmd.build_hw_register_read_response(daq_id=0, register_group=2, register_id=2, value=value, error_code=None)
    message = MESSAGE()
    cmd = message(cmd)
    print(cmd)

    window.rx_queue.put(cmd)
    sleep(0.1)

    fields = ['CLK_STAT_1',
              'CLK_STAT_0',
              'CLK_SEL_0',
              'CLK_SEL_1',
              'CLK_CONF_DONE',
              'CLK_CONF_ON',
              'CLK_REG_PROG_DONE',
              'CLK_REG_PROG_READY']

    for field in fields:
        assert window.lineEdit_CLK_CONF_REG_PROG_VALUE.text() == '0x00'
        widget = getattr(window, f'checkBox_{field}')
        if field == activated_field:
            assert widget.isChecked() == True
        else:
            assert widget.isChecked() == False


def test_clock_status_conf_data_out_gui(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for value in range(0, 127):
        cmd = srv_cmd.build_hw_register_read_response(daq_id=0, register_group=2, register_id=2, value=value, error_code=None)
        message = MESSAGE()
        cmd = message(cmd)
        print(cmd)

        window.rx_queue.put(cmd)
        sleep(0.1)

        expected_value = '0x{:02X}'.format(value)
        assert window.lineEdit_CLK_CONF_REG_PROG_VALUE.text() == expected_value
        assert window.checkBox_CLK_STAT_1.isChecked() == False
        assert window.checkBox_CLK_STAT_0.isChecked()          == False
        assert window.checkBox_CLK_SEL_0.isChecked()           == False
        assert window.checkBox_CLK_SEL_1.isChecked()           == False
        assert window.checkBox_CLK_CONF_DONE.isChecked()       == False
        assert window.checkBox_CLK_CONF_ON.isChecked()         == False
        assert window.checkBox_CLK_REG_PROG_DONE.isChecked()   == False
        assert window.checkBox_CLK_REG_PROG_READY.isChecked()  == False


#  @fixture(scope='session')
#  def database_connection():
#      conn, cursor = db.mysql_connect('localhost', 'root', 'root', 'petalo')
#      return conn, cursor
#
#  @mark.skip(reason="TBD")
#  def test_start_run(qtbot, database_connection):
#      window = MyApp()
#      qtbot.mouseClick(window.pushButton_reg_glob, QtCore.Qt.LeftButton)
#      qtbot.mouseClick(window.pushButton_reg_ch  , QtCore.Qt.LeftButton)
#      qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
#
#      print('\n\n\n\n run number:')
#      print(db.get_latest_run_number(database_connection[1]))
#      assert 0


# Check save to json
# Check load from json
# Check save to database

# define one config word and all the associated fields

@fixture()
def global_config():
    values = {
        'word' : '100000 00000 1 010011 11 0111 01101 110000 010011 111011 10111 1 0010 10010 101000 1110 110110 110000 111010 10011 00100 10111 111011 100011 00000 00001 10100 10111 11111 111001 101111 1 0 0 00 1001 1 110 0 00 00 110 1 000000 0 10 1 10',
        'fields' : {
            "tx_nlinks"         : '10',
            "tx_ddr"            : '1',
            "tx_mode"           : '10',
            "debug_mode"        : '0',
            "veto_mode"         : '000000',
            "tdc_clk_div"       : '1',
            "r_clk_en"          : '110',
            "stop_ramp_en"      : '00',
            "counter_en"        : '0',
            "counter_period"    : '110',
            "tac_refresh_en"    : '1',
            "tac_refresh_period": '1001',
            "data_clk_div"      : '00',
            "fetp_enable"       : '0',
            "input_polarity"    : '1',
            "attenuator_ls"     : '101111',
            "v_ref_diff_bias_ig": '111001',
            "v_cal_ref_ig"      : '11111',
            "fe_postamp_t"      : '10111',
            "fe_postamp_e"      : '10100',
            "v_cal_tp_top"      : '00001',
            "v_cal_diff_bias_ig": '00000',
            "v_att_diff_bias_ig": '100011',
            "v_integ_ref_ig"    : '111011',
            "imirror_bias_top"  : '10111',
            "tdc_comp_bias"     : '00100',
            "tdc_i_lsb"         : '10011',
            "disc_lsb_t1"       : '111010',
            "fe_ib2"            : '110000',
            "vdifffoldcas"      : '110110',
            "disc_vcas"         : '1110',
            "disc_lsb_e"        : '101000',
            "tdc_i_ref"         : '10010',
            "tdc_comp_vcas"     : '0010',
            "fe_ib2_x2"         : '1',
            "main_global_dac"   : '10111',
            "fe_ib1"            : '111011',
            "disc_ib"           : '010011',
            "disc_lsb_t2"       : '110000',
            "tdc_tac_vcas_p"    : '1101',
            "tdc_tac_vcas_n"    : '11',
            "adebug_out_mode"   : '010011',
            "tdc_global_dac"    : '1',
            "adebug_buffer"     : '00000',
            "disc_sf_bias"      : '100000',
        }
    }
    return values
