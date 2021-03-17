import sys
import os
import threading
from datetime import datetime
from PyQt5    import QtWidgets
from PyQt5    import uic
from PyQt5.QtCore    import QThreadPool


import petalo_daq.gui.utils              as gui
import petalo_daq.windows.main           as window_main
import petalo_daq.windows.general        as window_general
import petalo_daq.windows.global_config  as window_global
import petalo_daq.windows.channel_config as window_channel
import petalo_daq.windows.register_config as window_register
import petalo_daq.windows.commands       as window_commands
import petalo_daq.windows.calibration    as window_calibration


from petalo_daq.gui.widget_data  import global_data
from petalo_daq.gui.widget_data  import channel_data
from petalo_daq.gui.widget_data  import general_data
from petalo_daq.gui.widget_data  import temperature_data
from petalo_daq.gui.widget_data  import power_control_data
from petalo_daq.gui.widget_data  import run_control_data
from petalo_daq.gui.widget_data  import lmk_control_data
from petalo_daq.gui.widget_data  import link_control_data
from petalo_daq.gui.widget_data  import clock_control_data
from petalo_daq.gui.widget_data  import tofpet_config_data
from petalo_daq.gui.widget_data  import tofpet_config_value_data
from petalo_daq.gui.access_level import user_access
from petalo_daq.io.data_store    import DataStore
from petalo_daq.io.configuration import load_configuration_file
from petalo_daq.io.configuration import load_channel_config_from_yml


from petalo_daq.io.command_dispatcher import initialize_command_dispatcher

from petalo_daq.network.petalo_network import SCK_TXRX
from petalo_daq.network.responses      import read_network_responses
from queue     import Queue, Empty
from threading import Thread, Event


qtCreatorFile = "PETALO_v2.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def connect_server(window):
    localhost = window.textBrowser_Localhost    .toPlainText()
    server    = window.textBrowser_Petalo_server.toPlainText()
    cfg_data = {'port'        : 9116,
                'buffer_size' : 1024,
                'localhost'   : localhost,
                'ext_ip'      : server,
               }

    try:
        window.tx_stopper.set()
        window.thread_TXRX.join()
    except:
        pass
    window.tx_stopper.clear()

    # Empty cmd queue
    for i in range(window.tx_queue.unfinished_tasks):
        window.tx_queue.get(i)
        window.tx_queue.task_done()

    try:
        window.thread_TXRX  = SCK_TXRX(cfg_data,window.tx_queue,window.rx_queue,window.tx_stopper)
        window.thread_TXRX.daemon = True
        window.thread_TXRX.start()
    except ConnectionRefusedError as e:
        window.update_log_info("Connection error", str(e))


class PetaloRunConfigurationGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, test_mode=False):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Add data to all fields and set default values
        gui.populate_fields(self, global_data)
        gui.populate_fields(self, general_data)
        gui.populate_fields(self, channel_data)

        gui.populate_fields(self, temperature_data)
        gui.populate_fields(self, power_control_data)
        gui.populate_fields(self, run_control_data)
        gui.populate_fields(self, clock_control_data)
        gui.populate_fields(self, lmk_control_data)
        gui.populate_fields(self, link_control_data)
        gui.populate_fields(self, tofpet_config_data)
        gui.populate_fields(self, tofpet_config_value_data)

        # Data store
        self.data_store = DataStore()
        self.data_store.insert('labels', {}) # labels for the run in DB

        # QT thread pool
        self.threadpoolCalibration = QThreadPool()
        self.threadpoolCalibration.setMaxThreadCount(1)
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)

        # Initialize command dispatcher
        initialize_command_dispatcher(self)

        # Load default config file
        default_config = os.environ['PETALO_DAQ_DIR'] + '/petalo_daq/config/default.json'
        load_configuration_file(self, default_config)

        # Load channels config
        load_channel_config_from_yml(self)
        window_channel.update_channel_config(self)() # read gui config for default channel

        #Button Calls
        window_main   .connect_buttons(self)
        window_general.connect_buttons(self)
        window_global .connect_buttons(self)
        window_channel.connect_buttons(self)
        window_commands.connect_buttons(self)
        window_calibration.connect_buttons(self)

        window_register.connect_buttons(self)

        # Disable everything before authentication
        self.pass_lineEdit.setText("Petalo")
        window_main.validate_pass(self)()

        if test_mode:
            self.textBrowser_Localhost    .setText('127.0.0.1')
            self.textBrowser_Petalo_server.setText('127.0.0.1')

        self.tx_queue = Queue()
        self.rx_queue = Queue()
        self.tx_stopper = Event()
        self.rx_stopper = Event()

        self.rx_consumer = threading.Thread(target=read_network_responses, args=(self,))
        self.rx_consumer.daemon = True
        self.rx_consumer.start()

        connect_server(self)

        self.pushButton_Connect.clicked.connect(lambda: connect_server(self))


    def update_log_info(self, status, message):
        """
        Method to write messages in the application log and status fields

        The GUI has two text fields to present the status and log information.
        The first one should be a short message and will be printed in the "current
        status" field. The second one can be as long as needed and will be printed
        in the extended log field.

        Parameters:
        status (string): Message for Current status.
        message (string): Extended log message.

        Returns:
        None: The is no return value
        """
        self.textBrowser.append(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.textBrowser.append(message + '\n')
        self.Log.setText(status)
        # set scroll to the end
        scrollbar = self.textBrowser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    print (sys.argv)
    test_mode = False
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '-test'):
            test_mode = True
    window = PetaloRunConfigurationGUI(test_mode=test_mode)
    window.show()
    sys.exit(app.exec_())
