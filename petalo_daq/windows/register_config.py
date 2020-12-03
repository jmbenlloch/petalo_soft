from bitarray  import bitarray
import numpy as np

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.gui.widget_data  import temperature_data
from petalo_daq.gui.types        import temperature_config_tuple
from petalo_daq.io.config_params import temperature_config_fields
from petalo_daq.io.config_params import reverse_range_inclusive

from petalo_daq.gui.widget_data  import power_control_data
from petalo_daq.gui.types        import power_control_tuple
from petalo_daq.io.config_params import power_control_fields

from petalo_daq.gui.types        import power_status_tuple
from petalo_daq.io.config_params import power_status_fields

from petalo_daq.gui.widget_data  import clock_control_data
from petalo_daq.gui.types        import clock_control_tuple
from petalo_daq.io.config_params import clock_control_fields

from petalo_daq.gui.widget_data  import clock_status_data
from petalo_daq.gui.types        import clock_status_tuple
from petalo_daq.io.config_params import clock_status_fields

from petalo_daq.gui.widget_data  import lmk_control_data
from petalo_daq.gui.types        import lmk_control_tuple
from petalo_daq.io.config_params import lmk_control_fields

from petalo_daq.gui.widget_data  import link_control_data
from petalo_daq.gui.types        import link_control_tuple
from petalo_daq.io.config_params import link_control_fields

from petalo_daq.gui.widget_data  import link_status_data
from petalo_daq.gui.types        import link_status_tuple
from petalo_daq.io.config_params import link_status_fields

from petalo_daq.gui.widget_data  import tofpet_config_value_data
from petalo_daq.gui.types        import tofpet_config_value_tuple
from petalo_daq.io.config_params import tofpet_config_value_fields

from petalo_daq.gui.widget_data  import tofpet_config_data
from petalo_daq.gui.types        import tofpet_config_tuple
from petalo_daq.io.config_params import tofpet_config_fields

from petalo_daq.gui.widget_data  import leds_status_data
from petalo_daq.gui.types        import leds_status_tuple
from petalo_daq.io.config_params import leds_status_fields

from petalo_daq.gui.widget_data  import activate_data
from petalo_daq.gui.types        import activate_tuple
from petalo_daq.io.config_params import activate_fields

from petalo_daq.io.utils         import insert_bitarray_slice
from petalo_daq.io.config_params import range_inclusive

from petalo_daq.daq.client_commands import build_hw_register_write_command
from petalo_daq.daq.client_commands import build_sw_register_write_command
from petalo_daq.daq.client_commands import build_sw_register_read_command
from petalo_daq.daq.client_commands import build_hw_register_read_command
from petalo_daq.daq.commands        import register_tuple
from petalo_daq.daq.commands        import sleep_cmd
from petalo_daq.daq.process_responses import temperature_tofpet_to_ch
from petalo_daq.windows.utils       import tofpet_status
from petalo_daq.daq.process_responses import convert_int32_to_bitarray


# dispatch
from petalo_daq.io.utils              import read_bitarray_into_namedtuple
from petalo_daq.io.command_dispatcher import add_function_to_dispatcher
from petalo_daq.io.command_dispatcher import check_command_dispatcher
from petalo_daq.io.command_dispatcher import read_hw_response_from_log
from petalo_daq.gui.types import dispatchable_fn
from petalo_daq.gui.types import dispatch_type
from petalo_daq.gui.types import CommandDispatcherException
from datetime import datetime

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
    window.pushButton_Activate_TOFPET     .clicked.connect(activate_tofpets(window))


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

        write_to_lmk_ram(window,
                         lmk_control.LMK_WREN,
                         lmk_control.LMK_REG_ADD,
                         lmk_control.LMK_REG_VALUE)

        window.update_log_info("LMK control sent",
                               "LMK control command sent")

    return on_click


