import struct
import socket as sk

from PyQt5.QtCore import pyqtBoundSignal

from bitarray    import bitarray
from threading   import Thread
from collections import OrderedDict
from time        import sleep
from queue       import Empty

from . commands      import code_to_command
from . commands      import sleep_cmd
from . commands      import commands     as cmd
from . commands      import status_codes as status
from . command_utils import parse_first_parameter_in_response


class MESSAGE():
    def __init__(self):
        """
        COMM Protocol (wordlength=32):
        COMMAND + NUMBER OF PARAMs + PARAM1 + PARAM2 + ... + PARAMn

        COMMAND : ID (16 bits) + Destination (16 bits)
            PC -> DAQ Commands (bit 0 = 0)
            DAQ -> PC Commands (bit 0 =1)

            ID: Command Identification Code or ERROR Code
                ERROR Codes: -1 (ERR_BAD_PACKET)
                             -2 (ERR_INVALID_DESTINATION)
                             -3 (ERR_INVALID_COMMAND)
            Destination: DAQ board (PC-> DAQ // DAQ -> PC)

        NUMBER OF PARAMS: N_PARAMS = 1 -> PARAM1 = Status (OK=0,FAIL<0)

        """
        self.dict = OrderedDict([('command',0),('L1_id',0),('n_params',0),('params',0)])
        self.bits = bitarray()


    def __call__(self,in_data):

        self.dict = OrderedDict([('command',0),('L1_id',0),('n_params',0),('params',0)])
        self.bits = bitarray()

        switch = {"<class 'list'>": "encode",
                  "<class 'dict'>": "encode",
                  "<class 'bitarray.bitarray'>":  "decode"
                  }
        method_name = switch.get(str(type(in_data)),"decode")
        method      = getattr(self, method_name, lambda:"Invalid Data")
        return method(in_data)


    def encode(self,dict_in):
        """ Creates Dict, Json and Bitstream from {command,L1_id,args} dict
        """
        if type(dict_in)==type([]):
            command = dict_in[0]
            L1_id   = dict_in[1]
            args    = dict_in[2]
        elif type(dict_in)==type({'a':0,'b':0}):
            command = dict_in['command']
            L1_id   = dict_in['L1_id']
            args    = dict_in['params']

        # Error in args syntax
        try:
            len_args = len(args)
        except:
            args = [args]
            len_args = len(args)


        # TODO: Deal with errors
        #  command = getattr(cmd, cmd_str)

        #  if (command.value.n_params != len(args)):
        #      print("Parameter Error")
        #      self.bits = -1
        #  else:
        self.dict['command']  = command.value.code
        self.dict['L1_id']    = L1_id
        self.dict['n_params'] = len(args) #+ 2
        if (str(type(args[0]))=="<class 'int'>"):
            self.dict['params']   = args
        else:
            self.dict['params']   = [int(x,0) for x in args]
        self.translate()

        return self.bits


    def decode(self,bit_stream):
        """ Decodes Bitstream into Dict and JSON
        """
        v = memoryview(bit_stream)
        # COMMAND_ID + DAQ_ID = 4 bytes
        # N_PARAMETERS        = 4 bytes

        command  = struct.unpack('<H',v[0:2])[0]
        L1_id    = struct.unpack('<H',v[2:4])[0]
        n_params = struct.unpack('<I',v[4:8])[0]
        #format = '<'+str(n_params-2)+'I'
        format = '<'+str(n_params)+'I'
        params   = struct.unpack(format,v[8:])

        # Extract COMMAND
        command = code_to_command[command]

        # Parse first value in the response
        if command != cmd.CON_STATUS:
            params = list(params)
            params[0] = parse_first_parameter_in_response(params[0])

        self.dict['command']  = command
        self.dict['L1_id']    = L1_id
        self.dict['n_params'] = n_params
        #self.dict['params']   = [hex(x) for x in params]
        self.dict['params']   = params

        return self.dict


    def translate(self):
        """ Auxiliary function:
            Translates Message in Dict into bit array (decimal base)
        """
        byte_frame = bytearray()

        for key in self.dict.keys():
            switch = {"command":'<H', "L1_id":'<H',"n_params":'<I',"params":'<I'}
            case = switch.get(key,0)
            if key=="params":
                set = self.dict[key]
            else:
                set = [self.dict[key]]
            for word in set:
                byte_frame.extend(bytearray(struct.pack(case,word)))

        self.bits = byte_frame


class SCK_TXRX(Thread):
    """ PETALO DAQ Transmission Socket.
        Designed to run as TXRX thread

        Parameters (General)
        'stopper'     : Flag to stop thread execution
        'queue'       : Queue to send data

        Parameters (taken from UC data)
        'ext_ip'      : DAQ IP Address
        'port'        : DAQ port
        'buffer_size' : Size of data to receive
    """

    def __init__(self, config, tx_queue, rx_queue, stopper):
        super(SCK_TXRX,self).__init__()
        self.config     = config
        self.queue      = tx_queue
        self.out_queue  = rx_queue
        self.stopper    = stopper
        self.M          = MESSAGE()
        self.s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        # ADD TIMEOUT Mechanism !!!!
        self.s.settimeout(5.0)

        self.buffer    = int(config['buffer_size'])

        try:
            self.s.connect((self.config['ext_ip'],
                            int(self.config['port'])))
            data_r = self.M(bytearray(self.s.recv(self.buffer)))
        except Exception as e:
            # TODO test
            # control for timeout, no route to host, etc.
            raise ConnectionRefusedError('{}'.format(e))

        self.out_queue.put(data_r)

        if (data_r['command'] != cmd.CON_STATUS):
            raise sk.error('Communication Error (1)')
        elif ((data_r['command'] == cmd.CON_STATUS) and
              (data_r['params'][0] == status.STA_CONNECTION_REJECT.value)):
            IP = sk.inet_ntoa(struct.pack("!I",data_r['params'][1]))
            raise ConnectionRefusedError(f'Unsuccessful: DAQ is already connected to {IP}')
        else:
            print('\n<< Connection Stablished \n>> ')


    def run(self):
        while not self.stopper.is_set():
            try:
                self.item = self.queue.get(True,timeout=0.25)
                # Timeout should decrease computational load
            except Empty:
                pass
                # Wait for another timeout
            else:
                try:
                    #  print("Send: ", self.item)
                    if isinstance(self.item, sleep_cmd):
                        sleep(self.item.time / 1000.)
                        self.queue.task_done()
                    elif isinstance(self.item, pyqtBoundSignal):
                        self.item.emit()
                        self.queue.task_done()
                    else:
                        self.s.send(self.item)
                        self.queue.task_done()
                        # Get DAQ response
                        data_rx = self.s.recv(self.buffer)
                        data = self.M(bytearray(data_rx))
                        self.out_queue.put(data)
                except:
                    print ('\n<< Communication Error - Timeout \n>> ')
        self.s.close()
        sleep(0.5)
        print ("TXRX SOCKET IS DEAD")

