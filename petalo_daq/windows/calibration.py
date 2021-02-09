from bitarray  import bitarray
from time import sleep
from subprocess import check_output

from . worker import Worker
from . worker import WorkerSignals

from . utils import write_to_lmk_ram

from .. gui.utils        import read_parameters
from .. io.config_params import reverse_range_inclusive

from . register_config           import power_status
from . register_config           import clock_status
from . register_config           import link_status

from .. io.config_params import link_status_fields
from .. gui.types        import link_status_tuple

from .. gui.widget_data  import activate_data
from .. gui.types        import activate_tuple

from .. gui.types        import power_status_tuple
from .. io.config_params import power_status_fields

from .. gui.types        import clock_status_tuple
from .. io.config_params import clock_status_fields

from .. io.utils         import insert_bitarray_slice

from .. network.client_commands import build_hw_register_write_command
from .. network.client_commands import build_sw_register_write_command
from .. network.client_commands import build_sw_register_read_command
from .. network.commands        import register_tuple
from .. network.commands        import sleep_cmd
from .. network.process_responses import temperature_tofpet_to_ch
from .. network.process_responses import convert_int32_to_bitarray


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


        def fn_procedure():
            take_run = take_runs_automatically(window)
            procedure = window.plainTextEdit_calibration.toPlainText()
            print("executing procedure")
            print(procedure)
            try:
                exec(procedure)
            except Exception as e:
                window.plainTextEdit_calibrationLog.insertPlainText(repr(e))

        worker = Worker(fn_procedure)
        #  worker.signals.result.connect(fn_procedure)
        window.threadpool.start(worker)

    return on_click

def get_run_number():
    cmd = 'sshpass -pdate.123 ssh dateuser@ldc1petalo.ific.uv.es cat /tmp/date_runnumber.txt'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()
    return run_number

def update_ch_number(window):
    def fn(channel):
        window.spinBox_ch_number.setValue(channel)
    window.plainTextEdit_calibrationLog.insertPlainText(status)
    return fn

# for channel in range(0, 5):
#    take_run(locals())

#  for channel in range(0, 5):
#     for vth_t1 in range(0, 4):
#         take_run(locals())


#  for channel in range(0, 5):
#     for vth_t1 in range(0, 4):
#        for vth_t2 in range(0, 3):
#            take_run(locals())


def config_run(window, params):
    def to_dispatch():
        run_number = get_run_number()
        run_config = f"{run_number}"

        for key, value in params.items():
            if key in ['procedure', 'take_run', 'window']:
                continue

            run_config += f", {value}"
            if key == 'channel':
                #  window.spinBox_ch_number.setValue(value)
                continue

            # Find widget
            try:
                field_name = f'comboBox_{key}'
                print(field_name)
                widget = getattr(window, field_name)
                #  widget.setCurrentIndex(value)
            except:
                try:
                    field_name = f'spinBox_{key}'
                    print(field_name)
                    widget = getattr(window, field_name)
                    #  widget.setValue(value)
                except:
                    raise ValueError(f"Variable {key} not found")

        #window.plainTextEdit_calibrationLog.insertPlainText(run_config + "\n")
        print(run_config + "\n")
        #  WorkerSignals.progress.emit(run_config)
        print("emitted")

    return to_dispatch


def take_runs_automatically(window):
    def on_click(params):
        window.plainTextEdit_calibrationLog.insertPlainText("Start config\n")

        config_run(window, params)()

        #  fn = dispatchable_fn(type = dispatch_type.function,
        #                       condition_fn = None,
        #                       fn = fn)
        #  add_function_to_dispatcher(window, fn)

        #  check_command_dispatcher(window)

    return on_click