def write_to_lmk_ram(window, wr_enable, address, value):
    lmk_bitarray = bitarray('0'*32)

    # Convert address and value to bitarray
    address_binary   = '{:07b}'.format(address)
    address_bitarray = bitarray(address_binary.encode())

    value_binary   = '{:08b}'.format(value)
    value_bitarray = bitarray(value_binary.encode())

    lmk_control = lmk_control_tuple(LMK_WREN      = wr_enable,
                                    LMK_REG_ADD   = address_bitarray,
                                    LMK_REG_VALUE = value_bitarray )


    for field, positions in lmk_control_fields.items():
        value = getattr(lmk_control, field)
        insert_bitarray_slice(lmk_bitarray, positions, value)

    #fill bit 31
    insert_bitarray_slice(lmk_bitarray, [31], bitarray('1'))

    #Build command
    daq_id = 0x0000
    register = register_tuple(group=2, id=1)
    value = int(lmk_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2

    command = build_hw_register_write_command(daq_id, register.group, register.id, value)
    print(command)
    window.tx_queue.put(command)


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
        #Build command
        daq_id = 0x0000
        register = register_tuple(group=1, id=0)
        value = 0xFFFFFFFF

        command = build_sw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        window.tx_queue.put(command)

        daq_id = 0
        command = build_sw_register_read_command(daq_id, register_group=1, register_id=0)
        window.tx_queue.put(command)

        window.update_log_info("LEDs status sent",
                               "LEDs status command sent")

    return on_click


def activate_tofpets(window):
    """
    Function to activate selected TOFPETs. It manages power supplies, LMK
    and alignment.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        # Read tofpets to be activated
        activate_config = read_parameters(window, activate_data, activate_tuple)

        # reset power regulators
        fn = dispatchable_fn(type = dispatch_type.function,
                             condition_fn = None,
                             fn = reset_power_supplies(window))
        add_function_to_dispatcher(window, fn)

        # send config
        fn = dispatchable_fn(type = dispatch_type.function,
                             condition_fn = None,
                             fn = activate_power_supplies(window, activate_config))

        add_function_to_dispatcher(window, fn)

        # monitor status until conf done
        fn = dispatchable_fn(type = dispatch_type.loop,
                             condition_fn = check_power_supplies_conf_done(window, activate_config),
                             fn = power_status(window))
        add_function_to_dispatcher(window, fn)
        check_command_dispatcher(window)

        # send config
        fn = dispatchable_fn(type = dispatch_type.function,
                             condition_fn = None,
                             fn = activate_lmk(window, activate_config))

        add_function_to_dispatcher(window, fn)

        # start lmk conf
        fn = dispatchable_fn(type = dispatch_type.function,
                             condition_fn = None,
                             fn = start_lmk_config(window))

        add_function_to_dispatcher(window, fn)

        # monitor status until conf done
        fn = dispatchable_fn(type = dispatch_type.loop,
                             condition_fn = check_lmk_conf_done(window),
                             fn = clock_status(window))
        add_function_to_dispatcher(window, fn)
        check_command_dispatcher(window)

        # align links
        fn = dispatchable_fn(type = dispatch_type.function,
                             condition_fn = None,
                             fn = align_topet_links(window, activate_config))

        add_function_to_dispatcher(window, fn)

        # monitor status until alignment done
        fn = dispatchable_fn(type = dispatch_type.loop,
                             condition_fn = check_alignment_done(window, activate_config),
                             fn = link_status(window))
        add_function_to_dispatcher(window, fn)
        check_command_dispatcher(window)


    return on_click


def reset_power_supplies(window):
    def to_dispatch():
        daq_id = 0x0000
        register = register_tuple(group=1, id=0)
        value = 0x200000FF # reset

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        window.tx_queue.put(command)
    return to_dispatch


def activate_power_supplies(window, activate_config):
    def to_dispatch():
        # Setup power supplies
        print(activate_config)
        power_bitarray = convert_int32_to_bitarray(0x40030000)

        for i in range(8):
            value = getattr(activate_config, f'Activate_TOFPET_{i}')
            print(i, value)
            # VCC25EN activates on 0 and VCCEN activates on 1
            insert_bitarray_slice(power_bitarray, [i, i+8], [not value, value])

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=1, id=0)
        value = int(power_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        window.tx_queue.put(command)

    return to_dispatch


def check_power_supplies_conf_done(window, active_tofpets):
    now = datetime.now()

    def to_dispatch():
        result = False
        register = register_tuple(group=1, id=1)
        cmd_response_log = read_hw_response_from_log(window, register)
        print("value read: ", cmd_response_log)
        if cmd_response_log:
            value = cmd_response_log.cmd['params'][1]
            value_bitarray = convert_int32_to_bitarray(value)
            print(value)
            power_status = read_bitarray_into_namedtuple(value_bitarray, power_status_fields, power_status_tuple)
            print(power_status)

            if now < cmd_response_log.timestamp:
                # Check configuration is already done
                result = power_status.PWR_STATUS_CONF_DONE == bitarray('1')

                # check everything is enabled
                status_check = (power_status.PWR_STATUS_18DIS  == bitarray('0')) & \
                               (power_status.PWR_STATUS_25EN_1 == bitarray('1')) & \
                               (power_status.PWR_STATUS_25EN_2 == bitarray('1'))
                print("status_check: ", status_check)

                # check tofpets one by one
                tofpet_checks = True
                for i in range(8):
                    active_tofpet = getattr(active_tofpets, f'Activate_TOFPET_{i}')
                    print(i, active_tofpet)
                    # VCC25EN activates on 0 and VCCEN activates on 1
                    vccen   = getattr(power_status, f'PWR_STATUS_TOFPET_VCCEN_{i}')
                    vcc25en = getattr(power_status, f'PWR_STATUS_TOFPET_VCC25EN_{i}')
                    tofpet_checks &= (    vccen  .all() == active_tofpet)
                    tofpet_checks &= (not vcc25en.all() == active_tofpet)
                    print(tofpet_checks)
                print("tofpet_checks: ", tofpet_checks)

                if result:
                    if not status_check:
                        raise CommandDispatcherException('Error in 18DIS or 25EN status')
                    if not tofpet_checks:
                        raise CommandDispatcherException('Error in TOFPET power supplies status')

        return result

    return to_dispatch


def activate_lmk(window, active_tofpets):
    def to_dispatch():
        print("activate lmks")
        print(active_tofpets)

        if (active_tofpets.Activate_TOFPET_0 == True ) and (active_tofpets.Activate_TOFPET_1 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 7, value = 0x11)
            write_to_lmk_ram(window, bitarray('1'), address = 6, value = 0xF0)
        if (active_tofpets.Activate_TOFPET_0 == True ) and (active_tofpets.Activate_TOFPET_1 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 7, value = 0x01)
        if (active_tofpets.Activate_TOFPET_0 == False) and (active_tofpets.Activate_TOFPET_1 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 7, value = 0x10)
        if (active_tofpets.Activate_TOFPET_0 == False) and (active_tofpets.Activate_TOFPET_1 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 7, value = 0x00)
            write_to_lmk_ram(window, bitarray('1'), address = 6, value = 0xF9)

        if (active_tofpets.Activate_TOFPET_2 == True ) and (active_tofpets.Activate_TOFPET_3 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 55, value = 0x11)
            write_to_lmk_ram(window, bitarray('1'), address = 54, value = 0xF0)
        if (active_tofpets.Activate_TOFPET_2 == True ) and (active_tofpets.Activate_TOFPET_3 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 55, value = 0x01)
        if (active_tofpets.Activate_TOFPET_2 == False) and (active_tofpets.Activate_TOFPET_3 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 55, value = 0x10)
        if (active_tofpets.Activate_TOFPET_2 == False) and (active_tofpets.Activate_TOFPET_3 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 55, value = 0x00)
            write_to_lmk_ram(window, bitarray('1'), address = 54, value = 0xF9)

        if (active_tofpets.Activate_TOFPET_4 == True ) and (active_tofpets.Activate_TOFPET_5 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 31, value = 0x11)
            write_to_lmk_ram(window, bitarray('1'), address = 30, value = 0xF0)
        if (active_tofpets.Activate_TOFPET_4 == True ) and (active_tofpets.Activate_TOFPET_5 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 31, value = 0x10)
        if (active_tofpets.Activate_TOFPET_4 == False) and (active_tofpets.Activate_TOFPET_5 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 31, value = 0x01)
        if (active_tofpets.Activate_TOFPET_4 == False) and (active_tofpets.Activate_TOFPET_5 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 31, value = 0x00)
            write_to_lmk_ram(window, bitarray('1'), address = 30, value = 0xF9)

        if (active_tofpets.Activate_TOFPET_6 == True ) and (active_tofpets.Activate_TOFPET_7 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 23, value = 0x11)
            write_to_lmk_ram(window, bitarray('1'), address = 22, value = 0xF0)
        if (active_tofpets.Activate_TOFPET_6 == True ) and (active_tofpets.Activate_TOFPET_7 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 23, value = 0x01)
        if (active_tofpets.Activate_TOFPET_6 == False) and (active_tofpets.Activate_TOFPET_7 == True):
            write_to_lmk_ram(window, bitarray('1'), address = 23, value = 0x10)
        if (active_tofpets.Activate_TOFPET_6 == False) and (active_tofpets.Activate_TOFPET_7 == False):
            write_to_lmk_ram(window, bitarray('1'), address = 23, value = 0x00)
            write_to_lmk_ram(window, bitarray('1'), address = 22, value = 0xF9)

    return to_dispatch


def start_lmk_config(window):
    def to_dispatch():
        daq_id = 0x0000
        register = register_tuple(group=2, id=0)
        value = 0x40000000 # start

        command = build_hw_register_write_command(daq_id, register.group, register.id, value)
        print(command)
        window.tx_queue.put(command)
    return to_dispatch


def check_lmk_conf_done(window):
    now = datetime.now()

    def to_dispatch():
        result = False
        register = register_tuple(group=2, id=2)
        cmd_response_log = read_hw_response_from_log(window, register)
        print("value read: ", cmd_response_log)
        if cmd_response_log:
            value = cmd_response_log.cmd['params'][1]
            value_bitarray = convert_int32_to_bitarray(value)
            print(value)
            clock_status = read_bitarray_into_namedtuple(value_bitarray, clock_status_fields, clock_status_tuple)
            print(clock_status)

            if now < cmd_response_log.timestamp:
                result = (clock_status.CLK_CONF_DONE == bitarray('1')) & \
                         (clock_status.CLK_CONF_ON   == bitarray('0'))
        return result

    return to_dispatch


def align_topet_links(window, activate_config):
    def to_dispatch():
        print(activate_config)

        for i in range(8):
            active_tofpet = getattr(activate_config, f'Activate_TOFPET_{i}')
            print(i, active_tofpet)
            if active_tofpet:
                reset_link_alignment(window, i)
                align_link(window, i)

    return to_dispatch


def reset_link_alignment(window, tofpet_id):
    cmd_bitarray = convert_int32_to_bitarray(0x40000000)

    tofpet_binary   = '{:03b}'.format(tofpet_id)
    tofpet_bitarray = bitarray(tofpet_binary.encode())

    insert_bitarray_slice(cmd_bitarray,
                          reverse_range_inclusive(2, 0),
                          tofpet_bitarray)

    #Build command
    daq_id = 0x0000
    register = register_tuple(group=3, id=0)
    value = int(cmd_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2

    command = build_hw_register_write_command(daq_id, register.group, register.id, value)
    print(command)
    window.tx_queue.put(command)


def align_link(window, tofpet_id):
    cmd_bitarray = convert_int32_to_bitarray(0x80000000)

    tofpet_binary   = '{:03b}'.format(tofpet_id)
    tofpet_bitarray = bitarray(tofpet_binary.encode())

    insert_bitarray_slice(cmd_bitarray,
                          reverse_range_inclusive(2, 0),
                          tofpet_bitarray)

    #Build command
    daq_id = 0x0000
    register = register_tuple(group=3, id=0)
    value = int(cmd_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2

    command = build_hw_register_write_command(daq_id, register.group, register.id, value)
    print(command)
    window.tx_queue.put(command)


def check_alignment_done(window, active_tofpets):
    now = datetime.now()

    def to_dispatch():
        result = False
        register = register_tuple(group=3, id=1)
        cmd_response_log = read_hw_response_from_log(window, register)
        print("value read: ", cmd_response_log)
        if cmd_response_log:
            value = cmd_response_log.cmd['params'][1]
            value_bitarray = convert_int32_to_bitarray(value)
            print(value)
            link_status = read_bitarray_into_namedtuple(value_bitarray, link_status_fields, link_status_tuple)
            print(link_status)

            if now < cmd_response_log.timestamp:
                # check tofpets one by one
                tofpet_checks = True
                for i in range(8):
                    active_tofpet = getattr(active_tofpets, f'Activate_TOFPET_{i}')
                    print(i, active_tofpet)
                    aligned  = getattr(link_status, f'LINK_STATUS_ALIGNED_{i}')
                    aligning = getattr(link_status, f'LINK_STATUS_ALIGNING_{i}')
                    tofpet_checks &= (aligned .all() == active_tofpet)
                    tofpet_checks &= (aligning.all() == False)
                    print(tofpet_checks)
                print("tofpet_checks: ", tofpet_checks)

                result = tofpet_checks

        return result

    return to_dispatch
