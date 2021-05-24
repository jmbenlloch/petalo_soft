from time      import sleep
from PyQt5     import QtCore
from pytest    import mark
from PETALO_v7 import PetaloRunConfigurationGUI
from .. network.commands          import register_tuple
from .. network.petalo_network    import MESSAGE
from .. network.commands          import commands
from .. testing.utils             import check_pattern_present_in_log
from .. network.command_test      import check_expected_response

import petalo_daq.mock_server.binary_responses as srv_cmd


def test_tofpet_tpulse_status_locked_gui(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for i in range(0, 8):
        cmd = srv_cmd.build_sw_register_read_response(daq_id=0, register_group=3, register_id=0, value=i, error_code=None)
        message = MESSAGE()
        cmd = message(cmd)
        print(cmd)

        window.rx_queue.put(cmd)
        sleep(0.1)

        widget = getattr(window, 'checkBox_TPULSE_Locked')
        assert widget.isChecked() == (i > 0)


def test_tofpet_tpulse_status_continous_gui(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for i in range(0, 8):
        cmd = srv_cmd.build_sw_register_read_response(daq_id=0, register_group=3, register_id=3, value=i, error_code=None)
        message = MESSAGE()
        cmd = message(cmd)
        print(cmd)

        window.rx_queue.put(cmd)
        sleep(0.1)

        widget = getattr(window, 'checkBox_TPULSE_Continous_status')
        assert widget.isChecked() == (i > 0)


def test_tofpet_tpulse_status_length_up_gui(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for i in range(0, 128):
        cmd = srv_cmd.build_sw_register_read_response(daq_id=0, register_group=3, register_id=2, value=i, error_code=None)
        message = MESSAGE()
        cmd = message(cmd)
        print(cmd)

        window.rx_queue.put(cmd)
        sleep(0.1)

        widget = getattr(window, 'spinBox_TPULSE_Length_Up_status')
        assert widget.text() == str(i)


def test_tofpet_tpulse_status_length_down_gui(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for i in range(0, 128):
        cmd = srv_cmd.build_sw_register_read_response(daq_id=0, register_group=3, register_id=6, value=i, error_code=None)
        message = MESSAGE()
        cmd = message(cmd)
        print(cmd)

        window.rx_queue.put(cmd)
        sleep(0.1)

        widget = getattr(window, 'spinBox_TPULSE_Length_Down_status')
        assert widget.text() == str(i)


def test_tofpet_tpulse_status_phase_gui(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for i in range(0, 128):
        cmd = srv_cmd.build_sw_register_read_response(daq_id=0, register_group=3, register_id=1, value=i, error_code=None)
        message = MESSAGE()
        cmd = message(cmd)
        print(cmd)

        window.rx_queue.put(cmd)
        sleep(0.1)

        widget = getattr(window, 'spinBox_TPULSE_Phase_status')
        assert widget.text() == str(i)


def test_tpulse_status_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TPULSE_status, QtCore.Qt.LeftButton)
    pattern = 'TPULSE status command sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    # Four registers must be read to check the TPULSE status
    assert window.tx_queue.qsize() == 4

    for i in range(4):
        cmd_binary = window.tx_queue.get(0)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_response = {
            'command'  : commands.SOFT_REG_R,
            'L1_id'    : 0,
            'n_params' : 1,
            'params'   : [register_tuple(group=3, id=i)]
        }

        check_expected_response(cmd, expected_response)


def test_tpulse_reset_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TPULSE_Reset, QtCore.Qt.LeftButton)
    pattern = 'Reset TPULSE sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1

    cmd_binary = window.tx_queue.get(0)
    message    = MESSAGE()
    cmd        = message(cmd_binary)

    expected_value = 0
    expected_response = {
        'command'  : commands.SOFT_REG_W,
        'L1_id'    : 0,
        'n_params' : 2,
        'params'   : [register_tuple(group=3, id=0), expected_value]
    }

    check_expected_response(cmd, expected_response)


def test_tpulse_limited_time_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TPULSE_LimitedTime, QtCore.Qt.LeftButton)
    pattern = 'TPULSE continous mode for 1ms'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1

    cmd_binary = window.tx_queue.get(0)
    message    = MESSAGE()
    cmd        = message(cmd_binary)

    expected_value = 0
    expected_response = {
        'command'  : commands.SOFT_REG_W,
        'L1_id'    : 0,
        'n_params' : 2,
        'params'   : [register_tuple(group=3, id=5), expected_value]
    }

    check_expected_response(cmd, expected_response)


def test_tpulse_sendpulse_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.pushButton_TPULSE_SendPulse, QtCore.Qt.LeftButton)
    pattern = 'TPULSE signal sent'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1

    cmd_binary = window.tx_queue.get(0)
    message    = MESSAGE()
    cmd        = message(cmd_binary)

    expected_value = 0
    expected_response = {
        'command'  : commands.SOFT_REG_W,
        'L1_id'    : 0,
        'n_params' : 2,
        'params'   : [register_tuple(group=3, id=4), expected_value]
    }

    check_expected_response(cmd, expected_response)


@mark.parametrize(('continous'),
                 (True, False))
def test_tpulse_continous_send_command(qtbot, continous):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    widget = getattr(window, "checkBox_TPULSE_Continous")
    widget.setChecked(continous)

    qtbot.mouseClick(window.pushButton_TPULSE_Continous, QtCore.Qt.LeftButton)
    pattern = 'TPULSE continous mode updated'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1

    cmd_binary = window.tx_queue.get(0)
    message    = MESSAGE()
    cmd        = message(cmd_binary)

    expected_value = int(continous)
    expected_response = {
        'command'  : commands.SOFT_REG_W,
        'L1_id'    : 0,
        'n_params' : 2,
        'params'   : [register_tuple(group=3, id=3), expected_value]
    }

    check_expected_response(cmd, expected_response)


def test_tpulse_config_length_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for length in range(0, 127):
        window.spinBox_TPULSE_Length.setValue(length)

        qtbot.mouseClick(window.pushButton_TPULSE_Config, QtCore.Qt.LeftButton)
        pattern = 'TPULSE config sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 2

        _          = window.tx_queue.get(0)
        cmd_binary = window.tx_queue.get(1)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value = length
        expected_response = {
            'command'  : commands.SOFT_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=2), expected_value]
        }
        check_expected_response(cmd, expected_response)


def test_tpulse_config_phase_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    for length in range(0, 200):
        window.spinBox_TPULSE_Phase.setValue(length)

        qtbot.mouseClick(window.pushButton_TPULSE_Config, QtCore.Qt.LeftButton)
        pattern = 'TPULSE config sent'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 3

        cmd_binary = window.tx_queue.get(0)
        _          = window.tx_queue.get(1)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value = length
        expected_response = {
            'command'  : commands.SOFT_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=3, id=1), expected_value]
        }
        check_expected_response(cmd, expected_response)

