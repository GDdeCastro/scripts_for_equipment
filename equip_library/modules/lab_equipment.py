import pyvisa as visa
import sys
from pyvisa.constants import StopBits, Parity
rm = visa.ResourceManager()

def list_available_instruments():
    '''
    This function lists all instruments that python is able to recognize.
    '''

    return rm.list_resources()

def call_gpib_instrument(gpib_id, gpib_index=0):
    '''
    GPIB ID is the number that goes between ::
        :: gpib_id ::
    GPIB_index is the number that goes after GPIB
        GPIB gpib_index
    '''
    try:
        instr = rm.open_resource(f'GPIB{gpib_index}::{gpib_id}::INSTR')
        return instr
    except:
        sys.exit(f'It was not possible to call the equipment in GPIB{gpib_index}::{gpib_id}::INSTR\n All instruments available are:\n {list_available_instruments()}')
        return False

def call_general_instrument(address, b_rate = 115200, d_bits=8, flow=0):
    '''
    address - complete instrument address (resource name)
    address is a string
    b_rate is the baud_rate
    '''
    if type(address) != str:
        sys.exit(f'the address variable \'{address}\' isn\'t of type str')
    try:
        instr = rm.open_resource(address, baud_rate = b_rate, data_bits=d_bits, flow_control=flow, parity=Parity.none, stop_bits=StopBits.one)
        return instr
    except:
        sys.exit(f'It was not possible to call the equipment in {address}\n All instruments available are:\n {list_available_instruments()}')
        return False

'''
Usual ids...

Lock-In signal recovery 7265 - 12
Nanovoltmeter Keithley 2182 1 - 6
Nanovoltmeter Keithley 2182 2 - 9
Lakeshore 331 - 10
Lakeshore 372 - 11
'''
