from bitarray  import bitarray
from time import sleep
from subprocess import check_output

from . worker import Worker
from . worker import WorkerSignals

from . channel_config import Config_update_ch
from . main           import start_run
from . main           import stop_run

# dispatch
from .. io.utils              import read_bitarray_into_namedtuple
from .. io.command_dispatcher import add_function_to_dispatcher
from .. io.command_dispatcher import check_command_dispatcher
from .. io.command_dispatcher import read_hw_response_from_log
from .. gui.types import dispatchable_fn
from .. gui.types import dispatch_type
from .. gui.types import CommandDispatcherException
from datetime import datetime


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """

    window.pushButton_calibrate.clicked.connect(execute_procedure(window))


def execute_procedure(window):
    """
    Function to execute the specified procedure taking different runs

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        window.update_log_info("Calibration",
                               "Running calibration procedure")


        def fn_procedure(signals):
            take_run = take_runs_automatically(window, signals)
            procedure = window.plainTextEdit_calibration.toPlainText()
            print("executing procedure")
            print(locals())
            print(procedure)
            try:
                exec(procedure)
            except Exception as e:
                window.plainTextEdit_calibrationLog.insertPlainText(repr(e))

        worker = Worker(fn_procedure)
        worker.signals.progress .connect(print_progress(window))
        worker.signals.ch_config.connect(config_channels_and_send_cmd(window))
        worker.signals.start_run.connect(start_run(window))
        worker.signals.stop_run .connect(stop_run (window))
        window.threadpool.start(worker)

    return on_click


def print_progress(window):
    def fn(status):
        window.plainTextEdit_calibrationLog.insertPlainText(status)
    return fn


def get_run_number():
    cmd = 'ssh dateuser@ldc1petalo.ific.uv.es cat /tmp/date_runnumber.txt'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()
    return run_number

def stop_DATE():
    cmd = 'ssh dateuser@ldc1petalo.ific.uv.es /home/dateuser/scripts/stopDate.sh'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()


# for channel in range(0, 5):
#    take_run(locals())

#  for channel in range(0, 5):
#     for vth_t1 in range(0, 4):
#         take_run(locals())


#  for channel in range(0, 5):
#     for vth_t1 in range(0, 4):
#        for vth_t2 in range(0, 3):
#            take_run(locals())


def config_run(window, params, signals):
    run_number = get_run_number()
    run_config = f"{run_number}"

    config = {} # dict {GUI setter fn -> value}

    for key, value in params.items():
        if key in ['procedure', 'take_run', 'window', 'signals', 'channels']:
            continue
        print(key, value)

        run_config += f", {value}"
        if key == 'channel':
            widget = window.spinBox_ch_number
            config[widget.setValue] = value
            continue

        # Find widget
        try:
            field_name = f'comboBox_{key}'
            widget = getattr(window, field_name)
            config[widget.setCurrentIndex] = value
        except:
            try:
                field_name = f'spinBox_{key}'
                widget = getattr(window, field_name)
                config[widget.setValue] = value
            except:
                raise ValueError(f"Variable {key} not found")

    signals.progress.emit(run_config + '\n')
    signals.ch_config.emit(config)


def config_channels_and_send_cmd(window):
    def fn(config):
        print(config)
        for key, value in config.items():
            key(value)
        # Send ch config
        Config_update_ch(window)()
    return fn


def take_runs_automatically(window, signals):
    def on_click(params):
        print("take_run: ", params)
        if 'channels' in params:
            for channel in params['channels']:
                print("channel: ", channel)
                params['channel'] = channel
                config_run(window, params, signals)
        else:
            config_run(window, params, signals)
        signals.start_run.emit()
        sleep(10)
        signals.stop_run.emit()
        sleep(2)
        stop_DATE()
        sleep(10)

    return on_click
