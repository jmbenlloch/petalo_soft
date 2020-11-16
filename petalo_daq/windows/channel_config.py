from bitarray import bitarray

from petalo_daq.gui.utils        import read_parameters
from petalo_daq.gui.widget_data  import channel_data
from petalo_daq.gui.types        import channel_config_tuple
from petalo_daq.io.config_params import channel_config_fields
from petalo_daq.io.utils         import insert_bitarray_slice


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_reg_ch.clicked.connect(Config_update_ch(window))
    window.checkBox_all_ch  .clicked.connect(set_channels    (window))


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
            print(field)
            value = getattr(channel_config, field)
            insert_bitarray_slice(channel_bitarray, positions, value)

        #fill unused bits
        channel_bitarray[110:111] = bitarray('1') # "n/u

        # all channels
        all_channels = window.data_store.retrieve('all_channels')

        if all_channels:
            n_channels = 8 # TODO put somewhere the number of channels
            channel_configs = {}
            for ch in range(n_channels):
                channel_configs[ch] = channel_bitarray

            window.data_store.insert('channel_config', channel_configs)
        else:
            channel_configs = window.data_store.retrieve('channel_config')
            channel = window.spinBox_ch_number.value()
            channel_configs[channel] = channel_bitarray
            window.data_store.insert('channel_config', channel_configs)

        print(channel_bitarray[0:125])

        window.update_log_info("Channel registers configured",
                               "Channel ASIC registers configured")

    return on_click
