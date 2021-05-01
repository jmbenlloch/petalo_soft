from bitarray  import bitarray
import numpy as np

from .. network.client_commands import build_sw_register_write_command
from .. network.client_commands import build_sw_register_read_command
from .. network.commands        import register_tuple
from .  utils                   import tofpet_status


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """
    window.pushButton_TPULSE_Reset    .clicked.connect(tpulse_reset         (window, verbose=True))
    window.pushButton_TPULSE_Config   .clicked.connect(tpulse_config        (window, verbose=True))
    window.pushButton_TPULSE_Continous.clicked.connect(tpulse_continous_mode(window, verbose=True))
    window.pushButton_TPULSE_SendPulse.clicked.connect(tpulse_send_pulse    (window, verbose=True))
    window.pushButton_TPULSE_status   .clicked.connect(tpulse_status        (window, verbose=True))
    window.pushButton_TPULSE_LimitedTime.clicked.connect(tpulse_limited_time(window, verbose=True))



# TODO: Test this
def read_sw_status_register(window, register_group, register_id):
    daq_id = 0
    command = build_sw_register_read_command(daq_id, register_group, register_id)
    window.tx_queue.put(command)


def tpulse_status(window, verbose=True):
    """
    Read status registers

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        read_sw_status_register(window, register_group=3, register_id=0)
        read_sw_status_register(window, register_group=3, register_id=1)
        read_sw_status_register(window, register_group=3, register_id=2)
        read_sw_status_register(window, register_group=3, register_id=3)

        if verbose:
            window.update_log_info("TPULSE status sent",
                                   "TPULSE status command sent")

    return on_click


def tpulse_reset(window, verbose=False):
    """
    Function to reset the TPULSE PLL

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=0)
        value = 0

        command = build_sw_register_write_command(daq_id, register.group, register.id, value)
        # Send command
        window.tx_queue.put(command)
        if verbose:
            window.update_log_info("Reset TPULSE sent",
                                   "Reset TPULSE sent")

    return on_click


def tpulse_send_pulse(window, verbose=False):
    """
    Function to send the TPULSE signal

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=4)
        value = 0

        command = build_sw_register_write_command(daq_id, register.group, register.id, value)
        # Send command
        window.tx_queue.put(command)
        if verbose:
            window.update_log_info("Send TPULSE",
                                   "TPULSE signal sent")

    return on_click


def tpulse_continous_mode(window, verbose=False):
    """
    Function to set/unset continous mode

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=3)
        value = int(window.checkBox_TPULSE_Continous.isChecked())

        command = build_sw_register_write_command(daq_id, register.group, register.id, value)
        # Send command
        window.tx_queue.put(command)

        if verbose:
            window.update_log_info("TPULSE mode",
                                   "TPULSE continous mode updated")

    return on_click


def tpulse_limited_time(window, verbose=False):
    """
    Function to set/unset continous mode

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        #Build command
        daq_id = 0x0000
        register = register_tuple(group=3, id=5)
        value = 0 # not relevant

        command = build_sw_register_write_command(daq_id, register.group, register.id, value)
        # Send command
        window.tx_queue.put(command)

        if verbose:
            window.update_log_info("TPULSE mode",
                                   "TPULSE continous mode for 1ms")

    return on_click


def tpulse_config(window, verbose=False):
    """
    Function to set TPULSE phase/length configuration

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        daq_id = 0x0000
        # Send phase config
        register = register_tuple(group=3, id=1)
        value = int(window.spinBox_TPULSE_Phase.value())
        command = build_sw_register_write_command(daq_id, register.group, register.id, value)
        window.tx_queue.put(command)

        # Send length config
        register = register_tuple(group=3, id=2)
        value = int(window.spinBox_TPULSE_Length.value())
        command = build_sw_register_write_command(daq_id, register.group, register.id, value)
        window.tx_queue.put(command)

        if verbose:
           window.update_log_info("TPLUSE mode",
                                   "TPULSE config sent")

    return on_click

