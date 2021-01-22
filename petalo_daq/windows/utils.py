from petalo_daq.network.client_commands import build_hw_register_write_command
from petalo_daq.network.client_commands import build_hw_register_read_command
from petalo_daq.network.commands        import register_tuple
from petalo_daq.io.utils         import insert_bitarray_slice

from petalo_daq.gui.types        import tofpet_config_tuple
from petalo_daq.io.config_params import tofpet_config_fields
from petalo_daq.network.commands        import sleep_cmd

from bitarray import bitarray

def build_tofpet_configuration_register_value(tofpet_config):
    '''
    Read a NamedTuple with all the command parameters as bitarrays
    and returns the int value to be sent in the command

    Parameters:
    tofpet_config (NamedTuple): Configuration parameters

    Returns:
    int: Value for the tofpet control register command
    '''

    tofpet_config_bitarray = bitarray('0'*32)
    for field, positions in tofpet_config_fields.items():
        value = getattr(tofpet_config, field)
        insert_bitarray_slice(tofpet_config_bitarray, positions, value)

    value = int(tofpet_config_bitarray.to01()[::-1], 2) #reverse bitarray and convert to int in base 2
    return value


def build_tofpet_ram_address_command(daq_id, address_bitarray):
    tofpet_config = tofpet_config_tuple(TOFPET_CONF_START = bitarray('0'),
                                        TOFPET_CONF_VERIFY     = bitarray('0'),
                                        TOFPET_CONF_ERROR_RST  = bitarray('0'),
                                        TOFPET_CONF_WR    = bitarray('1'),
                                        TOFPET_CONF_ADDR  = address_bitarray,
                                        TOFPET_CONF_MODE       = bitarray('00'),
                                        TOFPET_CONF_CH_SEL     = bitarray('000000'))

    value    = build_tofpet_configuration_register_value(tofpet_config)
    register = register_tuple(group=3, id=2)
    command  = build_hw_register_write_command(daq_id, register.group, register.id, value)
    return command


def tofpet_status(window):
    """
    Function to read the tofpet status register.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        daq_id = 0
        command = build_hw_register_read_command(daq_id, register_group=3, register_id=4)
        window.tx_queue.put(command)

        window.update_log_info("TOFPET status sent",
                               "TOFPET status command sent")

    return on_click


def set_run_mode(window):
    """
    Function to set the run mode

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        qdc_mode_index = window.comboBox_qdc_mode.currentIndex()
        window.comboBox_intg_en       .setCurrentIndex(qdc_mode_index)
        window.comboBox_intg_signal_en.setCurrentIndex(qdc_mode_index)

        if (window.checkBox_counter_en.isChecked() == False):
            if window.comboBox_qdc_mode.currentIndex() == 0:
                window.comboBox_RUN_MODE.setCurrentIndex(0)

            if window.comboBox_qdc_mode.currentIndex() == 1:
                window.comboBox_RUN_MODE.setCurrentIndex(1)
        else:
            window.comboBox_RUN_MODE.setCurrentIndex(2)

    return on_click
