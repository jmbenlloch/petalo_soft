from bitarray  import bitarray

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.gui.widget_data  import global_data
from petalo_daq.gui.types        import global_config_tuple
from petalo_daq.io.config_params import global_config_fields


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_reg_glob.clicked.connect(Config_update_glob(window))
    #  window.checkBox_all_ASIC.clicked.connect()


def Config_update_glob(window):
    """
    Function to update the Global ASIC configuration.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        global_bitarray = bitarray()

        # ASIC parameters to be update
        global_config = read_parameters(window, global_data, global_config_tuple)

        for field, positions in global_config_fields.items():
            print(field)
            global_bitarray[positions] = getattr(global_config, field)

        #fill unused bits
        global_bitarray[ 16: 18] = bitarray('00')
        global_bitarray[ 31: 32] = bitarray('0')
        global_bitarray[176:178] = bitarray('00')

        window.data_store.insert('global_config', global_bitarray)

        window.update_log_info("Global register configured",
                               "Global ASIC registers conf")

    return on_click
