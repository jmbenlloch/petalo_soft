from bitarray  import bitarray

from . utils import write_to_lmk_ram

from .. gui.utils        import read_parameters
from .. io.config_params import reverse_range_inclusive

from . register_config           import power_status
from . register_config           import clock_status
from . register_config           import link_status

from .. io.config_params import link_status_fields
from .. gui.types        import link_status_tuple

from .. gui.widget_data  import activate_data
from .. gui.types        import activate_tuple

from .. gui.types        import power_status_tuple
from .. io.config_params import power_status_fields

from .. gui.types        import clock_status_tuple
from .. io.config_params import clock_status_fields

from .. io.utils         import insert_bitarray_slice

from .. network.client_commands import build_hw_register_write_command
from .. network.client_commands import build_sw_register_write_command
from .. network.client_commands import build_sw_register_read_command
from .. network.commands        import register_tuple
from .. network.commands        import sleep_cmd
from .. network.process_responses import temperature_tofpet_to_ch
from .. network.process_responses import convert_int32_to_bitarray


# dispatch
from .. io.utils              import read_bitarray_into_namedtuple
from .. io.command_dispatcher import add_function_to_dispatcher
from .. io.command_dispatcher import check_command_dispatcher
from .. io.command_dispatcher import read_hw_response_from_log
from .. gui.types import dispatchable_fn
from .. gui.types import dispatch_type
from .. gui.types import CommandDispatcherException
from datetime import datetime


def connect_buttons(window):
    """
    Function to connect each button to the function triggered when the button
    is clicked.

    Parameters
    window (PetaloRunConfigurationGUI): Main application
    """

    window.pushButton_calibrate.clicked.connect(read_temperature(window))


def read_temperature(window):
    """
    Function to read temperature sensors.
    It reads the values from the GUI fields and updates the bitarray in
    data_store

    Parameters
    window (PetaloRunConfigurationGUI): Main application

    Returns
    function: To be triggered on click
    """

    def on_click():
        # Read temperature values
        daq_id = 0
        for tofpet_id in range(9):
            print("tofpet_id: ", tofpet_id)
            channel = temperature_tofpet_to_ch[tofpet_id]
            command = build_sw_register_read_command(daq_id, register_group=2, register_id=channel)
            window.tx_queue.put(command)
            window.tx_queue.put(sleep_cmd(500))

        window.update_log_info("Temperature config",
                               "Temperature configuration sent")

    return on_click

