from petalo_daq.gui.types import LogError
from petalo_daq.io.config_params import power_status_fields
from petalo_daq.gui.widget_data  import power_status_data
from petalo_daq.io.config_params import clock_status_fields
from petalo_daq.gui.widget_data  import clock_status_data
from petalo_daq.io.config_params import link_status_fields
from petalo_daq.gui.widget_data  import link_status_data
from petalo_daq.io.utils         import load_bitarray_config
from petalo_daq.io.utils         import read_bitarray_slice

from petalo_daq.io.config_params import run_status_fields
from petalo_daq.io.config_params import tofpet_status_fields
from petalo_daq.gui.widget_data  import tofpet_status_data

from bitarray import bitarray

temperature_ch_to_tofpet = {0 : 1,
                            1 : 3,
                            2 : 5,
                            3 : 7,
                            4 : 0,
                            5 : 2,
                            6 : 4,
                            7 : 6,
                            8 : 8}

temperature_tofpet_to_ch = {v: k for k, v in temperature_ch_to_tofpet.items()}

def read_temperature(window, cmd, params):
    register, value = params

    tofpet_id = temperature_ch_to_tofpet[register.id]
    widget_name = 'lcdNumber_Temp_{}'.format(tofpet_id)
    widget = getattr(window, widget_name)

    # Bits 30 and 31 must be zero
    if (value & 0xC0000000) >> 30 != 0:
        widget.display('Err')
        raise LogError(f"Temperature error. Register {register} has not 00 in bits 30, 31")
    if (value & 0x30000000) >> 28 == 3:
        widget.display('Err')
        raise LogError(f"Temperature error. Register {register}, input signal out of ADC range")

    if register.id < 8:
        temperature = temperature_conversion_1(value)
    else:
        temperature = temperature_conversion_2(value)

    widget.display(temperature)


def temperature_conversion_1(value):
    return 1.65 / 2**24 * ((value & 0x0FFFFFE0) >> 5) #+ 1.65

def temperature_conversion_2(value):
    return (value & 0x0FFFFFFF) / 32. / 1570 * 3.3 - 273


def convert_int32_to_bitarray(value):
    value_binary_str = '{:032b}'.format(value)
    value_bitarray = bitarray(value_binary_str[::-1])
    return value_bitarray


def power_regulator_status(window, cmd, params):
    register, value = params
    value_bitarray = convert_int32_to_bitarray(value)

    load_bitarray_config(window, value_bitarray, power_status_fields, power_status_data)


def clock_status(window, cmd, params):
    register, value = params
    value_bitarray = convert_int32_to_bitarray(value)

    load_bitarray_config(window, value_bitarray, clock_status_fields, clock_status_data)


def link_status(window, cmd, params):
    register, value = params
    value_bitarray = convert_int32_to_bitarray(value)

    load_bitarray_config(window, value_bitarray, link_status_fields, link_status_data)


def run_status(window, cmd, params):
    register, value = params
    value_bitarray = convert_int32_to_bitarray(value)

    for field, bit_slice in run_status_fields.items():
        value = read_bitarray_slice(value_bitarray, bit_slice)
        window.update_log_info('', f'{field}: {value}')


def tofpet_status(window, cmd, params):
    register, value = params
    value_bitarray = convert_int32_to_bitarray(value)

    for field, bit_slice in tofpet_status_fields.items():
        value = read_bitarray_slice(value_bitarray, bit_slice)
        window.update_log_info('', f'{field}: {value}')
    load_bitarray_config(window, value_bitarray, tofpet_status_fields, tofpet_status_data)
