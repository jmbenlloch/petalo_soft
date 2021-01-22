from PyQt5 import QtWidgets

from . access_level import user_access


def populate_fields(window, gui_data):
    """
    Function to populate with data and options the different fields in the GUI

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    gui_data (dictionary): Dictionary with the different fields values and defaults
        The structure is the one in gui/widget_data.py
    """
    for field, entries in gui_data.items():
        widget = getattr(window, field)
        # Add all items in the case of QComboBox
        if isinstance(widget, QtWidgets.QComboBox):
            for index, item in entries['values'].items():
                widget.addItem(item['text'], item['value'])

        # Set default value for different widget types
        if isinstance(widget, QtWidgets.QComboBox):
            widget.setCurrentIndex(entries['default'])
        if isinstance(widget, QtWidgets.QCheckBox):
            widget.setEnabled(entries['default'])
        if isinstance(widget, QtWidgets.QSpinBox):
            widget.setValue     (entries['default'])
            if 'min' in entries:
                widget.setMinimum   (entries['min'])
            if 'max' in entries:
                widget.setMaximum   (entries['max'])
            if 'step' in entries:
                widget.setSingleStep(entries['step'])
        if isinstance(widget, QtWidgets.QDoubleSpinBox):
            widget.setValue     (entries['default'])
            if 'min' in entries:
                widget.setMinimum   (entries['min'])
            if 'max' in entries:
                widget.setMaximum   (entries['max'])
            if 'step' in entries:
                widget.setSingleStep(entries['step'])
            if 'decimals' in entries:
                widget.setSingleStep(entries['decimals'])



def enable_fields(window, user):
    """
    Function to enable/disable GUI fields according to the user's access level

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    user (string): authenticated user name
    """
    for field, access_levels in user_access.items():
        widget = getattr(window, field)
        access = access_levels[user]
        widget.setEnabled(access)


def path_browser_config(window, filetype_str, widget_name):
    """
    Factory of functions to create a widget to select a file

    Parameters
    window (QApplication): Parent window
    filetype_str (string): Description of the filetype to be selected
    widget (QtWidgets): Widget to show the filename selected.

    Returns:
    function: Function to be connected to the file select button
    """
    path = '/home/jmbenlloch/next/petalo/petalo_soft/'

    def file_browser():
        file_select = QtWidgets.QFileDialog.getOpenFileName(window,
                                        'Open file', path, filetype_str)

        fname = file_select[0]
        widget = getattr(window, widget_name)
        widget.setText(fname)

    return file_browser



def read_parameters(window, fields_data, params_tuple):
    """
    Function to read a set of field values from the GUI and store them in
    a named tuple. The names in the GUI (field_data) must follow the pattern
    {widgetType}_{name} such as comboBox_e_hysteresis. The names in params_tuple
    will be the same removing the first word before "_".


    Parameters
    window (QApplication): Parent window
    fields_data (dictionary): TODO
    parameters (namedtuple creator): NamedTuple creator with a matching
        structure for fields_data. Samples in gui/types.py

    Returns:
    namedtuple: Filled with the corresponding values for each parameter
    """
    params = {}

    for field, values in fields_data.items():
        fieldname = '_'.join(field.split('_')[1:])
        #print(field, fieldname)

        widget = getattr(window, field)
        if isinstance(widget, QtWidgets.QComboBox):
            #print(widget.currentData())
            params[fieldname] = widget.currentData()
        if isinstance(widget, QtWidgets.QCheckBox):
            status = widget.isChecked()
            #print(field, status)
            params[fieldname] = fields_data[field]['values'][status]['value']
        if isinstance(widget, QtWidgets.QSpinBox):
            params[fieldname] = widget.value()
        if isinstance(widget, QtWidgets.QDoubleSpinBox):
            params[fieldname] = int(widget.value())
    #print(params)

    #global_config = types.global_config_tuple(**params)
    parameters = params_tuple(**params)
    #  print(parameters)

    return parameters
