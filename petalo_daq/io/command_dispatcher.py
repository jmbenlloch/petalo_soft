from petalo_daq.gui.types import cmd_response_log
from petalo_daq.daq.commands import commands

from petalo_daq.gui.types import dispatch_type
from petalo_daq.gui.types import CommandDispatcherException
from datetime import datetime


def initialize_command_dispatcher(window):
    command_dispatcher = {
        'loop_counter' : 0,
        'fn_list'      : [],
    }
    command_sw_responses = {}
    command_hw_responses = {}

    window.data_store.insert('command_dispatcher'   , command_dispatcher)
    window.data_store.insert('command_hw_responses' , command_hw_responses)
    window.data_store.insert('command_sw_responses' , command_sw_responses)


def read_sw_response_from_log(window, register):
    responses = window.data_store.retrieve('command_sw_responses')
    print("read_sw_response_from_log: ")
    print(register)
    print(responses)
    result = responses.get(register, None)
    return result


def read_hw_response_from_log(window, register):
    responses = window.data_store.retrieve('command_hw_responses')
    result = responses.get(register, None)
    return result


def add_response_to_dispatcher_log(window, register, cmd_response):
    print(cmd_response)
    cmd       = cmd_response['command']

    field_name = ''
    if (cmd == commands.CON_STATUS):
        field_name = 'command_sw_responses'
    if (cmd == commands.SOFT_REG_W_r) or (cmd == commands.SOFT_REG_R_r):
        field_name = 'command_sw_responses'
    if (cmd == commands.HARD_REG_W_r) or (cmd == commands.HARD_REG_R_r):
        field_name = 'command_hw_responses'


    responses = window.data_store.retrieve(field_name)
    responses[register] = cmd_response_log(timestamp = datetime.now(),
                                           cmd       = cmd_response)
    window.data_store.insert(field_name, responses)

    #  print(window.data_store.data)


def add_function_to_dispatcher(window, dispatch_fn):
    print("add fn to dispatcher")
    dispatcher   = window.data_store.retrieve('command_dispatcher')
    fn_list      = dispatcher['fn_list']
    fn_list.append(dispatch_fn)
    dispatcher['fn_list'] = fn_list
    window.data_store.insert('command_dispatcher', dispatcher)


def check_command_dispatcher(window):
    print("execute dispatcher")
    dispatcher   = window.data_store.retrieve('command_dispatcher')
    fn_list      = dispatcher['fn_list']
    loop_counter = dispatcher['loop_counter']

    try:
        current_fn = fn_list[0]

        print(current_fn.type == dispatch_type.function)
        print(current_fn.type == dispatch_type.function)
        if current_fn.type == dispatch_type.function:
            # Execute the function and remove from list
            print("dispatch function")
            current_fn.fn()
            fn_list.pop(0)

        if current_fn.type == dispatch_type.loop:
            # if the function has already been executed, then check condition
            if loop_counter > 0:
                if current_fn.condition_fn():
                    # if the condition is satisfied, remove fn from list
                    fn_list.pop(0)
                    loop_counter = 0
                    # TODO check
                    check_command_dispatcher(window)
                else:
                    # if false, keep trying
                    current_fn.fn()
                    loop_counter += 1
            else:
                # if this is the first time this element is executed
                # it does not make sense to check the condition yet
                current_fn.fn()
                loop_counter += 1
    except CommandDispatcherException as e:
        window.update_log_info("", str(e))
        # Stop and reset data
        fn_list      = []
        loop_counter = 0
    except Exception as e:
        print(e)

    dispatcher['fn_list']      = fn_list
    dispatcher['loop_counter'] = loop_counter
    window.data_store.insert('command_dispatcher', dispatcher)
    print(dispatcher)
