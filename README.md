# PETALO DAQ software

To execute the software first some environment variables has to be defined. In linux systems can be done with:

`source setup.sh`

Then it can be executed:

`python PETALO_v7.py`

# Structure of the repository

`PETALO_v7.py` → Main file to run the program.

`PETALO_v2.ui` → xml file from `QTCreator` defining the interface.

- **config**: Sample json configuration file
- **database**: Functions to connect to the database and store data.
- **gui**: Data related to GUI fields, access levels...
- **io**: Functions to load/save configuration files. Data store class to keep all the state info centralized.
- **window**: One file per window/tab of the GUI with the relevant functions for those interfaces.

# Users access level

To control which fields are enabled/disabled for each user, a new entry has to be added to `petalo_daq/gui/access_level.py`. The keys are field names (as in `QTCreator`). For each user there will be an entry stating whether the field will be enabled or not for that user. Example:

```
'SpinBox_Buffer' : {
    'admin'   : True,
    'shifter' : True,
    'none'    : False,
}
```

# Data for each field

The file `petalo_daq/gui/widget_data.py` contains one dictionary per window/tab with the different possible values. The keys are widget identifiers as set in `QTCreator`. The values depend on the type of widget.

For `QSpinBox` there is only a default value now. Min/max could be added in the future. Example

```python
'SpinBox_Buffer' : {
        'default' : 5,
},
```

For `QComboBox`, several options can be added. Each one will have an index, a text label for the GUI and an internal value for the application. The default value is set using the index. Example:

```python
'comboBox_tx_nlinks' : {
        'default' : 2,
        'values' : {
            0 : {'value': bitarray('00'),
                 'text' : '1 link activate'},
            1 : {'value': bitarray('01'),
                 'text' : '2 links activate'},
            2 : {'value': bitarray('10'),
                 'text' : '4 links activate'},
        },
    },
```

For `QCheckBox` the indexes are `True` and `False`, each of them having an associated value. Example:

```python
'checkBox_fetp_enable' : {
        'default' : False,
        'values' : {
            False : {'value' : bitarray('0') },
            True  : {'value' : bitarray('1') },
        },
    },
}
```

# How to add a new tab

1. Prepare the interface in `QTCreator`. The naming convention for the fields is `{widgetType}_{identifier}`, such as `comboBox_tx_nlinks`.
2. Add a new dictionary to `petalo_daq/gui/widget_data.py` with the possible values for the new fields.
3. If needed (bitarrays), create a new dictionary in `petalo_daq/io/config_params.py` with the different bit slices and a new namedtuple in `petalo_daq/gui/types.py`)
4. Add a new file in `petalo_daq/windows/` for the related functions. A function `connect_buttons` receiving the main application will be responsible of setting up the functions to be triggered on user actions (like clicks). See any file in `petalo_daq/windows` for examples.
5. In the main file (`PETALO_v7.py`) call the `populate_fields` function for the new tab/window and the `connect_buttons` function defined in the previous step to connect widgets and functions.
6. KEEP IN MIND that relevant status parameters MUST be saved in the central `data_store`. Just by doing that, the config file export function will take care of saving it to json.
7. Add a new function to `petalo_daq/io/configuration.py` to load from json the new fields and call it in `load_configuration_file` (in the same file).

# Functions to be called on button click

The connect_buttons functions in `petalo_daq/windows/*` receive as an argument the main application. This is needed to access the widgets to setup the different triggers for functions (clicks, text edit, checkbox, etc.). To define a function triggered by one of those events, usually the main application will be needed to.

Given the previous requirements, the easiest way to do it is with closures (more or less, functions that store some variable and return another function). For example. In the `connect_buttons` we could have:

```python
window.pushButton_someButton.clicked.connect(action_for_someButon(window))
```

And the corresponding closure:

```python
def set_channels(window):
    def on_click():
        window.update_log_info('Some status', 'some message')

    return on_click
```

In that way, `set_channels(window)` returns a function (the inner `on_click` function) that will be called when `pushButton_someButton` is clicked. This function has access to the main application via the `window` variable.

# TODO

- Add testing functions and setup travis for automated testing
- Manage the database properly
- Add multi-chip support.
- Fix multi-channel support.
