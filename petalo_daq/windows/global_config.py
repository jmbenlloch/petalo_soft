from bitarray  import bitarray

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.gui.widget_data  import global_data
from petalo_daq.gui.types        import global_config_tuple
from petalo_daq.io.config_params import global_config_fields
from petalo_daq.io.utils         import insert_bitarray_slice

from petalo_daq.daq.client_commands import build_hw_register_write_command
from petalo_daq.daq.client_commands import build_hw_register_read_command
from petalo_daq.daq.commands        import register_tuple

from petalo_daq.gui.types        import tofpet_config_tuple
from petalo_daq.io.config_params import tofpet_config_fields
from petalo_daq.daq.commands        import sleep_cmd

from petalo_daq.windows.utils     import build_tofpet_configuration_register_value
from petalo_daq.windows.utils     import build_tofpet_ram_address_command
from petalo_daq.windows.utils     import tofpet_status

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
        global_bitarray = bitarray(184)

        # ASIC parameters to be update
        global_config = read_parameters(window, global_data, global_config_tuple)

        for field, positions in global_config_fields.items():
            print(field)
            value = getattr(global_config, field)
            insert_bitarray_slice(global_bitarray, positions, value)

        #fill unused bits
        global_bitarray[ 16: 18] = bitarray('00')
        global_bitarray[ 31: 32] = bitarray('0')
        global_bitarray[177:178] = bitarray('0')

        window.data_store.insert('global_config', global_bitarray)
        send_global_configuration_to_card(window, global_bitarray)

        window.update_log_info("Global register configured",
                               "Global ASIC registers conf")

    return on_click


def send_global_configuration_to_card(window, global_bitarray):
    print(global_bitarray)
    global_bitarray_split = [global_bitarray[152:184],
                             global_bitarray[120:152],
                             global_bitarray[ 88:120],
                             global_bitarray[ 56:88],
                             global_bitarray[ 24:56],
                             bitarray('0'*8) + global_bitarray[0:24]]

    for addr, value in enumerate(global_bitarray_split):
        print(addr, value)
        value_int = int(value.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value_int)

        address_binary   = '{:09b}'.format(addr)
        address_bitarray = bitarray(address_binary.encode())

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=3)
        command = build_hw_register_write_command(daq_id, register.group, register.id, value_int)

        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("", "Global config word {} sent".format(addr))

        command  = build_tofpet_ram_address_command(daq_id, address_bitarray)
        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("", "Global config register {} sent".format(addr))

    # TODO Select TOPFET id
    tofpet_id = 0
    tofpet_id = window.spinBox_ASIC_n.value()
    print("tofpet_id: ", tofpet_id)
    register  = register_tuple(group=3, id=0)
    command = build_hw_register_write_command(daq_id, register.group, register.id, tofpet_id)
    print(command)
    # Send command
    window.tx_queue.put(command)

    # Start configuration
    command  = build_start_global_configuration_command(daq_id)
    print(command)
    window.tx_queue.put(command)
    window.update_log_info("", "Global config start sent".format(addr))

    # Check TOFPET configuration status register
    window.tx_queue.put(sleep_cmd(1000))
    tofpet_status(window)()



def build_start_global_configuration_command(daq_id):
    '''
    Builds a Start configuration command for Global ASIC configuration.

    Returns:
    bitarray: Command to be sent
    '''
    tofpet_config = tofpet_config_tuple(TOFPET_CONF_START     = bitarray('1'),
                                        TOFPET_CONF_VERIFY    = bitarray('1'),
                                        TOFPET_CONF_ERROR_RST = bitarray('0'),
                                        TOFPET_CONF_WR        = bitarray('0'),
                                        TOFPET_CONF_ADDR      = bitarray('000000000'),
                                        TOFPET_CONF_MODE      = bitarray('01') ,
                                        TOFPET_CONF_CH_SEL    = bitarray('000000'))

    value    = build_tofpet_configuration_register_value(tofpet_config)
    register = register_tuple(group=3, id=2)
    command  = build_hw_register_write_command(daq_id, register.group, register.id, value)
    return command


