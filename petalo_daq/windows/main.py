import numpy as np
from bitarray import bitarray

from .. gui.utils        import read_parameters
from .. gui.utils        import enable_fields
from .. gui.utils        import path_browser_config
from .. io.utils         import insert_bitarray_slice
from .. io.configuration import load_configuration_file
from .. io.config_params import link_control_fields
#from .. database         import database as db
#from .. io.config_params import global_config_fields
#from .. io.config_params import channel_config_fields

from .. gui.widget_data  import run_control_data
from .. gui.types        import run_control_tuple
from .. io.config_params import run_control_fields

from .. network.client_commands   import build_hw_register_write_command
from .. network.commands          import register_tuple
from .. network.process_responses import convert_bitarray_to_int

from .. database.mongo_db import store_configuration_in_db



def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    json_file_select = path_browser_config(window,
                                           'Register data (*.json)',
                                           'lineEdit_config_file_path')
    window.toolButton_config.clicked.connect(json_file_select)
    window.pushButton_load.clicked.connect(lambda : load_configuration_file(window, window.lineEdit_config_file_path.text()))

    window.pushButton_config.clicked.connect(lambda: window.data_store.export_to_json('/tmp/test.json'))

    window.START.clicked.connect(start_run(window))
    window.STOP .clicked.connect(stop_run (window))

    window.pass_lineEdit.editingFinished.connect(validate_pass(window))


def start_run(window):
    """
    Function to start the run logging the configuration in the database

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        store_configuration_in_db(window)
        #TODO: Store properly database connection info, daq_id, asic_id
        # connect to database
        #  db_connector, db_cursor = db.mysql_connect('localhost', 'root', 'root', 'petalo')
        #
        #  # write run number to DB
        #  latest_run = db.get_latest_run_number(db_cursor)
        #  run_number = latest_run + 1
        #  db.insert_run_number(db_connector, db_cursor, run_number)
        #
        #  # write global config to DB
        #  daq_id  = 0
        #  asic_id = 0
        #  global_config = window.data_store.retrieve('global_config')
        #  db.insert_global_config(db_connector, db_cursor, run_number,
        #                          daq_id, asic_id, global_config, global_config_fields)
        #
        #  # write channel config to DB
        #  daq_id  = 0
        #  asic_id = 0
        #  channel_id = 0
        #  channel_config = window.data_store.retrieve('channel_config')
        #  db.insert_channel_config(db_connector, db_cursor, run_number,
        #                          daq_id, asic_id, channel_id,
        #                          channel_config[0], channel_config_fields)

        # Synchronize TOFPETs before starting the run
        send_sync_rst(window)

        run_control_bitarray = bitarray('0'*32) # initialize to zero all 32 bits
        run_control_config = read_parameters(window, run_control_data, run_control_tuple)

        evt_time           = run_control_config.RUN_Event
        discretized_value  = np.round(evt_time / 2**16 * 125e3).astype(np.int32)
        # check for overflow
        if discretized_value > 0x0FFFF:
            discretized_value = 0x0FFFF
        binary_value       = '{:016b}'.format(discretized_value)
        evt_time_bitarray  = bitarray(binary_value.encode())
        run_control_config = run_control_config._replace(RUN_Event = evt_time_bitarray)

        throughput          = run_control_config.RUN_Throughput
        discretized_value   = np.round(throughput * 2**20 / 2**16).astype(np.int32)
        binary_value        = '{:011b}'.format(discretized_value)
        throughput_bitarray = bitarray(binary_value.encode())
        run_control_config  = run_control_config._replace(RUN_Throughput = throughput_bitarray)

        for field, positions in run_control_fields.items():
            value = getattr(run_control_config, field)
            insert_bitarray_slice(run_control_bitarray, positions, value)

        # Set Start bit to 1
        insert_bitarray_slice(run_control_bitarray, [31], [1])

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=4, id=0)
        print(run_control_bitarray)
        value = int(run_control_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)

        window.update_log_info("The run is ongoing", "Run has started")

    return on_click


def stop_run(window):
    """
    Function to stop the run

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        run_control_bitarray = bitarray('0'*32) # initialize to zero all 32 bits
        run_control_config = read_parameters(window, run_control_data, run_control_tuple)

        evt_time           = run_control_config.RUN_Event
        discretized_value  = np.round(evt_time / 2**16 * 125e3).astype(np.int32)
        binary_value       = '{:016b}'.format(discretized_value)
        evt_time_bitarray  = bitarray(binary_value.encode())
        run_control_config = run_control_config._replace(RUN_Event = evt_time_bitarray)

        throughput          = run_control_config.RUN_Throughput
        discretized_value   = np.round(throughput * 2**20 / 2**16).astype(np.int32)
        binary_value        = '{:011b}'.format(discretized_value)
        throughput_bitarray = bitarray(binary_value.encode())
        run_control_config  = run_control_config._replace(RUN_Throughput = throughput_bitarray)

        print(run_control_config)
        for field, positions in run_control_fields.items():
            value = getattr(run_control_config, field)
            insert_bitarray_slice(run_control_bitarray, positions, value)

        # Set Start bit to 1
        insert_bitarray_slice(run_control_bitarray, [30], [1])

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=4, id=0)
        value = int(run_control_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)

        window.update_log_info('The run is stopped', 'The run is stopped')

    return on_click


def validate_pass(window):
    """
    Function authenticate user and enable fields according to the corresponding
    access level.

    Parameters:
    window (PetaloRunConfigurationGUI): QApplication

    Returns
    function: To be triggered on click
    """

    def on_click():
        password = window.pass_lineEdit.text()

        if password == "Petalo":
            window.update_log_info('Superuser access', 'Access as superuser')
            user = 'admin'
            enable_fields(window, user)

        elif password == "Shifter":
            window.update_log_info('Shifter access', 'Access as shifter')
            user = 'shifter'
            enable_fields(window, user)

        else:
            window.update_log_info('Wrong password', 'Wrong password')
            user = 'none'
            enable_fields(window, user)

    return on_click


def send_sync_rst(window):
    # Activate SYNC RST
    register_value = 1 << link_control_fields['SYNC_RST'][-1]

    # configure DDR mode
    ddr_mode = 1 if window.checkBox_DDR.isChecked() else 0
    register_value = register_value | (ddr_mode << link_control_fields['DDR'][-1])

    # Configure number of cycles
    rst_cycles = 20
    register_value = register_value | (rst_cycles << link_control_fields['RST_CYCLES'][-1])

    # Set ASIC number
    sel_mux_value = convert_bitarray_to_int(window.comboBox_TOFPET_LINK_SEL_MUX.currentData())
    register_value = register_value | sel_mux_value

    # Send command
    daq_id   = 0x0000
    register = register_tuple(group=3, id=0)
    command  = build_hw_register_write_command(daq_id, register.group, register.id, register_value)
    window.tx_queue.put(command)
