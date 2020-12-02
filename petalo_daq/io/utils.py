import json
from PyQt5    import QtWidgets
from bitarray import bitarray



def find_gui_value_from_bitarray(expected_value, values_dict):
    """
    Function to find the GUI value of a particular bitarray

    Parameters
    expected_value (bitarray): bitarray whose index is to be found.
    value_data (dictionary): Dictionary with the different fields values and defaults
        The structure is the one in gui/widget_data.py

    Returns:
    Object: Index of the correspoding value in "value_data".
    """
    result = -1
    for index, data in values_dict.items():
        if data['value'] == expected_value:
            result = index
            break

    return result


def load_gui_config(window, config):
    """
    Function to update GUI fields with some particular configuration

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    config (dictionary): Dictionary where the keys are widget names and
        the values contains the new value for the widget. For an example look
        at "general_config" in config/default.json
    """
    for field, data in config.items():
        widget = getattr(window, field)
        if isinstance(widget, QtWidgets.QSpinBox):
            widget.setValue(data['value'])


def read_bitarray_into_namedtuple(value_bitarray, params_fields, params_tuple):
    params = {}

    for field, bit_slice in params_fields.items():
        #  print(field, bit_slice)
        value = read_bitarray_slice(value_bitarray, bit_slice)
        params[field] = value
    parameters = params_tuple(**params)

    return parameters


def load_bitarray_config(window, config, config_fields, config_data):
    """
    Function to find the GUI value of a particular bitarray

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    config (bitarray): bitarray to be decoded
    config_fields (dictionary): Dictionary with the corresponding slice for each
        variable. Examples in io/config_params.py
    config_data (dictionary): Dictionary with the different fields values and defaults
        The structure is the one in gui/widget_data.py

    Returns:
    Object: Index of the correspoding value in "value_data".
    """
    for field, bit_slice in config_fields.items():
        #print(field, bit_slice)
        value = read_bitarray_slice(config, bit_slice)
        #  print(field, value)

        gui_field = field
        for key in config_data.keys():
            if(key.endswith(gui_field)):
                gui_field = key

        widget = getattr(window, gui_field)

        if isinstance(widget, QtWidgets.QLineEdit):
            value_int = convert_bitarray_to_int32(value)
            widget.setText('0x{:02X}'.format(value_int))
        else:
            index = find_gui_value_from_bitarray(value, config_data[gui_field]['values'])
            if index == -1:
                raise ValueError(f'Value {value} for {field} not found!')

            if isinstance(widget, QtWidgets.QComboBox):
                widget.setCurrentIndex(index)
            if isinstance(widget, QtWidgets.QCheckBox):
                widget.setChecked(index)
            if isinstance(widget, QtWidgets.QLCDNumber):
                widget.display(index)


def insert_bitarray_slice(config, indices, bits):
    """
    Inserts bits in bitarray config in the positions specified in indices
    Expected behaviour:

    config = bitarray('0000000')
    insert_bitarray_slice(config, range(1, 4), bitarray('111'))

    config -> bitarray('0111000')
    """
    for index, bit in zip(indices, bits):
        config[index] = bit
        #print(index, bit)


def read_bitarray_slice(bits, indices):
    """
    Reads bits fromt bitarray in the positions specified in indices
    Expected behaviour:

    config = bitarray('1110000')
    read_bitarray_slice(config, [3,0,4,1])
     -> bitarray('0101')
    """
    bits_slice = bitarray()
    for index in indices:
        bits_slice.append(bits[index])
        #print(index, bits[index])
    return bits_slice


def convert_bitarray_to_int32(bitarray):
    value = int(bitarray.to01(), 2)
    return value

