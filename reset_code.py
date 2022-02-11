import pymeasure
import pyvisa
import scipy.optimize as sp
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from pyvisa.constants import StopBits, Parity
from time import sleep
import time
from datetime import datetime
from pymeasure.instruments.signalrecovery import DSP7265

# Calling the equipment
rm = pyvisa.ResourceManager()
R = 99.8
# temperature controller
ls = rm.open_resource('GPIB0::10::INSTR')
# lock-in
sr = rm.open_resource('GPIB0::12::INSTR')

sr1 = DSP7265("GPIB0::12::INSTR")
sr1.timeout = 50000
# nanovoltmeter
nv1 = rm.open_resource('GPIB0::6::INSTR')
# nv2 = rm.open_resource('GPIB0::9::INSTR')

print(rm.list_resources())

# LS331

def set_heater_range(instrument, ran):
    '''
    0 -> Off
    1 -> Low (0.5 W)
    2 -> Medium (5 W)
    3 -> High (50 W)
    '''

    instrument.write(f'RANGE {ran}')
    return

def set_ramp(instrument, rate, onoff = 1, loop = 1):
   
    # print(f'RAMP {loop},{onoff},{rate}')
    instrument.write(f'RAMP {loop},{onoff},{rate}')
    return


# Lock-In

def set_current(I,f):
    """
    Sets the desired current based on the resistance of the Heater
    """
    global R
    V = round(R*I,5)
    sr.write(f"OA.{V}")
    sr.write(f"OF.{round(f,3)}")

# turns the heater off
set_heater_range(ls,0)

# turns off the ramp
set_ramp(ls, 0, 0)

# sets the lock in signal to 0V
set_current(0, 1.06)
