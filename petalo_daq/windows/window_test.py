import sys
import numpy as np
import re

from pytest import fixture
from pytest import raises
from pytest import mark

from PyQt5  import uic
from PyQt5  import QtWidgets
from PyQt5  import QtCore

from time     import sleep
from bitarray import bitarray


from .. gui.types                 import LogError
from .. network.commands          import commands
from .. network.commands          import sleep_cmd
from .. network.commands          import status_codes
from .. network.commands          import register_tuple
from .. network.command_test      import check_expected_response
from .. network.command_utils     import encode_error_value
from .. network.petalo_network    import MESSAGE
from .. network.responses         import check_write_response
from .. network.process_responses import temperature_tofpet_to_ch

from .. testing.utils             import check_pattern_present_in_log
from .. testing.utils             import close_connection

from PETALO_v7 import PetaloRunConfigurationGUI


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


def test_read_temperatures(qtbot, petalo_test_server):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_Temp_read, QtCore.Qt.LeftButton)

    # wait for results
    sleep(6)

    # check all temperatures
    np.testing.assert_almost_equal(window.lcdNumber_Temp_0.value(),  55.265, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_1.value(), 126.006, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_2.value(),  27.914, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_3.value(),   0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_4.value(),   0.077, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_5.value(),   0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_6.value(), -14.033, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_7.value(), 134.639, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_8.value(),  38.842, decimal=3)

    print(window.lcdNumber_Temp_raw_0.value())
    print(window.lcdNumber_Temp_raw_1.value())
    print(window.lcdNumber_Temp_raw_2.value())
    print(window.lcdNumber_Temp_raw_3.value())
    print(window.lcdNumber_Temp_raw_4.value())
    print(window.lcdNumber_Temp_raw_5.value())
    print(window.lcdNumber_Temp_raw_6.value())
    print(window.lcdNumber_Temp_raw_7.value())

    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_0.value(),  1.500, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_1.value(),  0.700, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_2.value(),  1.800, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_3.value(),  0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_4.value(),  2.100, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_5.value(),  0    , decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_6.value(),  2.250, decimal=3)
    np.testing.assert_almost_equal(window.lcdNumber_Temp_raw_7.value(),  0.600, decimal=3)


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


@mark.parametrize(('bit_position', 'field'),
                 ((0, 'Temp_RST'),
                  (1, 'Temp_Start'),
                  (2, 'Temp_RD_Control_SGL'),
                  (3, 'Temp_RD_Control_SPD'),
                  (4, 'Temp_RD_Control_FB'),
                  (5, 'Temp_RD_Control_FA'),
                  (6, 'Temp_RD_Control_IM'),
                  (7, 'Temp_RD_Control_EN2')))
