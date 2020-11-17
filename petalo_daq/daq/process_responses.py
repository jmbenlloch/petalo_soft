from petalo_daq.gui.types import LogError

def read_temperature(window, cmd, params):
    reg_to_tofpet = {0 : 1,
                     1 : 3,
                     2 : 5,
                     3 : 7,
                     4 : 0,
                     5 : 2,
                     6 : 4,
                     7 : 6}
    print("Read: ", params)
    register, value = params

    widget_name = 'lcdNumber_Temp_{}'.format(register.id)
    widget = getattr(window, widget_name)

    # Bits 30 and 31 must be zero
    if (value & 0xC0000000) >> 30 != 0:
        widget.display('Err')
        raise LogError(f"Temperature error. Register {register} has not 00 in bits 30, 31")
    if (value & 0x30000000) >> 28 != 0:
        widget.display('Err')
        raise LogError(f"Temperature error. Register {register}, input signal out of ADC range")

    if register.id < 8: # conversion 1
        temperature = 1.65 / 2**24 * (value & 0x0FFFFFFF) #+ 1.65
    else: # conversion 2
        temperature = (value & 0x0FFFFFFF) / 32. / 1570 * 3.3 - 273

    widget.display(temperature)


