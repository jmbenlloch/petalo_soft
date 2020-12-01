from collections import namedtuple
from petalo_daq.io import config_params


# Name tuples to store all the parameters related to some particular config
# They are constructed using all the keys stated in config_params.py

global_config_tuple      = namedtuple('global_config'     , config_params.global_config_fields)
channel_config_tuple     = namedtuple('channel_config'    , config_params.channel_config_fields)
temperature_config_tuple = namedtuple('temperature_config', config_params.temperature_config_fields)
power_control_tuple      = namedtuple('power_control'     , config_params.power_control_fields)
run_control_tuple        = namedtuple('run_control'       , config_params.run_control_fields)
clock_control_tuple      = namedtuple('clock_control'     , config_params.clock_control_fields)
lmk_control_tuple        = namedtuple('lmk_control'       , config_params.lmk_control_fields)
tofpet_config_tuple      = namedtuple('tofpet_config'     , config_params.tofpet_config_fields)
link_control_tuple       = namedtuple('link_control'      , config_params.link_control_fields)
tofpet_config_value_tuple = namedtuple('tofpet_config_value', config_params.tofpet_config_value_fields)
leds_status_tuple        = namedtuple('leds_status'       , config_params.leds_status_fields)
activate_tuple           = namedtuple('activate'          , config_params.activate_fields)


class LogError(Exception):
    pass
