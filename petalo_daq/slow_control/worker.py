from ..windows.general import read_temperature

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRunnable

import traceback, sys
import schedule
import time


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
    temperature = pyqtSignal(object)


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

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.signals   = WorkerSignals()
        self.period    = kwargs['period']
        self.threshold = kwargs['threshold']
        self.window    = kwargs['window']
        self.monitor   = True

        self.signals.temperature.connect(self.temperature_threshold_alert)


    @pyqtSlot()
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            print("Running")
            schedule.every(self.period).seconds.do(read_temperature(self.window))
            while self.monitor:
                schedule.run_pending()
                time.sleep(1)
            print("Ending")

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()  # Done


    def temperature_threshold_alert(self, data):
        print("Alert: ", data)

        if (data.temperature > self.threshold):
            print("Temperature {} over threshold".format(data.temperature))
            turn_off_power_regulators(self.window)


from .. gui.widget_data   import power_control_data
from .. gui.types         import power_control_tuple
from .. io .config_params import power_control_fields
from .. io.utils          import insert_bitarray_slice
from .. network.commands  import register_tuple
from .. network.client_commands import build_hw_register_write_command

from bitarray import bitarray

def turn_off_power_regulators(window):
    power_control_bitarray = bitarray('0'*32)
    power_config = power_control_tuple(
        PWR_GStart           = bitarray('0'),
        PWR_Start            = bitarray('1'),
        PWR_RST              = bitarray('0'),
        PWR_18DIS            = bitarray('1'),
        PWR_25EN_1           = bitarray('0'),
        PWR_25EN_2           = bitarray('0'),
        PWR_TOFPET_VCCEN_7   = bitarray('0'),
        PWR_TOFPET_VCCEN_6   = bitarray('0'),
        PWR_TOFPET_VCCEN_5   = bitarray('0'),
        PWR_TOFPET_VCCEN_4   = bitarray('0'),
        PWR_TOFPET_VCCEN_3   = bitarray('0'),
        PWR_TOFPET_VCCEN_2   = bitarray('0'),
        PWR_TOFPET_VCCEN_1   = bitarray('0'),
        PWR_TOFPET_VCCEN_0   = bitarray('0'),
        PWR_TOFPET_VCC25EN_7 = bitarray('0'),
        PWR_TOFPET_VCC25EN_6 = bitarray('0'),
        PWR_TOFPET_VCC25EN_5 = bitarray('0'),
        PWR_TOFPET_VCC25EN_4 = bitarray('0'),
        PWR_TOFPET_VCC25EN_3 = bitarray('0'),
        PWR_TOFPET_VCC25EN_2 = bitarray('0'),
        PWR_TOFPET_VCC25EN_1 = bitarray('0'),
        PWR_TOFPET_VCC25EN_0 = bitarray('0'),
    )


    for field, positions in power_control_fields.items():
        value = getattr(power_config, field)
        insert_bitarray_slice(power_control_bitarray, positions, value)

    #Build command
    daq_id = 0x0000
    register = register_tuple(group=1, id=0)
    value = int(power_control_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2

    command = build_hw_register_write_command(daq_id, register.group, register.id, value)
    window.tx_queue.put(command)


