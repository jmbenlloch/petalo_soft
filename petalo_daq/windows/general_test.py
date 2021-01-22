from pytest import mark
from time   import sleep
from PyQt5  import QtCore

from PETALO_v7 import PetaloRunConfigurationGUI

from .. testing.utils             import check_pattern_present_in_log

from .. network    .commands         import commands
from .. mock_server.binary_responses import build_sw_register_read_response
from .. network    .petalo_network   import MESSAGE

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

