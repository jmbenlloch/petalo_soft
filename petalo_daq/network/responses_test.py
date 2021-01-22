from time      import sleep
from pytest    import raises
from PETALO_v7 import PetaloRunConfigurationGUI

from .. gui.types                 import LogError
from .. network.commands          import commands
from .. network.commands          import status_codes
from .. network.responses         import check_write_response
from .. testing.utils             import check_pattern_present_in_log
from .. testing.utils             import close_connection


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

