from bitarray  import bitarray
from datetime  import datetime

from .. gui.utils        import read_parameters
from .. gui.widget_data  import global_data
from .. gui.types        import global_config_tuple
from .. io.config_params import global_config_fields
from .. io.utils         import insert_bitarray_slice
from .. io.utils         import update_gui_fields
from .. io.config_params import link_control_fields
from .. io.configuration import save_global_config_to_yml

from .. network.client_commands import build_hw_register_write_command
from .. network.commands        import register_tuple

from .. gui.types        import tofpet_config_tuple
from .. network.commands        import sleep_cmd

from . utils     import build_tofpet_configuration_register_value
from . utils     import build_tofpet_ram_address_command
from . utils     import tofpet_status
from . utils     import set_run_mode

def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_reg_glob.clicked.connect(Config_update_glob(window))
    window.checkBox_counter_en.clicked.connect(set_run_mode(window))
    window.spinBox_ASIC_n.valueChanged.connect(update_global_config(window))
    #  window.checkBox_all_ASIC.clicked.connect()


def update_global_config(window):
    def on_click():
        asic = window.spinBox_ASIC_n.value()
        global_configs = window.data_store.retrieve('global_config_mongo')
        config = global_configs[asic]
        for field, value in config._asdict().items():
            update_gui_fields(window, field, value, global_data)

    return on_click


#  def update_global_config(window):
#      def on_click():
#          global_config = window.data_store.retrieve('global_config')
#          for field, value in global_config._asdict().items():
#              update_gui_fields(window, field, value, global_data)
#
#      return on_click


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

        # update data store
        global_configs = window.data_store.retrieve('global_config_mongo')
        asic = window.spinBox_ASIC_n.value()
        global_configs[asic] = global_config

        window.data_store.insert('global_config_mongo', global_configs)

        for field, positions in global_config_fields.items():
            value = getattr(global_config, field)

            # convert int values to bitarrays
            if not isinstance(value, bitarray):
                nbits        = len(positions)
                fmt_string   = '{{:0{}b}}'.format(nbits)
                value_binary = fmt_string.format(value)
                value        = bitarray(value_binary.encode())

            insert_bitarray_slice(global_bitarray, positions, value)

        #fill unused bits
        global_bitarray[ 16: 18] = bitarray('00')
        global_bitarray[ 31: 32] = bitarray('0')
        global_bitarray[177:178] = bitarray('1')

        # print("global config: ", global_bitarray[::-1])

        with open('global_config_log.txt', 'a') as fd:
            date = datetime.now()
            fd.write(f"{date}: {global_bitarray}\n")

        window.data_store.insert('global_config', global_bitarray)
        save_global_config_to_yml(window)
        send_global_configuration_to_card(window, global_bitarray)

        window.update_log_info("Global register configured",
                               "Global ASIC registers conf")

    return on_click


def send_global_configuration_to_card(window, global_bitarray):
    #  print(global_bitarray)
    global_bitarray_split = [global_bitarray[152:184],
                             global_bitarray[120:152],
                             global_bitarray[ 88:120],
                             global_bitarray[ 56:88],
                             global_bitarray[ 24:56],
                             bitarray('0'*8) + global_bitarray[0:24]]

    for addr, value in enumerate(global_bitarray_split):
        #  print(addr, value)
        value_int = int(value.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        #  print(value_int)

        address_binary   = '{:09b}'.format(addr)
        address_bitarray = bitarray(address_binary.encode())

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=3)
        command = build_hw_register_write_command(daq_id, register.group, register.id, value_int)

        #  print(command)
        # Send command
        window.tx_queue.put(command)
        #  window.update_log_info("", "Global config word {} sent".format(addr))

        command  = build_tofpet_ram_address_command(daq_id, address_bitarray)
        #  print(command)
        # Send command
        window.tx_queue.put(command)
        #  window.update_log_info("", "Global config register {} sent".format(addr))

    # Select TOPFET id
    tofpet_id = window.spinBox_ASIC_n.value()

    # set rst cycles
    reset_cycles = 10
    tofpet_id = tofpet_id | (reset_cycles << 4)

    # set ddr mode
    ddr_mode = 1 if window.checkBox_DDR.isChecked() else 0
    tofpet_id = tofpet_id | (ddr_mode << link_control_fields['DDR'][-1])

    #  print("tofpet_id: ", tofpet_id)
    register  = register_tuple(group=3, id=0)
    command = build_hw_register_write_command(daq_id, register.group, register.id, tofpet_id)
    #  print(command)
    # Send command
    window.tx_queue.put(command)

    # Start configuration
    command  = build_start_global_configuration_command(daq_id)
    #  print(command)
    window.tx_queue.put(command)
    window.update_log_info("", "Global config start sent")

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


