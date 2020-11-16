from collections import namedtuple
from petalo_daq.io import config_params


# Name tuples to store all the parameters related to some particular config
# They are constructed using all the keys stated in config_params.py

global_config_tuple  = namedtuple('global_config' , config_params.global_config_fields)
channel_config_tuple = namedtuple('channel_config', config_params.channel_config_fields)
temperature_config_tuple = namedtuple('temperature_config', config_params.temperature_config_fields)


class LogError(Exception):
    pass
