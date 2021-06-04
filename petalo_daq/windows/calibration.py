from bitarray  import bitarray

from . worker import Worker
from . worker import WorkerSignals
from . worker import Calibration

from . worker_tpulse import Worker        as tpulse_worker
from . worker_tpulse import WorkerSignals as tpulse_signals
from . worker_tpulse import channel_calib_tuple

from . global_config  import Config_update_glob
from . channel_config import Config_update_ch
from . main           import start_run
from . main           import stop_run
from . tpulse_config  import tpulse_config
from . tpulse_config  import tpulse_send_pulse
from . tpulse_config  import tpulse_continous_mode
from . tpulse_config  import tpulse_limited_time

from .. network.commands import sleep_cmd

from time import sleep


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """

    window.pushButton_calibrate       .clicked.connect(execute_procedure(window))
    window.pushButton_calibrate_tpulse.clicked.connect(execute_tpulse_procedure(window))


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

###############
### TPULSE  ###
###############

def execute_tpulse_procedure(window):
    def on_click():
        window.update_log_info("TPULSE Calibration",
                               "Running TPULSE calibration procedure")

        def fn_procedure(self, signals):
            procedure = window.plainTextEdit_calibration.toPlainText()
            self.window = window
            self.started = False
            try:
                exec(procedure)
            except Exception as e:
                window.plainTextEdit_calibrationLog.insertPlainText(repr(e))

        worker = tpulse_worker(fn_procedure)
        worker.signals.progress      .connect(print_progress(window))
        worker.signals.tpulse_config .connect(config_tpulse_send_cmd(window, worker.signals))
        worker.signals.channel_config.connect(config_tpulse_channels_and_send_cmd(window, worker.signals))
        worker.signals.start_run     .connect(start_tpulse_run(window, worker.signals))
        worker.signals.stop_run      .connect(stop_run (window))

        worker.signals.config_done        .connect(conf_done_signal_ack(worker))
        worker.signals.data_taken        .connect(data_taken_signal_ack(worker))
        window.threadpoolCalibration.start(worker)

    return on_click


def config_tpulse_send_cmd(window, signals):
    # actually set the values in the GUI (config: {setter -> value})
    def fn(config):
        for key, value in config.items():
            key(value)
        tpulse_config(window)()

        # Put conf_done signal in the queue
        window.tx_queue.put(signals.config_done)

    return fn


def config_tpulse_channels_and_send_cmd(window, signals):
    # Disable all channels but one, setting it to TPULSE trigger
    # actually set the values in the GUI (config: {setter -> value})
    def fn(config):
        # Disable all channels
        window.checkBox_all_ch.setChecked(True)
        window.spinBox_ASIC_n_2.setValue(config.asic)
        window.comboBox_trigger_mode_1.setCurrentIndex(3)
        Config_update_ch(window)

        sleep(0.5)

        # Enable only the selected channel
        window.checkBox_all_ch.setChecked(False)
        window.spinBox_ch_number.setValue(config.channel)
        window.spinBox_ASIC_n_2.setValue(config.asic)
        window.comboBox_trigger_mode_1.setCurrentIndex(1) # tpulse

        # Set the simplest trigger (T1)
        window.comboBox_trigger_mode_2_b.setCurrentIndex(0)
        window.comboBox_trigger_mode_2_e.setCurrentIndex(0)
        window.comboBox_trigger_mode_2_q.setCurrentIndex(0)
        window.comboBox_trigger_mode_2_t.setCurrentIndex(0)

        if config.mode == 'qdc':
            window.comboBox_qdc_mode      .setCurrentIndex(0)
            window.comboBox_intg_en       .setCurrentIndex(0)
            window.comboBox_intg_signal_en.setCurrentIndex(0)
        if config.mode == 'tot':
            window.comboBox_qdc_mode      .setCurrentIndex(1)
            window.comboBox_intg_en       .setCurrentIndex(1)
            window.comboBox_intg_signal_en.setCurrentIndex(1)

        Config_update_ch(window)
        sleep(0.1)

        # Set calibration mode to activate TPULSE
        window.comboBox_RUN_MODE.setCurrentIndex(2)

        # Put conf_done signal in the queue
        window.tx_queue.put(signals.config_done)

    return fn


def start_tpulse_run(window, signals):
    def fn():
        window.comboBox_RUN_MODE.setCurrentIndex(2)
        start_run(window)()
        #  for _ in range(10):
        #      # send 10 pulses
        #      tpulse_send_pulse(window)()

        #  window.checkBox_TPULSE_Continous.setChecked(True)
        #  tpulse_continous_mode(window)()
        #  sleep(1/10)
        #  window.checkBox_TPULSE_Continous.setChecked(False)

        tpulse_limited_time(window)()
        #  tpulse_continous_mode(window)()

        # Put data_taken_signal_ack signal in the queue
        window.tx_queue.put(signals.data_taken)

    return fn

def data_taken_signal_ack(worker):
    def ack():
        worker.data_taken = True
    return ack

