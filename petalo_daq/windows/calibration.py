from bitarray  import bitarray

from . worker import Worker
from . worker import WorkerSignals
from . worker import Calibration

from . global_config  import Config_update_glob
from . channel_config import Config_update_ch
from . main           import start_run
from . main           import stop_run

from .. network.commands import sleep_cmd

from time import sleep


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

        def fn_procedure(self, signals):
            procedure = window.plainTextEdit_calibration.toPlainText()
            print("executing procedure")
            print(locals())
            print(procedure)
            self.window = window
            self.started = False
            try:
                exec(procedure)
            except Exception as e:
                window.plainTextEdit_calibrationLog.insertPlainText(repr(e))

        worker = Worker(fn_procedure)
        worker.signals.progress .connect(print_progress(window))
        worker.signals.ch_config.connect(config_channels_and_send_cmd(window, worker.signals))
        worker.signals.start_run.connect(start_run(window))
        worker.signals.stop_run .connect(stop_run (window))

        worker.signals.config_done        .connect(conf_done_signal_ack(worker))
        window.threadpoolCalibration.start(worker)

    return on_click


def conf_done_signal_ack(worker):
    def ack():
        print("ack signal")
        worker.conf_done = True
    return ack


def print_progress(window):
    def fn(status):
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


def config_channels_and_send_cmd(window, signals):
    # actually set the values in the GUI (config: {setter -> value})
    def fn(config):
        print(config)
        for key, value in config.items():
            key(value)
        # Send ch config
        Config_update_ch(window)()

        # Put conf_done signal in the queue
        window.tx_queue.put(signals.config_done)

    return fn
