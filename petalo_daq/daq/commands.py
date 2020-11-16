from collections import namedtuple
from enum        import Enum
from dataclasses import dataclass

command_tuple  = namedtuple('command_tuple' , ['code' , 'n_params'])
register_tuple = namedtuple('register_tuple', ['group', 'id'])

class status_codes(Enum):
    STA_CONNECTION_REJECT   =  1
    STA_CONNECTION_ACCEPT   =  0
    ERR_BAD_PACKET          = -1
    ERR_INVALID_DESTINATION = -2
    ERR_INVALID_COMMAND     = -3
    ERR_INVALID_REGISTER    = -4
    ERR_READ_ONLY           = -5
    ERR_WRITE_ONLY          = -6
    ERR_NOT_AVAILABLE       = -7


class commands(Enum):
    CON_STATUS   = command_tuple( 1, 2) # 1 or 2 params
    SOFT_REG_W   = command_tuple( 2, 2)
    SOFT_REG_W_r = command_tuple( 3, 1)
    SOFT_REG_R   = command_tuple( 4, 1)
    SOFT_REG_R_r = command_tuple( 5, 2)
    HARD_REG_W   = command_tuple( 6, 2)
    HARD_REG_W_r = command_tuple( 7, 1)
    HARD_REG_R   = command_tuple( 8, 1)
    HARD_REG_R_r = command_tuple( 9, 2)

code_to_command = {cmd.value.code : cmd    for cmd    in commands}
code_to_status  = {status.value   : status for status in status_codes}


@dataclass
class sleep_cmd:
    time: int #sleep time in ms
