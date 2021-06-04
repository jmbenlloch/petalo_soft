from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRunnable

import traceback, sys

from time       import sleep
from subprocess import check_output
from enum       import Enum, auto

from . worker import Calibration

from .. database.mongo_db import get_run_number

# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/

from collections import namedtuple

channel_calib_tuple  = namedtuple('channel_calib_tuple' , ['channel', 'asic', 'mode'])


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything
    '''
    finished       = pyqtSignal()
    error          = pyqtSignal(tuple)
    result         = pyqtSignal(object)
    progress       = pyqtSignal(object)
    start_run      = pyqtSignal()
    stop_run       = pyqtSignal()
    config_done    = pyqtSignal()
    tpulse_config  = pyqtSignal(object)
    channel_config = pyqtSignal(object)
    data_taken     = pyqtSignal()


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


        # Add the callback to our kwargs
        #  self.kwargs['progress_callback'] = self.signals.progress
        #  self.kwargs['ch_config_callback'] = self.signals.ch_config
        self.kwargs['signals'] = self.signals


    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(self, *self.args, **self.kwargs)

            self.conf_sent  = False
            self.conf_done  = False
            self.data_taken = False
            self.finished   = False
            self.iteration = 0
            while not self.finished:
                if not self.conf_sent:
                    self.conf_sent = self.send_next_configuration()
                if self.conf_done:
                    self.take_runs_automatically_with_signals()
                    self.conf_done = False
                if self.data_taken:
                    sleep(2)
                    self.signals.stop_run.emit()
                    self.data_taken = False
                    self.conf_sent  = False
                sleep(1)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


    def send_next_configuration(self):
        ready_for_data = False # only True when channel and TPULSE are setup
        try:
            params = next(self.generator)
            if isinstance(params, channel_calib_tuple):
                print("Configuring channnel")
                # configure channels
                # channel_calib_tuple :
                #    channel : int
                #    asic    : int
                #    mode    : 'qdc' or 'tot'
                config_channels(self.window, params, self.signals)
                ready_for_data = False
            else:
                print("Configuring tpulse")
                config_tpulse(self.window, params, self.signals)
                ready_for_data = True
        except StopIteration:
            # If there are no more configs in the generator -> Stop the run
            stop_DATE()
            self.finished = True
            self.window.data_store.insert('labels', {})

        return ready_for_data


    def take_runs_automatically_with_signals(self):
        # Add label for DB
        labels = self.window.data_store.retrieve('labels')
        labels['iteration'] = self.iteration
        self.window.data_store.insert('labels', labels)
        self.iteration += 1

        self.signals.start_run.emit()


def print_run_number(window, signals):
    run_number = get_run_number()
    run_config = f"{run_number}"
    signals.progress.emit(run_config + '\n')


def config_tpulse(window, params, signals):
    config = {} # dict {GUI setter fn -> value}

    # Set phase
    widget  = window.spinBox_TPULSE_Phase
    config[widget.setValue] = params['phase']

    # Set length up
    widget  = window.spinBox_TPULSE_Length_Up
    config[widget.setValue] = params['length_up']

    # Set length down
    widget  = window.spinBox_TPULSE_Length_Down
    config[widget.setValue] = params['length_down']

    run_config = "{}, {}".format(params['phase'], params['length_up'], params['length_down'])

    signals.progress.emit(run_config + '\n')
    signals.tpulse_config.emit(config)


def config_channels(window, params, signals):
    run_config = "Configuring channel {} of ASIC {} in {} mode".format(params.channel, params.asic, params.mode)
    signals.progress.emit(run_config + '\n')
    signals.channel_config.emit(params)


def stop_DATE():
    cmd = 'ssh dateuser@ldc1petalo.ific.uv.es /home/dateuser/scripts/stopDate.sh'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()
