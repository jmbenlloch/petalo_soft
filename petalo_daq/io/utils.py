import json
from PyQt5 import QtWidgets


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
        print(field, bit_slice)
        value = config[bit_slice]
        print(field, value)

        gui_field = f'comboBox_{field}'
        if gui_field not in config_data:
            gui_field = f'checkBox_{field}'

        print(gui_field)

        index = find_gui_value_from_bitarray(value, config_data[gui_field]['values'])
        if index == -1:
            raise ValueError(f'Value {value} for {field} not found!')

        widget = getattr(window, gui_field)

        if isinstance(widget, QtWidgets.QComboBox):
            widget.setCurrentIndex(index)
        if isinstance(widget, QtWidgets.QCheckBox):
            widget.setChecked(index)

