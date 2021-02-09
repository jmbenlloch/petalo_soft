from bitarray import bitarray

from .. gui.utils        import read_parameters
from .. gui.widget_data  import channel_data
from .. gui.types        import channel_config_tuple
from .. io.config_params import channel_config_fields
from .. io.utils         import insert_bitarray_slice

from .. network.client_commands import build_hw_register_write_command
from .. network.commands        import register_tuple

from .. gui.types        import tofpet_config_tuple
from .. network.commands import sleep_cmd

from .  utils     import build_tofpet_configuration_register_value
from .  utils     import build_tofpet_ram_address_command
from .  utils     import tofpet_status
from .  utils     import set_run_mode


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_reg_ch.clicked.connect(Config_update_ch(window))
    window.checkBox_all_ch  .clicked.connect(set_channels    (window))

    # Run mode
    #window.comboBox_qdc_mode      .currentIndexChanged.connect(set_run_mode(window))
    #  window.comboBox_intg_en       .currentIndexChanged.connect(set_run_mode(window))
    #  window.comboBox_intg_signal_en.currentIndexChanged.connect(set_run_mode(window))


def set_channels(window):
    """
    Function to set the same configuration for all channels

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        if (window.checkBox_all_ch.isChecked() == True):
            window.data_store.insert( 'all_channels', True)
            window.spinBox_ch_number.setEnabled (False)
        else:
            window.data_store.insert( 'all_channels', False)
            window.spinBox_ch_number.setEnabled (True)

    return on_click


def Config_update_ch(window):
    """
    Function to update the channel configuration.
    It reads the values from the GUI fields and updates the bitarray in
    data_store. If "all_channels" is activated, then all channels are updated,
    if not, only the channel selected is updated.

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        channel_bitarray = bitarray(125)

        # ASIC channel parameters to be update
        channel_config = read_parameters(window, channel_data, channel_config_tuple)
        for field, positions in channel_config_fields.items():
            value = getattr(channel_config, field)
            #  print(field, value, positions)

            # convert int values to bitarrays
            if not isinstance(value, bitarray):
                nbits        = len(positions)
                fmt_string   = '{{:0{}b}}'.format(nbits)
                value_binary = fmt_string.format(value)
                value        = bitarray(value_binary.encode())

            insert_bitarray_slice(channel_bitarray, positions, value)

        #fill unused bits
        channel_bitarray[110:111] = bitarray('1') # "n/u

        # all channels
        all_channels = window.data_store.retrieve('all_channels')

        if all_channels:
            n_channels = 64 # TODO put somewhere the number of channels
            channel_configs = {}
            for ch in range(n_channels):
                channel_configs[ch] = channel_bitarray
                send_channel_configuration_to_ram(window, ch, channel_bitarray)

            send_start_all_channels_configuration_to_card(window)

            window.data_store.insert('channel_config', channel_configs)
        else:
            channel_configs = window.data_store.retrieve('channel_config')
            channel = window.spinBox_ch_number.value()
            channel_configs[channel] = channel_bitarray

            send_channel_configuration_to_ram(window, channel, channel_bitarray)
            send_start_channel_configuration_to_card(window, channel)

            window.data_store.insert('channel_config', channel_configs)

        print(channel_bitarray[0:125])

        window.update_log_info("Channel registers configured",
                               "Channel ASIC registers configured")

    return on_click


def send_channel_configuration_to_ram(window, channel_id, channel_bitarray):
    print(channel_bitarray)
    channel_bitarray_split = [channel_bitarray[93:125],
                              channel_bitarray[61:93],
                              channel_bitarray[29:61],
                              bitarray('0'*3) + channel_bitarray[0:28]]

    for offset, value in enumerate(channel_bitarray_split):
        print(offset, value)
        address   = channel_id*4 + offset+6
        value_int = int(value.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
        print(value_int)

        address_binary   = '{:09b}'.format(address)
        address_bitarray = bitarray(address_binary.encode())

        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=3)
        command = build_hw_register_write_command(daq_id, register.group, register.id, value_int)

        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("", "Channel config word {} sent".format(address))

        command  = build_tofpet_ram_address_command(daq_id, address_bitarray)
        print(command)
        # Send command
        window.tx_queue.put(command)
        window.update_log_info("", "Channel config register {} sent".format(address))


