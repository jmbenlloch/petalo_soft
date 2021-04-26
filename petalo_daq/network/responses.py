from .  commands import commands       as cmd
from .  commands import status_codes   as status
from .  commands import register_tuple

from . process_responses import read_temperature
from . process_responses import power_regulator_status
from . process_responses import clock_status
from . process_responses import link_status
from . process_responses import run_status
from . process_responses import tofpet_status
from . process_responses import leds_status
from . process_responses import check_connection
from . process_responses import tpulse_status

from .. gui.types             import LogError
from .. io.command_dispatcher import add_response_to_dispatcher_log
from .. io.command_dispatcher import check_command_dispatcher


def check_write_response(window, cmd, params):
    status_code = params[0]
    if isinstance(status_code, status):
        raise LogError("{} register error {}".format(cmd.name, status_code.name))


response_functions = {
    cmd.CON_STATUS  : check_connection,
    cmd.SOFT_REG_W_r: check_write_response,
    cmd.HARD_REG_W_r: check_write_response,
    cmd.SOFT_REG_R_r : {
        register_tuple(1, 0): leds_status,
        register_tuple(2, 0): read_temperature,
        register_tuple(2, 1): read_temperature,
        register_tuple(2, 2): read_temperature,
        register_tuple(2, 3): read_temperature,
        register_tuple(2, 4): read_temperature,
        register_tuple(2, 5): read_temperature,
        register_tuple(2, 6): read_temperature,
        register_tuple(2, 7): read_temperature,
        register_tuple(2, 8): read_temperature,
        register_tuple(3, 0): tpulse_status,
        register_tuple(3, 1): tpulse_status,
        register_tuple(3, 2): tpulse_status,
        register_tuple(3, 3): tpulse_status,
    },
    cmd.HARD_REG_R_r : {
        register_tuple(1, 1): power_regulator_status,
        register_tuple(2, 2): clock_status,
        register_tuple(3, 1): link_status,
        register_tuple(3, 4): tofpet_status,
        register_tuple(4, 1): run_status,
    },
}


def read_network_responses(window):
    while not window.rx_stopper.is_set():
        message = window.rx_queue.get()
        if message:
            response_str = 'Response:\n'
            for key, value in message.items():
                response_str += f'\t{key}: {value}\n'
            window.plainTextEdit_cmdResponse.insertPlainText(f'{response_str}\n')

            print("Netword response: ", message)
            try:
                cmd      = message['command']
                register = message['params' ][0]
                fn = response_functions[cmd]
                #  print(cmd, register, fn)
                if isinstance(fn, dict):
                    fn = fn[register]
                # add response to Command dispatcher log
                add_response_to_dispatcher_log(window, register, message)

                # process response
                fn(window, cmd, message['params'])

                # check command dispatcher
                check_command_dispatcher(window)
            except KeyError as e:
                print("Function to process {} not found. ".format(register), e)
            except LogError as e:
                window.update_log_info("", str(e))
