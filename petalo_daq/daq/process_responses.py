from petalo_daq.gui.types import LogError

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


def power_regulator_status(window, cmd, params):
    register, value = params
    widget_name = 'lcdNumber_Temp_{}'.format(tofpet_id)
    widget = getattr(window, widget_name)