def send_start_channel_configuration_to_card(window, channel):
    # TODO Select TOPFET id
    tofpet_id = 0
    tofpet_id = window.spinBox_ASIC_n_2.value()
    print("tofpet_id: ", tofpet_id)
    daq_id    = 0
    register  = register_tuple(group=3, id=0)
    command = build_hw_register_write_command(daq_id, register.group, register.id, tofpet_id)
    print(command)
    # Send command
    window.tx_queue.put(command)

    # Start configuration
    command  = build_start_channel_configuration_command(daq_id, channel)
    print(command)
    window.tx_queue.put(command)
    window.update_log_info("", "Channel {} config start sent".format(channel))

    # Check TOFPET configuration status register
    window.tx_queue.put(sleep_cmd(1000))
    tofpet_status(window)()


def send_start_all_channels_configuration_to_card(window):
    # TODO Select TOPFET id
    tofpet_id = 0
    tofpet_id = window.spinBox_ASIC_n_2.value()
    print("tofpet_id: ", tofpet_id)
    daq_id    = 0
    register  = register_tuple(group=3, id=0)
    command = build_hw_register_write_command(daq_id, register.group, register.id, tofpet_id)
    print(command)
    # Send command
    window.tx_queue.put(command)

    # Start configuration
    command  = build_start_all_channels_configuration_command(daq_id)
    print(command)
    window.tx_queue.put(command)
    window.update_log_info("", "Channels config start sent")

    # Check TOFPET configuration status register
    window.tx_queue.put(sleep_cmd(1000))
    tofpet_status(window)()


def build_start_all_channels_configuration_command(daq_id):
    '''
    Builds a Start configuration command for Channel ASIC configuration.

    Returns:
    bitarray: Command to be sent
    '''
    tofpet_config = tofpet_config_tuple(TOFPET_CONF_START = bitarray('1'),
                                        TOFPET_CONF_VERIFY     = bitarray('0'),
                                        TOFPET_CONF_ERROR_RST  = bitarray('0'),
                                        TOFPET_CONF_WR    = bitarray('1'),
                                        TOFPET_CONF_ADDR  = bitarray('000000000'),
                                        TOFPET_CONF_MODE       = bitarray('10') ,
                                        TOFPET_CONF_CH_SEL     = bitarray('000000'))

    value    = build_tofpet_configuration_register_value(tofpet_config)
    register = register_tuple(group=3, id=2)
    command  = build_hw_register_write_command(daq_id, register.group, register.id, value)
    return command


def build_start_channel_configuration_command(daq_id, channel):
    '''
    Builds a Start configuration command for Channel ASIC configuration.

    Returns:
    bitarray: Command to be sent
    '''
    channel_binary   = '{:06b}'.format(channel)
    channel_bitarray = bitarray(channel_binary.encode())

    tofpet_config = tofpet_config_tuple(TOFPET_CONF_START     = bitarray('1'),
                                        TOFPET_CONF_VERIFY    = bitarray('1'),
                                        TOFPET_CONF_ERROR_RST = bitarray('0'),
                                        TOFPET_CONF_WR        = bitarray('0'),
                                        TOFPET_CONF_ADDR      = bitarray('000000000'),
                                        TOFPET_CONF_MODE      = bitarray('11') ,
                                        TOFPET_CONF_CH_SEL    = channel_bitarray)

    value    = build_tofpet_configuration_register_value(tofpet_config)
    register = register_tuple(group=3, id=2)
    command  = build_hw_register_write_command(daq_id, register.group, register.id, value)
    return command


