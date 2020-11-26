import sys
import os
import threading
from datetime import datetime
from PyQt5    import QtWidgets
from PyQt5    import uic


import petalo_daq.gui.utils              as gui
import petalo_daq.windows.main           as window_main
import petalo_daq.windows.general        as window_general
import petalo_daq.windows.global_config  as window_global
import petalo_daq.windows.channel_config as window_channel
import petalo_daq.windows.register_config as window_register
import petalo_daq.windows.commands       as window_commands


from petalo_daq.gui.widget_data  import global_data
from petalo_daq.gui.widget_data  import channel_data
from petalo_daq.gui.widget_data  import general_data
from petalo_daq.gui.widget_data  import temperature_data
from petalo_daq.gui.widget_data  import power_control_data
from petalo_daq.gui.widget_data  import run_control_data
from petalo_daq.gui.widget_data  import lmk_control_data
from petalo_daq.gui.widget_data  import clock_control_data
from petalo_daq.gui.widget_data  import tofpet_config_data
from petalo_daq.gui.access_level import user_access
from petalo_daq.io.data_store    import DataStore
from petalo_daq.io.configuration import load_configuration_file



from petalo_daq.daq.petalo_network import SCK_TXRX
from petalo_daq.daq.responses      import read_network_responses
from queue     import Queue, Empty
from threading import Thread, Event


qtCreatorFile = "PETALO_v2.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class PetaloRunConfigurationGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
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
        gui.populate_fields(self, tofpet_config_data)

        # Data store
        self.data_store = DataStore()

        # Load default config file
        default_config = os.environ['PETALO_DAQ_DIR'] + '/petalo_daq/config/default.json'
        load_configuration_file(self, default_config)

        #Button Calls
        window_main   .connect_buttons(self)
        window_general.connect_buttons(self)
        window_global .connect_buttons(self)
        window_channel.connect_buttons(self)
        window_commands.connect_buttons(self)

        window_register.connect_buttons(self)

        # Disable everything before authentication
        window_main.validate_pass(self)()

        # Socket
        cfg_data = {'port'           :9116,
                    'buffer_size'    :1024,
                    'localhost'      :'127.0.0.1',
                    'ext_ip'         :'127.0.0.1',
                   }

        self.tx_queue = Queue()
        self.rx_queue = Queue()
        self.stopper  = Event()

        try:
            self.thread_TXRX  = SCK_TXRX(cfg_data,self.tx_queue,self.rx_queue,self.stopper)
            self.thread_TXRX.daemon = True
            self.thread_TXRX.start()
        except ConnectionRefusedError as e:
            self.update_log_info("Connection error", str(e))

        rx_consumer = threading.Thread(target=read_network_responses, args=(self,))
        rx_consumer.daemon = True
        rx_consumer.start()


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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PetaloRunConfigurationGUI()
    window.show()
    sys.exit(app.exec_())
