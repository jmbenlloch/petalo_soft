from bitarray  import bitarray

from . worker import Worker
from . worker import WorkerSignals
from . worker import Calibration

from . worker_qdc    import QDC_Worker    as qdc_worker
from . worker_qdc    import WorkerSignals as qdc_signals
from . worker_tpulse import channel_calib_tuple

from . calibration_utils import print_progress

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
import numpy as np


def execute_tpulse_qdc_procedure(window):
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

        # Start run
        start_qdc_tpulse_run(window)

        worker = qdc_worker(fn_procedure)
        worker.signals.progress      .connect(print_progress(window))
        worker.signals.stop_run      .connect(stop_run_with_signal  (window, worker.signals))
        worker.signals.run_stopped   .connect(run_stopped_signal_ack(worker))

        worker.signals.channel_config.connect(config_tpulse_channels_and_send_cmd(window, worker.signals))
        worker.signals.channel_ready .connect(channel_ready_signal_ack           (worker))

        worker.signals.tpulse_config .connect(config_tpulse_and_take_data(window, worker.signals))
        worker.signals.tpulse_done   .connect(tpulse_done_signal_ack(worker))

        window.threadpoolCalibration.start(worker)

    return on_click


def stop_run_with_signal(window, signals):
    def fn():
        print("main stopping run")
        stop_run(window)()
        window.tx_queue.put(signals.run_stopped)
    return fn


def run_stopped_signal_ack(worker):
    def ack():
        print("stopped ack signal")
        worker.new_channel = True
    return ack


def config_tpulse_and_take_data(window, signals):
    # actually set the values in the GUI (config: {setter -> value})
    def fn(config):
        for key, value in config.items():
            key(value)
        tpulse_config(window)()

        # Take data
        tpulse_limited_time(window)()

        # Put tpulse_done signal in the queue
        window.tx_queue.put(signals.tpulse_done)

    return fn


def config_tpulse_channels_and_send_cmd(window, signals):
    # Disable all channels but one, setting it to TPULSE trigger
    # actually set the values in the GUI (config: {setter -> value})
    def fn(params):
        config = params['configuration']
        # Disable all channels
        if params['disable_all_channels']:
            window.checkBox_all_ch.setChecked(True)
        window.spinBox_ASIC_n_2.setValue(config.asic)
        window.comboBox_trigger_mode_1.setCurrentIndex(3)
        Config_update_ch(window)()

        sleep(0.5)

        # Open the integration window
        window.spinBox_min_intg_time.setValue(0)
        window.spinBox_max_intg_time.setValue(127)

        # Enable only the selected channel
        if params['disable_all_channels']:
            window.checkBox_all_ch.setChecked(False)
        window.spinBox_ch_number.setValue(config.channel)
        window.spinBox_ASIC_n_2.setValue(config.asic)
        window.comboBox_trigger_mode_1.setCurrentIndex(1) # tpulse

        # Set the simplest trigger (T1)
        window.comboBox_trigger_mode_2_b.setCurrentIndex(0)
        window.comboBox_trigger_mode_2_e.setCurrentIndex(0)
        window.comboBox_trigger_mode_2_q.setCurrentIndex(0)
        window.comboBox_trigger_mode_2_t.setCurrentIndex(0)

        # Set QDC mode
        window.comboBox_qdc_mode      .setCurrentIndex(0)
        window.comboBox_intg_en       .setCurrentIndex(0)
        window.comboBox_intg_signal_en.setCurrentIndex(0)

        Config_update_ch(window)()
        sleep(0.1)

        # Set calibration mode to activate TPULSE
        window.comboBox_RUN_MODE.setCurrentIndex(2)
        window.comboBox_TOFPET_LINK_SEL_MUX.setCurrentIndex(config.asic)

        # Start run
        start_qdc_tpulse_run(window)

        # Put channel_ready signal in the queue
        print("main send channel ready")
        window.tx_queue.put(signals.channel_ready)

    return fn


def channel_ready_signal_ack(worker):
    def ack():
        print("channel ready ack")
        worker.channel_ready = True
    return ack


def start_qdc_tpulse_run(window):
    window.comboBox_RUN_MODE.setCurrentIndex(2)
    start_run(window)()


def tpulse_done_signal_ack(worker):
    def ack():
        print("main tpulse done ack")
        worker.channel_ready = True
    return ack

