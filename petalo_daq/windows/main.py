import petalo_daq.gui.utils as gui

from petalo_daq.database         import database as db
from petalo_daq.io.configuration import load_configuration_file
from petalo_daq.io.config_params import global_config_fields
from petalo_daq.io.config_params import channel_config_fields


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    json_file_select = gui.path_browser_config(window,
                                           'Register data (*.json)',
                                           'lineEdit_config_file_path')
    window.toolButton_config.clicked.connect(json_file_select)
    window.pushButton_load.clicked.connect(lambda : load_configuration_file(window, window.lineEdit_config_file_path.text()))

    window.pushButton_config.clicked.connect(lambda: window.data_store.export_to_json('/tmp/test.json'))

    window.START.clicked.connect(Start_run(window))
    window.STOP .clicked.connect(Stop_run (window))

    window.pass_lineEdit.editingFinished.connect(validate_pass(window))


def Start_run(window):
    """
    Function to start the run logging the configuration in the database

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        #TODO: Store properly database connection info, daq_id, asic_id
        # connect to database
        db_connector, db_cursor = db.mysql_connect('localhost', 'root', 'root', 'petalo')

        # write run number to DB
        latest_run = db.get_latest_run_number(db_cursor)
        run_number = latest_run + 1
        db.insert_run_number(db_connector, db_cursor, run_number)

        # write global config to DB
        daq_id  = 0
        asic_id = 0
        global_config = window.data_store.retrieve('global_config')
        db.insert_global_config(db_connector, db_cursor, run_number,
                                daq_id, asic_id, global_config, global_config_fields)

        # write channel config to DB
        daq_id  = 0
        asic_id = 0
        channel_id = 0
        channel_config = window.data_store.retrieve('channel_config')
        db.insert_channel_config(db_connector, db_cursor, run_number,
                                daq_id, asic_id, channel_id,
                                channel_config[0], channel_config_fields)

        window.update_log_info("The run is ongoing", f"Run {run_number} has start")

    return on_click


def Stop_run(window):
    """
    Function to stop the run

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
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
            gui.enable_fields(window, user)

        elif password == "Shifter":
            window.update_log_info('Shifter access', 'Access as shifter')
            user = 'shifter'
            gui.enable_fields(window, user)

        else:
            window.update_log_info('Wrong password', 'Wrong password')
            user = 'none'
            gui.enable_fields(window, user)

    return on_click
