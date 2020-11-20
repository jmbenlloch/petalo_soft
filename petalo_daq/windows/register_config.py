from bitarray  import bitarray
import numpy as np

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.gui.widget_data  import temperature_data
from petalo_daq.gui.types        import temperature_config_tuple
from petalo_daq.io.config_params import temperature_config_fields

from petalo_daq.gui.widget_data  import power_control_data
from petalo_daq.gui.types        import power_control_tuple
from petalo_daq.io.config_params import power_control_fields

from petalo_daq.io.utils         import insert_bitarray_slice
from petalo_daq.io.config_params import range_inclusive

from petalo_daq.daq.client_commands import build_hw_register_write_command
from petalo_daq.daq.client_commands import build_sw_register_read_command
from petalo_daq.daq.client_commands import build_hw_register_read_command
from petalo_daq.daq.commands        import register_tuple
from petalo_daq.daq.commands        import sleep_cmd
from petalo_daq.daq.process_responses import temperature_tofpet_to_ch


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_Temp_hw_reg .clicked.connect(config_temperature(window))
    window.pushButton_Temp_read   .clicked.connect(read_temperature  (window))
    window.pushButton_Power_hw_reg.clicked.connect(power_control     (window))
    window.pushButton_Power_status_hw_reg.clicked.connect(power_status(window))
    window.pushButton_Clock_status_hw_reg.clicked.connect(clock_status(window))
    window.pushButton_Link_status_hw_reg.clicked .connect(link_status(window))


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

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)
        #window.tx_queue.put(sleep_cmd(700))

        window.update_log_info("Temperature config",
                               "Temperature configuration sent")

    return on_click


def read_temperature(window):
    """
    Function to read temperature sensors.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        # Read temperature values
        daq_id = 0
        for tofpet_id in range(9):
            print("tofpet_id: ", tofpet_id)
            channel = temperature_tofpet_to_ch[tofpet_id]
            command = build_sw_register_read_command(daq_id, register_group=2, register_id=channel)
            window.tx_queue.put(command)
            window.tx_queue.put(sleep_cmd(500))

        window.update_log_info("Temperature config",
                               "Temperature configuration sent")

    return on_click


def power_control(window):
    """
    Function to update the power configuration.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        power_control_bitarray = bitarray(32)

        power_config = read_parameters(window, power_control_data, power_control_tuple)

        for field, positions in power_control_fields.items():
            print(field)
            value = getattr(power_config, field)
            print(field, positions, value)
            insert_bitarray_slice(power_control_bitarray, positions, value)

        #fill unused bits
        insert_bitarray_slice(power_control_bitarray,
                              range_inclusive(19, 28),
                              bitarray('0000000000'))

        window.data_store.insert('power_control', power_control_bitarray)

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=1, id=0)
        print(power_control_bitarray)
        value = int(power_control_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value, hex(value))

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)

        window.update_log_info("PWR control sent",
                               "Power control register sent")

    return on_click


def power_status(window):
    """
    Function to read the power status register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        daq_id = 0
        command = build_hw_register_read_command(daq_id, register_group=1, register_id=1)
        window.tx_queue.put(command)

        window.update_log_info("Power status sent",
                               "Power status command sent")

    return on_click


def clock_status(window):
    """
    Function to read the clock status register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        daq_id = 0
        command = build_hw_register_read_command(daq_id, register_group=2, register_id=2)
        window.tx_queue.put(command)

        window.update_log_info("Clock status sent",
                               "Clock status command sent")

    return on_click


def link_status(window):
    """
    Function to read the link status register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        daq_id = 0
        command = build_hw_register_read_command(daq_id, register_group=3, register_id=1)
        window.tx_queue.put(command)

        window.update_log_info("Link status sent",
                               "Link status command sent")

    return on_click

