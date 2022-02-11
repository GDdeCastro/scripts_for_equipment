# By M. Henry Przygocki, December 2021
# G. de Castro contribution, January 2022
# Packages importation
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

# temperature controller
ls = rm.open_resource('GPIB0::10::INSTR')
# lock-in
sr = rm.open_resource('GPIB0::12::INSTR')
sr1 = DSP7265("GPIB0::12::INSTR")
sr1.timeout = 50000
# nanovoltmeter
nv1 = rm.open_resource('GPIB0::9::INSTR')
# nv2 = rm.open_resource('GPIB0::6::INSTR')

print(rm.list_resources())

# Getting the date
date = datetime.today().strftime('%Y-%m-%d')

# general definitions
R = 99.8 # control resistance

# Commands dictionary
    
def create_file(file_name, directory):
    file = open(directory + file_name, "w")                                    #Abre arquivo de data
    file.write('[Header]\nTIMEMODE, SECONDS, RELATIVE\nTITLE, Python Log Data File\n')  #Header of data for MultiVu
    file.write('[Data]\n Time (s), 331 Temperature (K), V (V)\n')
    file.flush()
def write2file(file_name, directory, t, temp, v1):
    file = open(directory + file_name, "a")
    file.write(str(t)+","+str(temp)+","+str(v1)+"\n" )
    os.fsync(file)
    file.flush()

# 331

def set_PID(instrument, P, I, D, loop = 1):
    '''
    This command sets the PID
    Loop: 1 or 2
    P value: 0.1 to 1000
    I value: 0.1 to 1000
    D value: 0 to 200
    '''
    term = 'Cr Lf' # This is the terminator phrase
    instrument.write(f'PID {loop}, {P}, {I}, {D}')
    return

def query_PID(instrument, loop = 1):
    '''
    This command reads the PID
    Loop: 1 or 2
    '''

    aux = instrument.query(f'PID? {loop}')
    return aux

def set_setpoint(instrument, temperature, loop = 1):
    '''
    Defined using Kelvin as a scale (necessary to check at the instrument whether this is the set unit.
    Read manual Page 4-5.
    '''

    instrument.write(f'SETP {loop}, {temperature}')
    return

def set_ramp(instrument, rate, onoff = 1, loop = 1):

    instrument.write(f'RAMP {loop}, {onoff}, {rate}')
    return

def query_setpoint(instrument, loop = 1):
    term = 'Cr Lf' # This is the terminator phrase
    aux = instrument.query(f'SETP? {loop}')
    return float(aux)

def set_heater_range(instrument, ran):
    '''
    0 -> Off
    1 -> Low (0.5 W)
    2 -> Medium (5 W)
    3 -> High (50 W)
    '''

    instrument.write(f'RANGE {ran}')
    return

def query_heat_range(instrument):

    aux = instrument.query('RANGE? ')
    return float(aux)

def set_manual_heater_power(instrument, percentage, loop = 1):
    '''
    loop: 1 or 2
    The value is a percentage value of power:
    ex: MOUT 1,22.45 -> Control Loop 1 Manual Heater POwer output set to 22.45%
    '''

    instrument.write(f'MOUT {loop}, {percentage}')
    return

def query_manual_heater_power(instrument, loop = 1):

    aux = instrument.query(f'MOUT? {loop}')
    return aux

def read_temperature(instrument, channel = 'a'):
    '''
    channel = A or B
    '''

    aux = instrument.query(f'KRDG? {channel}')
    return float(aux)

# Lock-In

def set_current(I,f):
    """
    Sets the desired current based on the resistance of the Heater
    """
    global R
    V = round(R*I,5)
    sr.write(f"OA.{V}")
    sr.write(f"OF.{round(f,3)}")

# Nano Voltmeters

def set_nano(nv, ch):
    nv.write('SENS:FUNC VOLT') # sets nv to voltage reading
    nv.write(f':SENS:VOLT:CHAN{ch}:RANG:AUTO 1')
    return

