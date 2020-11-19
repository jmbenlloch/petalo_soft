from petalo_daq.daq.commands import commands as cmd
from petalo_daq.daq.commands import status_codes   as status
from petalo_daq.daq.commands import register_tuple
from petalo_daq.gui.types    import LogError

from petalo_daq.daq.process_responses import read_temperature
from petalo_daq.daq.process_responses import power_regulator_status


def check_write_response(window, cmd, params):
    status_code = params[0]
    if isinstance(status_code, status):
        raise LogError("{} register error {}".format(cmd.name, status_code.name))


response_functions = {
    cmd.SOFT_REG_W_r: check_write_response,
    cmd.HARD_REG_W_r: check_write_response,
    cmd.SOFT_REG_R_r : {
        register_tuple(2, 0): read_temperature,
        register_tuple(2, 1): read_temperature,
        register_tuple(2, 2): read_temperature,
        register_tuple(2, 3): read_temperature,
        register_tuple(2, 4): read_temperature,
        register_tuple(2, 5): read_temperature,
        register_tuple(2, 6): read_temperature,
        register_tuple(2, 7): read_temperature,
        register_tuple(2, 8): read_temperature,
    }
    cmd.SOFT_REG_R_r : {
        register_tuple(1, 1): power_regulator_status,
    }
}


def read_network_responses(window):
    while not window.stopper.is_set():
        message = window.rx_queue.get()
        if message:
            response_str = 'Response:\n'
            for key, value in message.items():
                response_str += f'\t{key}: {value}\n'
            window.plainTextEdit_cmdResponse.insertPlainText(f'{response_str}\n')

            try:
                cmd      = message['command']
                register = message['params' ][0]
                fn = response_functions[cmd]
                if isinstance(fn, dict):
                    fn = fn[register]
                fn(window, cmd, message['params'])
            except KeyError as e:
                print("Function to process {} not found. ".format(register), e)
            except LogError as e:
                window.update_log_info("", str(e))
