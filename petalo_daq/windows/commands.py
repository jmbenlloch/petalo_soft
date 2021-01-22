from .. network.petalo_network  import MESSAGE
from .. network.client_commands import build_sw_register_read_command
from .. network.client_commands import build_hw_register_read_command
from .. network.client_commands import build_sw_register_write_command
from .. network.client_commands import build_hw_register_write_command

def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_sendCmd      .clicked.connect(send_commands  (window))
    window.pushButton_clearResponse.clicked.connect(clear_responses(window))



def send_commands(window):
    """
    Function to clean responses from the DAQ

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        cmd_input = window.plainTextEdit_cmdSend.toPlainText()
        for cmd_str in cmd_input.split('\n'):
            print("new_command: ", cmd_str)
            cmd = eval(cmd_str)
            window.plainTextEdit_cmdResponse.insertPlainText(f'Sending command: {cmd}\n')
            window.tx_queue.put(cmd)

    return on_click


def clear_responses(window):
    """
    Function to clean responses from the DAQ

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        window.plainTextEdit_cmdResponse.clear()

    return on_click