def voltage(nv, ch):
    nv.write(f':SENS:VOLT:CHAN{ch}:LPASS off')
    # nv.write(f'SENS:DATA:FRES?')
    # which one is better? comment one of them and test
    t = nv.query(":READ?")
    return float(t)

def stable(x, y, n, sigma, slope):
    if len(x) != len(y):
        print('The lists are not in the correct format.')
        return False
    if len(y) < n or len(y) == 0:
        return False
    desv_pad = np.std(y[-n:])
    a, b = np.polyfit(x[-n:], y[-n:], 1)
    if desv_pad <= sigma and a <= slope:
        return True
    else:
        return False
    

dir = "D:/LQMEC-Julio-group/Python/Data/Data/Users/Guilherme/"

# The first measurement (lock in turned off) will be perfomed during the cooling of the system

def measure(file_name, directory, interval, stable_time, onoff, sigma, slope): # stable time in minutes
    create_file(file_name, directory)
    # settings
    if onoff:
        set_current(25*10**(-3), 1.06) # the frequency depends on the working freq
    else:
        set_current(0, 1.06)
    set_nano(nv1, 1)
    # set_nano(nv2)
    n = stable_time*60//interval
    t_0 = time.time()
    t = []
    T = []
    v1 = []
    v2 = []
    while not stable(t, T, n, sigma, slope):
        t_i = time.time() - t_0
        T_i = read_temperature(ls)
        v1_i = voltage(nv1, 1)
        # v2_i = voltage(nv2)
        t.append(t_i)
        T.append(T_i)
        v1.append(v1_i)
        # v2.append(v2_i)
        # v12_i = np.absolute(v1_i - v2_i)
        write2file(file_name,directory,t_i,T_i,v1_i)
        sleep(interval)
    return

# here, you need to perform measurements of V and T every interval (you are not controlling the temperature, just measuring)

# this will be performed during the cooling of the system:

def cooling_measurement(onoff = True):
    interval = 3
    stable_time = 15
    sigma = 0.3
    slope = (1)*1/(stable_time * 60)

    set_heater_range(ls,0) #turned the heater off
    if onoff:
        name = 'cooling_lockin_on_data.dat'
    else:
        name = 'cooling_lockin_off_data.dat'
    measure(name, dir, interval, stable_time, onoff, sigma, slope) # the slope is calculated so that temperature changes less than a degree within the stable_time
    return

# This is to be performed during the heating of the system (compressor turned off)

def heating_measurement(onoff = False):
    interval = 3
    stable_time = 10
    sigma = 0.1
    slope = (1/3)*1/(stable_time * 60)

    set_heater_range(ls,0) #turned the heater off
    if onoff:
        name = 'heating_lockin_on_data.dat'
    else:
        name = 'heating_lockin_off_data.dat'
    measure(name, dir, interval, stable_time, onoff, sigma, slope) # the slope is calculated so that temperature changes less than a degree within the stable_time
    return

# Here, you will change temperature in a controlled way and perform the measurements.

def ramped_measurement(target_T, onoff):
    interval = 3
    stable_time = 15
    if target_T > 50:
        sigma = 0.01
        slope = (1/2)*1/(stable_time * 60)
    else:
        sigma = 0.1
        slope = (1)*1/(stable_time * 60)
        
    set_heater_range(ls,0)
    
    if target_T <= 103:
        set_PID(ls, 150, 20, 0) # P I D
        set_ramp(ls, 0.1)
    elif target_T <= 155:  
        set_PID(ls, 200, 10, 0) # P I D
        set_ramp(ls, 0.1)
    else:
        set_PID(ls, 300, 10, 0) # P I D
        set_ramp(ls, 0.1)

    set_setpoint(ls, target_T)
    if onoff:
        name = f'ramped_lockin_on_target_{target_T}K.dat'
    else:
        name = f'ramped_lockin_off_target_{target_T}K.dat'    
    measure(name, dir, interval, stable_time, onoff, sigma, slope) # the slope is calculated so that temperature changes less than a degree within the stable_time
    
    return

# heating_measurement()
nv1.write('*RST')
ramped_measurement(15, False)
