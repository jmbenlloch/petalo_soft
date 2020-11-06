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
import petalo_daq.windows.commands       as window_commands


from petalo_daq.gui.widget_data  import global_data
from petalo_daq.gui.widget_data  import channel_data
from petalo_daq.gui.widget_data  import general_data
from petalo_daq.gui.access_level import user_access
from petalo_daq.io.data_store    import DataStore
from petalo_daq.io.configuration import load_configuration_file



from petalo_daq.daq.petalo_network import SCK_TXRX
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

        # Data store
        self.data_store = DataStore()

        # Disable everything before authentication
        window_main.validate_pass(self)

        # Load default config file
        default_config = os.environ['PETALO_DAQ_DIR'] + '/petalo_daq/config/default.json'
        load_configuration_file(self, default_config)

        #Button Calls
        window_main   .connect_buttons(self)
        window_general.connect_buttons(self)
        window_global .connect_buttons(self)
        window_channel.connect_buttons(self)
        window_commands.connect_buttons(self)


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
        except ConnectionRefusedError:
            pass

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


def read_network_responses(window):
    while not window.stopper.is_set():
        message = window.rx_queue.get()
        if message:
            response_str = 'Response:\n'
            for key, value in message.items():
                response_str += f'\t{key}: {value}\n'
            window.plainTextEdit_cmdResponse.insertPlainText(f'{response_str}\n')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PetaloRunConfigurationGUI()
    window.show()
    sys.exit(app.exec_())
