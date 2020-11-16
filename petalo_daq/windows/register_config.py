from bitarray  import bitarray
import numpy as np

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.gui.widget_data  import temperature_data
from petalo_daq.gui.types        import temperature_config_tuple
from petalo_daq.io.config_params import temperature_config_fields
from petalo_daq.io.utils         import insert_bitarray_slice

from petalo_daq.daq.client_commands import build_hw_register_write_command
from petalo_daq.daq.commands        import register_tuple



def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_Temp_hw_reg.clicked.connect(config_temperature(window))


def config_temperature(window):
    """
    Function to update the Temperature sensor configuration.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        temperature_bitarray = bitarray(32)

        # ASIC parameters to be update
        print(temperature_config_tuple)
        temperature_config = read_parameters(window, temperature_data, temperature_config_tuple)

        # Convert time
        time_ns            = temperature_config.Temp_Time
        discretized_value  = np.round(time_ns / 40).astype(np.int32)
        binary_value       = '{:020b}'.format(discretized_value)
        time_bitarray      = bitarray(binary_value.encode())
        temperature_config = temperature_config._replace(Temp_Time = time_bitarray)

        for field, positions in temperature_config_fields.items():
            print(field)
            value = getattr(temperature_config, field)
            print(field, positions, value)
            insert_bitarray_slice(temperature_bitarray, positions, value)

        window.data_store.insert('temperature_config', temperature_bitarray)

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=0, id=0)
        print(temperature_bitarray)
        value = int(temperature_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        window.update_log_info("Temperature config",
                               "Temperature configuration sent")

    return on_click
