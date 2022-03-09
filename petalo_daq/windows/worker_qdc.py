from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRunnable

import traceback, sys

from time       import sleep
from subprocess import check_output
from enum       import Enum, auto

from . worker import Calibration
from . worker_tpulse import print_run_number
from . worker_tpulse import config_tpulse
from . worker_tpulse import config_channels
from . worker_tpulse import stop_DATE
from . worker_tpulse import channel_calib_tuple

from .. database.mongo_db import get_run_number

# https://www.learnpyqt.com/tutorials/multithreading-pyqt-applications-qthreadpool/

from collections import namedtuple


class WorkerSignals(QObject):
    finished       = pyqtSignal()
    error          = pyqtSignal(tuple)
    result         = pyqtSignal(object)
    progress       = pyqtSignal(object)
    stop_run       = pyqtSignal()
    run_stopped    = pyqtSignal()
    channel_config = pyqtSignal(object)
    channel_ready  = pyqtSignal()
    tpulse_config  = pyqtSignal(object)
    tpulse_done    = pyqtSignal()


class QDC_Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(QDC_Worker, self).__init__()

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

            self.finished      = False
            self.new_channel   = False
            self.channel_ready = False
            self.tpulse_ready  = False
            self.first_channel = True

            self.channel_config_sent = False

            self.next_config     = None

            while not self.finished:
                print("qdc loop")

                if not self.next_config:
                    print("next_config")
                    self.next_config = self.get_next_configuration()
                    print("config: ", self.next_config)
                    print("isinstance: ", isinstance(self.next_config, channel_calib_tuple))
                    if isinstance(self.next_config, channel_calib_tuple):
                       self.channel_ready = False
                       print("Configuring channnel")
                       # configure channels
                       # channel_calib_tuple :
                       #    channel : int
                       #    asic    : int
                       #    mode    : 'qdc' or 'tot'
                       self.signals.stop_run.emit()
                    if self.next_config == None:
                        break

                if self.new_channel:
                    print("worker new channel")
                    config_channels(self.window, self.next_config, self.signals, self.first_channel)
                    self.new_channel   = False
                    self.next_config   = None
                    self.first_channel = False

                if self.channel_ready and self.next_config:
                    print("worker channel_ready")
                    print(self.next_config)
                    config_tpulse(self.window, self.next_config, self.signals)
                    self.channel_ready = False
                    self.next_config   = None

                sleep(1)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

    def get_next_configuration(self):
        params = None
        try:
            params = next(self.generator)
        except StopIteration:
            print("End of process")
            # If there are no more configs in the generator -> Stop the run
            self.signals.stop_run.emit()
            stop_DATE()
            self.finished = True
            self.window.data_store.insert('labels', {})

        return params
