# SW and HW registers with their permissions according to DAQ's docs

sw_registers = {
    0: { # Board diagnosis and status
        0: { # Board id
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00000000,
           },
        1: { # Firmware version
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00000000,
           },
        2: { # Console verbosity level
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        3: { # Session counter
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00000000,
           },
        4: { # Command counter
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00000000,
           },
        5: { # Default timeout
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 0x00000000,
           },
       },
    1: { # Peripheral control
        0: { # LED on/off
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 0x000000AA,
           },
        1: { # Push button & DIP switch status
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00000000,
           },
       },
    2: { # Slow control
        0: { # Temperature sensor 0-7. Raw data
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x16C9B260,
           },
        1: {
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0xCD1745E0,
           },
        2: {
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x30000000,
           },
        3: {
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x15D1747F,
           },
        4: {
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x1E8BA2E0,
           },
        5: {
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x21745D20,
           },
        6: {
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x245D1740,
           },
        7: {
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x25D1747F,
           },
        8: { # Temperature sensor Mezzanine
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x20487132, # ~30 degrees celsius
           },
       },
    3: { #TPULSE
        0: {
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 1,
           },
        1: {
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 121,
           },
        2: {
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 123,
           },
        3: {
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 1,
           },
        4: {
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0,
           },
        5: {
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0,
           },
        6: {
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 0,
           },
        7: {
            'permissions' : {
                'read'  : True,
                'write' : True,
            },
            'value' : 0,
           },

       },
}

hw_registers = {
    0: { # Temperature sensor
        0: { # Temperature sensor control
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
       },
    1: { # Power control
        0: { # TOFPET Power Regulator Control
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        1: { # TOFPET Power Regulator Status
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x800300FF,
           },
       },
    2: { # Clock control
        0: { # Clock Control
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        1: { # LMK Configuration Register
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        2: { # Clock Status
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x0000AF35,
           },
       },
    3: { # TOFPET Control / TOFPET DATA WR
        0: { # TOFPET Link Control Register
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        1: { # TOFPET Link Status Register
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00010000,
           },
        2: { # TOFPET DATA WR Control Register
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        3: { # TOFPET DATA WR Register
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        4: { # TOFPET DATA WR Status
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00000093,
           },
       },
    4: { # Run Control
        0: { # Run Configuration Control
            'permissions' : {
                'read'  : False,
                'write' : True,
            },
            'value' : 0x00000000,
           },
        1: { # Run Status Register
            'permissions' : {
                'read'  : True,
                'write' : False,
            },
            'value' : 0x00000000,
           },
       },
}