def test_temperature_control_register_boolean_fields(qtbot, bit_position, field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # set default time (1 ms)
    window.spinBox_Temp_Time.setValue(1)
    temp_mask = 0x061A8000

    for status in [True, False]:
        widget = getattr(window, f'checkBox_{field}')
        widget.setChecked(status)

        qtbot.mouseClick(window.pushButton_Temp_hw_reg, QtCore.Qt.LeftButton)
        pattern = 'Temperature configuration sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = int(status) << bit_position | temp_mask
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=0, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_temperature_control_register_channel_selection(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # set default time (1 ms)
    window.spinBox_Temp_Time.setValue(1)
    temp_mask = 0x061A8000

    widget = window.comboBox_Temp_CH_Sel

    #check number of channels
    assert widget.count() == 9

    for channel in range(0, 9):
        # choose channel and check widget properties
        widget.setCurrentIndex(channel)
        assert widget.currentIndex() == channel
        assert widget.currentText()  == f"CH {channel}"
        expected_bitarray = bitarray('{:04b}'.format(channel))
        assert widget.currentData() == expected_bitarray

        qtbot.mouseClick(window.pushButton_Temp_hw_reg, QtCore.Qt.LeftButton)
        pattern = 'Temperature configuration sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = channel << 8 | temp_mask
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=0, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_temperature_control_register_time_selection(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    widget = window.spinBox_Temp_Time
    min_value_ms = 1
    max_value_ms = 42
    step_ms      = 1

    for time_gui in range(min_value_ms, max_value_ms+step_ms, step_ms):
        print("time: " , time_gui)
        widget.setValue(time_gui)

        qtbot.mouseClick(window.pushButton_Temp_hw_reg, QtCore.Qt.LeftButton)
        pattern = 'Temperature configuration sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        # Convert time
        discretized_value  = np.round(time_gui * 10**6 / 40).astype(np.int32)
        binary_value       = '{:020b}'.format(discretized_value)

        expected_value    = discretized_value << 12
        if expected_value > 0x0FFFFFFFF:
            expected_value = 0xFFFFF000
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=0, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


@mark.parametrize(('bit_position', 'field'),
                  ((31, 'PWR_GStart'),
                   (30, 'PWR_Start'),
                   (29, 'PWR_RST'),
                   (18, 'PWR_18DIS'),
                   (17, 'PWR_25EN_1'),
                   (16, 'PWR_25EN_2'),
                   (15, 'PWR_TOFPET_VCCEN_7'),
                   (14, 'PWR_TOFPET_VCCEN_6'),
                   (13, 'PWR_TOFPET_VCCEN_5'),
                   (12, 'PWR_TOFPET_VCCEN_4'),
                   (11, 'PWR_TOFPET_VCCEN_3'),
                   (10, 'PWR_TOFPET_VCCEN_2'),
                   ( 9, 'PWR_TOFPET_VCCEN_1'),
                   ( 8, 'PWR_TOFPET_VCCEN_0'),
                   ( 7, 'PWR_TOFPET_VCC25EN_7'),
                   ( 6, 'PWR_TOFPET_VCC25EN_6'),
                   ( 5, 'PWR_TOFPET_VCC25EN_5'),
                   ( 4, 'PWR_TOFPET_VCC25EN_4'),
                   ( 3, 'PWR_TOFPET_VCC25EN_3'),
                   ( 2, 'PWR_TOFPET_VCC25EN_2'),
                   ( 1, 'PWR_TOFPET_VCC25EN_1'),
                   ( 0, 'PWR_TOFPET_VCC25EN_0')))
def test_power_control_register(qtbot, bit_position, field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for status in [True, False]:
        widget = getattr(window, f'checkBox_{field}')
        widget.setChecked(status)

        qtbot.mouseClick(window.pushButton_Power_hw_reg, QtCore.Qt.LeftButton)
        pattern = 'Power control register sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = int(status) << bit_position
        expected_value    = expected_value ^ 0x000000FF # VCC25EN are disabled on 1
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=1, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


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


def test_clock_control_register_send_command(qtbot, bit_position, field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()


@mark.parametrize(('bit_position', 'field'),
                  ((30, 'CLK_Start'),
                   (29, 'CLK_RST')))
def test_clock_control_register_send_command(qtbot, bit_position, field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for status in [True, False]:
        widget = getattr(window, f'checkBox_{field}')
        widget.setChecked(status)

        qtbot.mouseClick(window.pushButton_Clock_control_hw_reg, QtCore.Qt.LeftButton)
        pattern = 'Clock control command sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = int(status) << bit_position
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=2, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_lmk_control_register_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # Check all options for each field separately
    for enable in (True, False):
        check_lmk_control_cmd(qtbot, window, enable, address=0, value=0)
    for address in range(0, 128):
        check_lmk_control_cmd(qtbot, window, enable=True, address=address, value=0)
    for value in range(0, 256):
        check_lmk_control_cmd(qtbot, window, enable=True, address=0, value=value)


def check_lmk_control_cmd(qtbot, window, enable, address, value):
    # set values in GUI
    window.checkBox_LMK_WREN    .setChecked(enable)
    window.spinBox_LMK_REG_ADD  .setValue(address)
    window.spinBox_LMK_REG_VALUE.setValue(value)

    qtbot.mouseClick(window.pushButton_Clock_LMK_hw_reg, QtCore.Qt.LeftButton)
    pattern = 'LMK control command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)
    message    = MESSAGE()
    cmd        = message(cmd_binary)

    expected_value    = (1 << 31) | (int(enable) << 15) | (address << 8) | value
    expected_response = {
        'command'  : commands.HARD_REG_W,
        'L1_id'    : 0,
        'n_params' : 2,
        'params'   : [register_tuple(group=2, id=1),
                      expected_value]
    }
    check_expected_response(cmd, expected_response)


@mark.parametrize(('bit_position', 'field'),
                  ((31, 'TOFPET_LINK_CONF'),
                   (30, 'TOFPET_LINK_RST'),
                   (29, 'TOFPET_LINK_CONF_IODELAY'),
                   (28, 'TOFPET_LINK_RST_IODELAY'),
                   ( 3, 'TOFPET_LINK_BC')))
def test_link_control_register_send_command_boolean_fields(qtbot, bit_position, field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for status in [True, False]:
        widget = getattr(window, f'checkBox_{field}')
        widget.setChecked(status)

        qtbot.mouseClick(window.pushButton_TOFPET_LINK_CONTROL, QtCore.Qt.LeftButton)
        pattern = 'Link control command sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = int(status) << bit_position
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_link_control_register_send_command_sel_mux(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    widget = window.comboBox_TOFPET_LINK_SEL_MUX

    #check number of TOFPETs
    assert widget.count() == 8

    for channel in range(0, 8):
        # choose channel and check widget properties
        widget.setCurrentIndex(channel)
        assert widget.currentIndex() == channel
        assert widget.currentText()  == f"{channel}"
        expected_bitarray = bitarray('{:03b}'.format(channel))
        assert widget.currentData() == expected_bitarray

        qtbot.mouseClick(window.pushButton_TOFPET_LINK_CONTROL, QtCore.Qt.LeftButton)
        pattern = 'Link control command sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = channel
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


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

    # Check all bits to 1, one by one
    for bit_position in range(0, 32):
        print("bit_position: ", bit_position)
        expected_value    = 1 << bit_position
        window.spinBox_TOPFET_CONF_VALUE.setValue(expected_value)

        qtbot.mouseClick(window.pushButton_TOPFET_CONF_VALUE, QtCore.Qt.LeftButton)
        pattern = 'TOFPET configuration value sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=3),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)



@mark.parametrize(('bit_position', 'field'),
                  ((31, 'TOFPET_CONF_START'),
                   (30, 'TOFPET_CONF_VERIFY'),
                   (29, 'TOFPET_CONF_ERROR_RST'),
                   (20, 'TOFPET_CONF_WR')))
def test_tofpet_config_register_command_boolean_fields(qtbot, bit_position, field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for status in [True, False]:
        widget = getattr(window, f'checkBox_{field}')
        widget.setChecked(status)

        qtbot.mouseClick(window.pushButton_TOPFET_CONF, QtCore.Qt.LeftButton)
        pattern = 'TOFPET configuration command sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = int(status) << bit_position
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=2),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_tofpet_config_register_command_ram_address(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for address in range(0, 2**9):
        window.spinBox_TOFPET_CONF_ADDR.setValue(address)
        qtbot.mouseClick(window.pushButton_TOPFET_CONF, QtCore.Qt.LeftButton)
        pattern = 'TOFPET configuration command sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = address << 8
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=2),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_link_control_register_send_command_mode(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    widget = window.comboBox_TOFPET_CONF_MODE

    #check number of TOFPETs
    assert widget.count() == 4

    modes = ['All registers', 'Global register',
             'All channel registers', 'Channel register selected']

    for mode in range(0, 4):
        print("mode: ", mode)
        # choose channel and check widget properties
        widget.setCurrentIndex(mode)
        assert widget.currentIndex() == mode
        assert widget.currentText()  == modes[mode]
        expected_bitarray = bitarray('{:02b}'.format(mode))
        assert widget.currentData() == expected_bitarray

        qtbot.mouseClick(window.pushButton_TOPFET_CONF, QtCore.Qt.LeftButton)
        pattern = 'TOFPET configuration command sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = mode << 6
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=2),
                          expected_value]
        }
        check_expected_response(cmd, expected_response)


def test_tofpet_config_register_command_ch_sel(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for address in range(0, 2**6):
        window.spinBox_TOFPET_CONF_CH_SEL.setValue(address)

        qtbot.mouseClick(window.pushButton_TOPFET_CONF, QtCore.Qt.LeftButton)
        pattern = 'TOFPET configuration command sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 1
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = address
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=2),
                          expected_value]
        }
        check_expected_response(cmd, expected_response)


import petalo_daq.mock_server.binary_responses as srv_cmd

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
                 (((1 << 31), 'PWR_STATUS_CONF_DONE'),
                  ((1 << 30), 'PWR_STATUS_CONF_ON'),
                  ((1 << 18), 'PWR_STATUS_18DIS'),
                  ((1 << 17), 'PWR_STATUS_25EN_1'),
                  ((1 << 16), 'PWR_STATUS_25EN_2'),
                  ((1 << 15), 'PWR_STATUS_TOFPET_VCCEN_7'),
                  ((1 << 14), 'PWR_STATUS_TOFPET_VCCEN_6'),
                  ((1 << 13), 'PWR_STATUS_TOFPET_VCCEN_5'),
                  ((1 << 12), 'PWR_STATUS_TOFPET_VCCEN_4'),
                  ((1 << 11), 'PWR_STATUS_TOFPET_VCCEN_3'),
                  ((1 << 10), 'PWR_STATUS_TOFPET_VCCEN_2'),
                  ((1 <<  9), 'PWR_STATUS_TOFPET_VCCEN_1'),
                  ((1 <<  8), 'PWR_STATUS_TOFPET_VCCEN_0'),

                  ((1 <<  7), 'PWR_STATUS_TOFPET_VCC25EN_7'),
                  ((1 <<  6), 'PWR_STATUS_TOFPET_VCC25EN_6'),
                  ((1 <<  5), 'PWR_STATUS_TOFPET_VCC25EN_5'),
                  ((1 <<  4), 'PWR_STATUS_TOFPET_VCC25EN_4'),
                  ((1 <<  3), 'PWR_STATUS_TOFPET_VCC25EN_3'),
                  ((1 <<  2), 'PWR_STATUS_TOFPET_VCC25EN_2'),
                  ((1 <<  1), 'PWR_STATUS_TOFPET_VCC25EN_1'),
                  ( 1       , 'PWR_STATUS_TOFPET_VCC25EN_0')))
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
