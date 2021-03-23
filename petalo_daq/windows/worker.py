from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRunnable

import traceback, sys

from time       import sleep
from subprocess import check_output
from enum       import Enum, auto

from .. database.mongo_db import get_run_number

# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/


class Calibration(Enum):
    config_done = auto()


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
    finished = pyqtSignal()
    error    = pyqtSignal(tuple)
    result   = pyqtSignal(object)
    progress = pyqtSignal(object)
    ch_config = pyqtSignal(object)
    start_run = pyqtSignal()
    stop_run  = pyqtSignal()
    config_done  = pyqtSignal()
    separator_run = pyqtSignal()
    separator_run_taken = pyqtSignal()


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
            print("running")
            result = self.fn(self, *self.args, **self.kwargs)
            print(self.generator)
            print(self.window)
            self.conf_done = True
            self.finished = False
            self.iteration = 0
            while not self.finished:
                if self.conf_done:
                    self.take_runs_automatically_with_signals()
                sleep(1./100.)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


    def initialize_run(self):
        # For each config, for each channel -> take data
        print_run_number(self.window, self.signals)
        self.current_channels  = self.channels.copy()
        self.params = next(self.generator)


    def take_runs_automatically_with_signals(self):
        print("Executing take runs")
        try:
            params = next(self.generator)
            if params == Calibration.config_done:
                # Add label for DB
                labels = self.window.data_store.retrieve('labels')
                labels['separator'] = False
                labels['iteration'] = self.iteration
                self.window.data_store.insert('labels', labels)
                self.iteration += 1

                self.signals.start_run.emit()
                sleep(2)
                self.signals.stop_run.emit()
                self.signals.separator_run.emit()
            else:
                config_run(self.window, params, self.signals)
                self.conf_done = False
        except StopIteration:
            # If there are no more configs in the generator -> Stop the run
            stop_DATE()
            self.finished = True
            self.window.data_store.insert('labels', {})


def print_run_number(window, signals):
    run_number = get_run_number()
    run_config = f"{run_number}"
    signals.progress.emit(run_config + '\n')


def config_run(window, params, signals):
    config = {} # dict {GUI setter fn -> value}

    # Channel must be the first parameter
    channel = params.pop('channel')
    widget  = window.spinBox_ch_number
    config[widget.setValue] = channel
    run_config = f"{channel}"

    for key, value in params.items():
        run_config += f", {value}"

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


def stop_DATE():
    cmd = 'ssh dateuser@ldc1petalo.ific.uv.es /home/dateuser/scripts/stopDate.sh'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()
