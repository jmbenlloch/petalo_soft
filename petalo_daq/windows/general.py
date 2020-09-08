def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.SpinBox_Buffer    .editingFinished.connect(store_general_data(window))
    window.SpinBox_Pretrigger.editingFinished.connect(store_general_data(window))
    window.SpinBox_Triggers  .editingFinished.connect(store_general_data(window))


def store_general_data(window):
    """
    Function read the values from general configuration tab and store them

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        data = {
            'SpinBox_Buffer' : {
                'value' : window.SpinBox_Buffer.value()
            },
            'SpinBox_Pretrigger' : {
                'value' : window.SpinBox_Pretrigger.value()
            },
            'SpinBox_Triggers' : {
                'value' : window.SpinBox_Triggers.value()
            },
        }

        window.data_store.insert('general_config', data)

    return on_click

