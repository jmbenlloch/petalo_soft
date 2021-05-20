import numpy as np

from pytest   import mark
from PyQt5    import QtCore
from bitarray import bitarray

from .. network.commands          import commands
from .. network.commands          import register_tuple
from .. network.command_test      import check_expected_response
from .. network.petalo_network    import MESSAGE
from .. testing.utils             import check_pattern_present_in_log

from PETALO_v7 import PetaloRunConfigurationGUI


@mark.parametrize(('bit_position', 'field'),
                  ((27, 'RUN_THR_ON'),))
def test_start_run_register_send_command_boolean_fields(qtbot, bit_position, field):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # set the rest of fields to zero (their defaults are not zero)
    window.comboBox_RUN_MODE.setCurrentIndex(0)
    window.spinBox_RUN_Throughput.setValue(1)
    window.spinBox_RUN_Event     .setValue(1)
    throughtput_mask = 0x00100000
    time_mask        = 0x00000002

    for status in [True, False]:
        widget = getattr(window, f'checkBox_{field}')
        widget.setChecked(status)

        qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
        pattern = 'Run has started'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 2
        cmd_binary = window.tx_queue.get(0)
        cmd_binary = window.tx_queue.get(1)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    = 1 << 31 | (int(status) << bit_position) | throughtput_mask | time_mask
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=4, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_start_run_register_send_command_mode(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # set the rest of fields to zero (their defaults are not zero)
    window.spinBox_RUN_Throughput.setValue(1)
    window.spinBox_RUN_Event     .setValue(1)
    throughtput_mask = 0x00100000
    time_mask        = 0x00000002

    widget = window.comboBox_RUN_MODE

    #check number of TOFPETs
    assert widget.count() == 3

    modes = [
        {'index' : 0,
         'code'  : 0,
         'label' : 'QDC: Charge Integration'
        },
        {'index' : 1,
         'code'  : 1,
         'label' : 'TOT: Time Over Threshold'
        },
        {'index' : 2,
         'code'  : 3,
         'label' : 'Calibration: Event counter'
        },
    ]

    for mode in range(0, 2):
        # choose channel and check widget properties
        index = modes[mode]['index']
        widget.setCurrentIndex(index)
        assert widget.currentIndex() == index
        assert widget.currentText()  == modes[mode]['label']
        binary_code = '{:02b}'.format(modes[mode]['code'])
        expected_bitarray = bitarray(binary_code.encode())
        assert widget.currentData()  == expected_bitarray

        qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
        pattern = 'Run has started'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 2
        cmd_binary = window.tx_queue.get(0)
        cmd_binary = window.tx_queue.get(1)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        expected_value    =  (1 << 31) | (modes[mode]['code'] << 28) | throughtput_mask | time_mask
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=4, id=0),
                          expected_value]
        }

        check_expected_response(cmd, expected_response)


def test_start_run_register_send_command_throughput(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # set the rest of fields to a default value
    window.comboBox_RUN_MODE.setCurrentIndex(0)
    window.spinBox_RUN_Event.setValue(1)
    time_mask = 0x00000002

    for throughput in range(1, 81):
        window.spinBox_RUN_Throughput.setValue(throughput)

        qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
        pattern = 'Run has started'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 2
        cmd_binary = window.tx_queue.get(0)
        cmd_binary = window.tx_queue.get(1)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        discretized_value   = np.round(throughput * 2**20 / 2**16).astype(np.int32)
        if discretized_value > 0x0FFF:
            discretized_value = 0x0FFF

        expected_value    = 1 << 31 | (discretized_value << 16) | time_mask
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=4, id=0),
                          expected_value]
        }
        check_expected_response(cmd, expected_response)


def test_start_run_register_send_command_evt_time(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # set the rest of fields to a default value
    window.comboBox_RUN_MODE     .setCurrentIndex(0)
    window.spinBox_RUN_Throughput.setValue(1)
    throughtput_mask = 0x00100000


    # Range from 1 to 34360. Too many values. This test checks the
    # lower and upper part of the interval and some random values
    # in the middle.
    values_to_check_beginning = np.arange(1, 10)
    values_to_check_middle    = np.random.randint(10, 34350, 300)
    values_to_check_ending    = np.arange(34350, 34361)
    values_to_check = np.concatenate((values_to_check_beginning,
                                      values_to_check_middle,
                                      values_to_check_ending))

    for time in values_to_check:
        window.spinBox_RUN_Event.setValue(time)
        qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
        pattern = 'Run has started'
        check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

        assert window.tx_queue.qsize() == 2
        cmd_binary = window.tx_queue.get(0)
        cmd_binary = window.tx_queue.get(1)
        message    = MESSAGE()
        cmd        = message(cmd_binary)

        discretized_value   = np.round(time * 125e3 / 2**16).astype(np.int32)
        if discretized_value > 0x0FFFF:
            discretized_value = 0x0FFFF

        expected_value    = 1 << 31 | throughtput_mask | discretized_value
        expected_response = {
            'command'  : commands.HARD_REG_W,
            'L1_id'    : 0,
            'n_params' : 2,
            'params'   : [register_tuple(group=4, id=0),
                          expected_value]
        }
        check_expected_response(cmd, expected_response)


def test_start_run_send_sync_reset_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    qtbot.mouseClick(window.START, QtCore.Qt.LeftButton)
    pattern = 'Run has started'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 2
    cmd_binary = window.tx_queue.get(0)
    message    = MESSAGE()
    cmd        = message(cmd_binary)

    rst_cycles = 20
    expected_value    = (1 << 10) | (rst_cycles << 4)
    expected_response = {
        'command'  : commands.HARD_REG_W,
        'L1_id'    : 0,
        'n_params' : 2,
        'params'   : [register_tuple(group=3, id=0),
                      expected_value]
    }
    check_expected_response(cmd, expected_response)



def test_stop_run_register_send_command(qtbot):
    window = PetaloRunConfigurationGUI(test_mode=True)
    window.textBrowser.clear()

    # set the rest of fields to a default value
    window.comboBox_RUN_MODE.setCurrentIndex(0)
    window.spinBox_RUN_Throughput.setValue(1)
    window.spinBox_RUN_Event     .setValue(1)
    throughtput_mask = 0x00100000
    time_mask        = 0x00000002

    qtbot.mouseClick(window.STOP, QtCore.Qt.LeftButton)
    pattern = 'The run is stopped'
    check_pattern_present_in_log(window, pattern, expected_matches=1, escape=True)

    assert window.tx_queue.qsize() == 1
    cmd_binary = window.tx_queue.get(0)
    message    = MESSAGE()
    cmd        = message(cmd_binary)

    expected_value    = 1 << 30 | throughtput_mask | time_mask
    expected_response = {
        'command'  : commands.HARD_REG_W,
        'L1_id'    : 0,
        'n_params' : 2,
        'params'   : [register_tuple(group=4, id=0),
                      expected_value]
    }

    check_expected_response(cmd, expected_response)
