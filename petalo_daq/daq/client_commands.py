from petalo_daq.daq.petalo_network    import MESSAGE
from petalo_daq.daq.command_utils import encode_register_address
from petalo_daq.daq.commands      import commands as cmd

def build_sw_register_write_command(daq_id, register_group, register_id, value):
    """
    Create a SW register write command

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Software Register Group identifier, check DAQ docs
    register_id    (int): Software Register identifier, chech DAQ docs
    value          (int): Value to be written (32 bits)

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    address = encode_register_address(register_group, register_id)

    message = MESSAGE()
    m = message({
        'command': cmd.SOFT_REG_W,
        'L1_id'   : daq_id,
        'params'  : [address, value]
    })
    return m


def build_hw_register_write_command(daq_id, register_group, register_id, value):
    """
    Create a HW register write command

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Hardware Register Group identifier, check DAQ docs
    register_id    (int): Hardware Register identifier, chech DAQ docs
    value          (int): Value to be written (32 bits)

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    address = encode_register_address(register_group, register_id)

    message = MESSAGE()
    m = message({
        'command': cmd.HARD_REG_W,
        'L1_id'   : daq_id,
        'params'  : [address, value]
    })
    return m


def build_sw_register_read_command(daq_id, register_group, register_id):
    """
    Create a SW register read command

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Software Register Group identifier, check DAQ docs
    register_id    (int): Software Register identifier, chech DAQ docs

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    address = encode_register_address(register_group, register_id)

    message = MESSAGE()
    m = message({
        'command': cmd.SOFT_REG_R,
        'L1_id'   : daq_id,
        'params'  : [address]
    })
    return m


def build_hw_register_read_command(daq_id, register_group, register_id):
    """
    Create a HW register write command

    Parameters:
    daq_id         (int): L1 ID
    register_group (int): Hardware Register Group identifier, check DAQ docs
    register_id    (int): Hardware Register identifier, chech DAQ docs

    Returns:
    bytearray: Command encoded. Check DAQ docs
    """
    address = encode_register_address(register_group, register_id)

    message = MESSAGE()
    m = message({
        'command': cmd.HARD_REG_R,
        'L1_id'   : daq_id,
        'params'  : [address]
    })
    return m
