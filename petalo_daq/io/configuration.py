import json

from bitarray import bitarray

from petalo_daq.io.config_params import channel_config_fields
from petalo_daq.io.config_params import global_config_fields
from petalo_daq.io.utils         import load_gui_config
from petalo_daq.io.utils         import load_bitarray_config
from petalo_daq.gui.widget_data  import channel_data
from petalo_daq.gui.widget_data  import global_data


def load_configuration_file(window, fname):
    """
    Function to load a configuration file and store the config in data_store.
    There is one line per window/tab in the application.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    fname (string): File path
    """
    with open(fname) as fd:
        data = json.loads(fd.read())
        load_general_parameters       (window, data)
        load_global_config_parameters (window, data)
        load_channel_config_parameters(window, data)
    print(window.data_store.data)


def load_general_parameters(window, data):
    """
    Function to load the parameters of the "General" tab.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    data (dictionary): Values read from the json file for this tab.
    """
    general_config = data['general_config']
    window.data_store.insert('general_config', general_config)
    load_gui_config(window, general_config)


def load_global_config_parameters(window, data):
    """
    Function to load the parameters of the "Global ASIC config" tab.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    data (dictionary): Values read from the json file for this tab.
    """
    global_config  = eval(data['global_config'] ['value'])
    window.data_store.insert('global_config' , global_config)
    load_bitarray_config(window, global_config, global_config_fields, global_data)


def load_channel_config_parameters(window, data):
    """
    Function to load the parameters of the "Channel config" tab.
    There is a loop to interpret each bitarray for each channel.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    data (dictionary): Values read from the json file for this tab.
    """
    all_channels   = data['all_channels']
    channel_config = data['channel_config']
    for channel, config in channel_config.items():
        channel_config[channel]['value'] = eval(config['value'])

    window.data_store.insert('channel_config', channel_config)
    window.data_store.insert('all_channels'  , all_channels)

    default_channel = "0"
    print(channel_config)
    load_bitarray_config(window, channel_config[default_channel]['value'], channel_config_fields, channel_data)

