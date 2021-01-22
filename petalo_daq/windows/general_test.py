import numpy as np

from pytest import mark
from time   import sleep
from PyQt5  import QtCore

from PETALO_v7 import PetaloRunConfigurationGUI


from .. network    .commands          import commands
from .. network    .commands          import sleep_cmd
from .. mock_server.binary_responses  import build_sw_register_read_response
from .. network    .petalo_network    import MESSAGE
from .. network    .process_responses import temperature_tofpet_to_ch
from .. testing    .utils             import check_pattern_present_in_log
from .. testing    .utils             import close_connection

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
    cmd = build_sw_register_read_response(daq_id=0, register_group=1, register_id=0, value=value, error_code=None)
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
        cmd = build_sw_register_read_response(daq_id=0, register_group=1, register_id=0,
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
