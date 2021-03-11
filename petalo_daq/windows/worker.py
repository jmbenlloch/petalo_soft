from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRunnable

import traceback, sys

from time import sleep
from subprocess import check_output

# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/

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

        self.signals.config_done.connect(take_run_wrapper_for_signal(self))

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
            self.take_runs_automatically_with_signals()
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
        if not self.started:
            self.started = True
            self.initialize_run()

        try:
            channel = self.current_channels.pop(0)
            self.params['channel'] = channel
            config_run(self.window, self.params, self.signals)
        except IndexError:
            self.signals.start_run.emit()
            sleep(2)
            self.signals.stop_run.emit()
            sleep(2)
            stop_DATE()
            sleep(10)
            # Prepare for next configuration
            try:
                # Get next config and make recursive call
                self.initialize_run()
                self.take_runs_automatically_with_signals()
            except StopIteration:
                # If no more configurations, finish
                pass


def take_run_wrapper_for_signal(worker):
    def on_signal():
        print("signal received")
        worker.take_runs_automatically_with_signals()
    return on_signal


def print_run_number(window, signals):
    run_number = get_run_number()
    run_config = f"{run_number}"
    signals.progress.emit(run_config + '\n')


def config_run(window, params, signals):
    run_config = ""
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


def get_run_number():
    cmd = 'ssh dateuser@ldc1petalo.ific.uv.es cat /tmp/date_runnumber.txt'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()
    return run_number


def stop_DATE():
    cmd = 'ssh dateuser@ldc1petalo.ific.uv.es /home/dateuser/scripts/stopDate.sh'
    cmd_out = check_output(cmd, shell=True, executable='/bin/bash')
    run_number = cmd_out.decode()
