from bitarray  import bitarray
import numpy as np

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.gui.widget_data  import temperature_data
from petalo_daq.gui.types        import temperature_config_tuple
from petalo_daq.io.config_params import temperature_config_fields

from petalo_daq.gui.widget_data  import power_control_data
from petalo_daq.gui.types        import power_control_tuple
from petalo_daq.io.config_params import power_control_fields

from petalo_daq.gui.widget_data  import clock_control_data
from petalo_daq.gui.types        import clock_control_tuple
from petalo_daq.io.config_params import clock_control_fields

from petalo_daq.gui.widget_data  import lmk_control_data
from petalo_daq.gui.types        import lmk_control_tuple
from petalo_daq.io.config_params import lmk_control_fields

from petalo_daq.gui.widget_data  import link_control_data
from petalo_daq.gui.types        import link_control_tuple
from petalo_daq.io.config_params import link_control_fields

from petalo_daq.gui.widget_data  import tofpet_config_value_data
from petalo_daq.gui.types        import tofpet_config_value_tuple
from petalo_daq.io.config_params import tofpet_config_value_fields

from petalo_daq.gui.widget_data  import tofpet_config_data
from petalo_daq.gui.types        import tofpet_config_tuple
from petalo_daq.io.config_params import tofpet_config_fields

from petalo_daq.gui.widget_data  import leds_status_data
from petalo_daq.gui.types        import leds_status_tuple
from petalo_daq.io.config_params import leds_status_fields

from petalo_daq.io.utils         import insert_bitarray_slice
from petalo_daq.io.config_params import range_inclusive

from petalo_daq.daq.client_commands import build_hw_register_write_command
from petalo_daq.daq.client_commands import build_sw_register_read_command
from petalo_daq.daq.client_commands import build_hw_register_read_command
from petalo_daq.daq.commands        import register_tuple
from petalo_daq.daq.commands        import sleep_cmd
from petalo_daq.daq.process_responses import temperature_tofpet_to_ch
from petalo_daq.windows.utils       import tofpet_status


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
    window.pushButton_Power_status_hw_reg .clicked.connect(power_status(window))
    window.pushButton_Clock_status_hw_reg .clicked.connect(clock_status(window))
    window.pushButton_Link_status_hw_reg  .clicked.connect(link_status(window))
    window.pushButton_Clock_control_hw_reg.clicked.connect(clock_control(window))
    window.pushButton_Clock_LMK_hw_reg    .clicked.connect(lmk_control(window))
    window.pushButton_TOFPET_LINK_CONTROL .clicked.connect(link_control(window))
    window.pushButton_TOFPET_STATUS       .clicked.connect(tofpet_status(window))
    window.pushButton_TOPFET_CONF_VALUE   .clicked.connect(tofpet_config_value(window))
    window.pushButton_TOPFET_CONF         .clicked.connect(tofpet_config(window))
    window.pushButton_LEDs_read           .clicked.connect(read_leds(window))


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
        power_control_bitarray = bitarray('0'*32)

        power_config = read_parameters(window, power_control_data, power_control_tuple)

        for field, positions in power_control_fields.items():
            print(field)
            value = getattr(power_config, field)
            print(field, positions, value)
            insert_bitarray_slice(power_control_bitarray, positions, value)

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


