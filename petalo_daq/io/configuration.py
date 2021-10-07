import json
import os
import yaml

from bitarray import bitarray

from .  config_params    import channel_config_fields
from .  config_params    import global_config_fields
from .  utils            import load_gui_config
from .  utils            import load_bitarray_config
from .. gui.widget_data  import channel_data
from .. gui.widget_data  import global_data
from .. gui.types        import channel_config_tuple
from .. gui.types        import global_config_tuple
from .. gui.utils        import read_parameters


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
    #print(window.data_store.data)


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
    # add to data_store the tuple format
    global_config = read_parameters(window, global_data, global_config_tuple)
    window.data_store.insert('global_config_mongo', global_config)


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
    #print(channel_config)
    load_bitarray_config(window, channel_config[default_channel]['value'], channel_config_fields, channel_data)


ch_config_yml     = '{}/channels_config.yml'.format(os.environ['PETALO_DAQ_DIR'])
global_config_yml = '{}/global_config.yml'  .format(os.environ['PETALO_DAQ_DIR'])

class NoAliasDumper(yaml.SafeDumper):
   def ignore_aliases(self, data):
       return True

def bitarray_representer(dumper, data):
    return dumper.represent_scalar(u'!bitarray', data.to01())
yaml.add_representer(bitarray, bitarray_representer, NoAliasDumper)

def bitarray_parser(loader,node):
    value = loader.construct_scalar(node)
    return bitarray(value)


def save_config_to_yml(window):
    configs = window.data_store.retrieve('channel_config')

    configs_dicts = {asic : {k : v._asdict() for k,v in config.items()} \
                      for asic, config in configs.items()}

    with open(ch_config_yml, 'w') as outfile:
        yaml.dump(configs_dicts, outfile, default_flow_style=False, Dumper=NoAliasDumper)


def save_global_config_to_yml(window):
    configs = window.data_store.retrieve('global_config_mongo')

    configs_dicts = {k : v._asdict() for k,v in configs.items()}

    with open(global_config_yml, 'w') as outfile:
        yaml.dump(configs_dicts, outfile, default_flow_style=False, Dumper=NoAliasDumper)


def load_channel_config_from_yml(window):
    yaml.add_constructor(u'!bitarray', bitarray_parser)

    with open(ch_config_yml, 'r') as outfile:
        channel_configs_tmp = yaml.load(outfile)

    channel_configs = { asic : {k : channel_config_tuple(**v) for k, v in config.items()} \
                        for asic, config in channel_configs_tmp.items()}
    window.data_store.insert('channel_config', channel_configs)


def load_global_config_from_yml(window):
    """
    Function to load the parameters of the "Global config" tab.
    TODO: Save one config per TOFPET

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    yaml.add_constructor(u'!bitarray', bitarray_parser)

    with open(global_config_yml, 'r') as outfile:
        global_configs_tmp = yaml.load(outfile)

    global_configs = {k : global_config_tuple(**v) for k, v in global_configs_tmp.items()}
    window.data_store.insert('global_config_mongo', global_configs)

