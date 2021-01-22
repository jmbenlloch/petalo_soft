from bitarray  import bitarray

from . utils import write_to_lmk_ram

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.io.config_params import reverse_range_inclusive

from . register_config           import power_status
from . register_config           import clock_status
from . register_config           import link_status

from petalo_daq.io.config_params import link_status_fields
from petalo_daq.gui.types        import link_status_tuple

from petalo_daq.gui.widget_data  import activate_data
from petalo_daq.gui.types        import activate_tuple

from petalo_daq.gui.types        import power_status_tuple
from petalo_daq.io.config_params import power_status_fields

from petalo_daq.gui.types        import clock_status_tuple
from petalo_daq.io.config_params import clock_status_fields

from petalo_daq.io.utils         import insert_bitarray_slice

from petalo_daq.network.client_commands import build_hw_register_write_command
from petalo_daq.network.client_commands import build_sw_register_write_command
from petalo_daq.network.client_commands import build_sw_register_read_command
from petalo_daq.network.commands        import register_tuple
from petalo_daq.network.commands        import sleep_cmd
from petalo_daq.network.process_responses import temperature_tofpet_to_ch
from petalo_daq.network.process_responses import convert_int32_to_bitarray


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

    window.pushButton_Temp_read      .clicked.connect(read_temperature(window))
    window.pushButton_LEDs_read      .clicked.connect(read_leds       (window))
    window.pushButton_Activate_TOFPET.clicked.connect(activate_tofpets(window))

    window.SpinBox_Buffer    .editingFinished.connect(store_general_data(window))
    window.SpinBox_Pretrigger.editingFinished.connect(store_general_data(window))
    window.SpinBox_Triggers  .editingFinished.connect(store_general_data(window))


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


def store_general_data(window):
    """
    Function read the values from general configuration tab and store them

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        data = {
            'SpinBox_Buffer' : {
                'value' : window.SpinBox_Buffer.value()
            },
            'SpinBox_Pretrigger' : {
                'value' : window.SpinBox_Pretrigger.value()
            },
            'SpinBox_Triggers' : {
                'value' : window.SpinBox_Triggers.value()
            },
        }

        window.data_store.insert('general_config', data)

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

        window.checkBox_Activate_done.setChecked(False)

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
                             fn = power_status(window, verbose=False))
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
                             fn = clock_status(window, verbose=False))
        add_function_to_dispatcher(window, fn)
        check_command_dispatcher(window)

        # align links
        for i in range(8):
            active_tofpet = getattr(activate_config, f'Activate_TOFPET_{i}')
            print(i, active_tofpet)
            if active_tofpet:
                fn = dispatchable_fn(type = dispatch_type.function,
                                     condition_fn = None,
                                     fn = align_topet_links(window, i))

                add_function_to_dispatcher(window, fn)

                # monitor status until alignment done
                fn = dispatchable_fn(type = dispatch_type.loop,
                                     condition_fn = check_alignment_done(window, i),
                                     fn = link_status(window, verbose=False))
                add_function_to_dispatcher(window, fn)
                check_command_dispatcher(window)

        # signal finish upon success
        fn = dispatchable_fn(type = dispatch_type.function,
                             condition_fn = None,
                             fn = activate_finished(window))

        add_function_to_dispatcher(window, fn)

    return on_click


def activate_finished(window):
    def to_dispatch():
        window.checkBox_Activate_done.setChecked(True)
        window.update_log_info("Configuring TOFPETs", "TOFPETs activated!")
    return to_dispatch


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
        window.update_log_info("Configuring TOFPETs",
                               "Configuring power regulators")

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

                # Break look if it takes too long
                tdelta = cmd_response_log.timestamp - now
                if (not result) and (tdelta.total_seconds() > 10):
                    raise CommandDispatcherException('Error in Power regulators configuration')

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
        window.update_log_info("Configuring TOFPETs",
                               "Configuring LMK")
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

            # Break look if it takes too long
            tdelta = cmd_response_log.timestamp - now
            if (not result) and (tdelta.total_seconds() > 10):
                raise CommandDispatcherException('Error in LMK configuration')

        return result

    return to_dispatch


def align_topet_links(window, tofpet_id):
    def to_dispatch():
        reset_link_alignment(window, tofpet_id)
        align_link(window, tofpet_id)

        window.update_log_info("Configuring TOFPETs",
                               f"Aligning links {tofpet_id}")

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


def check_alignment_done(window, tofpet_id):
    now = datetime.now()

    def to_dispatch():
        result = False
        register = register_tuple(group=3, id=1)
        window.tx_queue.put(sleep_cmd(2000))
        cmd_response_log = read_hw_response_from_log(window, register)
        print("value read: ", cmd_response_log)
        if cmd_response_log:
            value = cmd_response_log.cmd['params'][1]
            value_bitarray = convert_int32_to_bitarray(value)
            print(value)
            link_status = read_bitarray_into_namedtuple(value_bitarray, link_status_fields, link_status_tuple)
            print(link_status)

            if now < cmd_response_log.timestamp:
                print("link_status: ", link_status)
                aligned  = getattr(link_status, f'LINK_STATUS_ALIGNED_{tofpet_id}')
                aligning = getattr(link_status, f'LINK_STATUS_ALIGNING_{tofpet_id}')

                print("\n\n\n aligned: ", aligned)
                print("\n aligning: ", aligning, "\n\n\n\n\n")

                result = aligned.all() and (not aligning.all())

                # Break look if it takes too long
                tdelta = cmd_response_log.timestamp - now
                if (not result) and (tdelta.total_seconds() > 30):
                    raise CommandDispatcherException('Error in TOFPET alignment')

        return result

    return to_dispatch