def clock_control(window):
    """
    Function to write the clock control register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        clock_bitarray = bitarray('0'*32)

        # ASIC parameters to be update
        clock_control = read_parameters(window, clock_control_data, clock_control_tuple)

        for field, positions in clock_control_fields.items():
            value = getattr(clock_control, field)
            insert_bitarray_slice(clock_bitarray, positions, value)

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=2, id=0)
        print(clock_bitarray)
        value = int(clock_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("Clock control sent",
                               "Clock control command sent")

    return on_click


def lmk_control(window):
    """
    Function to write the clock control register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        lmk_bitarray = bitarray('0'*32)

        # ASIC parameters to be update
        lmk_control = read_parameters(window, lmk_control_data, lmk_control_tuple)
        print(lmk_control)

        # Convert address and value to bitarray
        lmk_address          = lmk_control.LMK_REG_ADD
        lmk_address_binary   = '{:07b}'.format(lmk_address)
        lmk_address_bitarray = bitarray(lmk_address_binary.encode())

        lmk_value          = lmk_control.LMK_REG_VALUE
        lmk_value_binary   = '{:08b}'.format(lmk_value)
        lmk_value_bitarray = bitarray(lmk_value_binary.encode())

        lmk_control = lmk_control._replace(LMK_REG_ADD   = lmk_address_bitarray,
                                           LMK_REG_VALUE = lmk_value_bitarray )


        for field, positions in lmk_control_fields.items():
            value = getattr(lmk_control, field)
            print(field, positions, value)
            insert_bitarray_slice(lmk_bitarray, positions, value)

        #fill bit 31
        insert_bitarray_slice(lmk_bitarray, [31], bitarray('1'))

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=2, id=1)
        print(lmk_bitarray)
        value = int(lmk_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("LMK control sent",
                               "LMK control command sent")

    return on_click


def link_control(window):
    """
    Function to write the link control register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        link_bitarray = bitarray('0'*32)

        # ASIC parameters to be update
        link_control = read_parameters(window, link_control_data, link_control_tuple)

        for field, positions in link_control_fields.items():
            value = getattr(link_control, field)
            insert_bitarray_slice(link_bitarray, positions, value)

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=0)
        print(link_bitarray)
        value = int(link_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("Link control sent",
                               "Link control command sent")

    return on_click


def tofpet_config_value(window):
    """
    Function to write the TOFPET configuration value register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        config_bitarray = bitarray('0'*32)

        # ASIC parameters to be update
        tofpet_config_value = read_parameters(window, tofpet_config_value_data, tofpet_config_value_tuple)

        binary_value        = '{:032b}'.format(tofpet_config_value.TOPFET_CONF_VALUE)
        value_bitarray      = bitarray(binary_value.encode())
        tofpet_config_value = tofpet_config_value._replace(TOPFET_CONF_VALUE = value_bitarray)

        for field, positions in tofpet_config_value_fields.items():
            value = getattr(tofpet_config_value, field)
            insert_bitarray_slice(config_bitarray, positions, value)

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=3)
        print(config_bitarray)
        value = int(config_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("TOFPET config value sent",
                               "TOFPET configuration value sent")

    return on_click


def tofpet_config(window):
    """
    Function to write the TOFPET configuration register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        config_bitarray = bitarray('0'*32)

        # ASIC parameters to be update
        tofpet_config = read_parameters(window, tofpet_config_data, tofpet_config_tuple)

        address_binary   = '{:09b}'.format(tofpet_config.TOFPET_CONF_ADDR)
        address_bitarray = bitarray(address_binary.encode())
        tofpet_config    = tofpet_config._replace(TOFPET_CONF_ADDR = address_bitarray)

        channel_binary   = '{:06b}'.format(tofpet_config.TOFPET_CONF_CH_SEL)
        channel_bitarray = bitarray(channel_binary.encode())
        tofpet_config    = tofpet_config._replace(TOFPET_CONF_CH_SEL = channel_bitarray)

        print(tofpet_config)

        for field, positions in tofpet_config_fields.items():
            value = getattr(tofpet_config, field)
            print(field, positions, value)
            insert_bitarray_slice(config_bitarray, positions, value)

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=2)
        print(config_bitarray)
        value = int(config_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value)

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("TOFPET config sent",
                               "TOFPET configuration command sent")

    return on_click


def read_leds(window):
    """
    Function to read the leds status register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        daq_id = 0
        command = build_sw_register_read_command(daq_id, register_group=1, register_id=0)
        window.tx_queue.put(command)

        window.update_log_info("LEDs status sent",
                               "LEDs status command sent")

    return on_click
