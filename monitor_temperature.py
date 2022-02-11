from time import time
from time import sleep
import numpy as np
from random import gauss
import matplotlib.pyplot as plt
from datetime import datetime
import os
import pyvisa
# Here, we have to import the equipment

# I reccoment we call it LS331

rm = pyvisa.ResourceManager()
LS331 = rm.open_resource("GPIB0::10::INSTR")

# file creation functions

def create_file(file_name, directory):
    file = open(directory + file_name + '.dat', "w")                                    #Abre arquivo de data
    file.write('[Header]\nTIMEMODE, SECONDS, RELATIVE\nTITLE, Python Log Data File\n')  #Header of data for MultiVu
    file.write('[Data]\n Time (s), Temperature (K)\n')
    os.fsync(file)
    file.flush()
    return

def write2file(file,dir,t,T):
    file = open(dir + file + '.dat', "a")
    file.write(str(t)+","+str(T)+"\n" )
    os.fsync(file)
    file.flush()
    return

# Creation of functions for the LakeShore 331 Temp. Controller.

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

def waiting_time(temperature):
    ref_temp = [1, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300]
    # ref_time = [1*10**-1, 2*10**-1, 3*10**-1, 4*10**-1, 5*10**-1, 6*10**-1, 7*10**-1, 8*10**-1, 9*10**-1, 10*10**-1, 11*10**-1]
    ref_time = [1]*len(ref_temp)
    aux = np.absolute(np.array(ref_temp) - np.array([temperature]*len(ref_temp)))
    # print(aux)
    return ref_time[aux.tolist().index(np.min(aux))]

def is_stable(list, ref):
    ref_temp = [1, 10, 20, 30, 50, 75, 100, 150, 200, 250, 300]
    percentual = [100, 5, 2.5, 2.5, 1, 1, 1, 1, 1, 1]
    T = np.average(list[round(len(list)*0.8):])
    aux = np.absolute(np.array(ref_temp) - np.array([T]*len(ref_temp)))
    var = np.var(list[round(len(list)*0.8):])
    if ref - np.sqrt(var) <= T <= ref + np.sqrt(var) and var <= np.absolute(ref*percentual[aux.tolist().index(np.min(aux))]/100):
        return True
    else:
        return False

temp_list = []
time_list = []


directory = 'D:/LQMEC-Julio-group/Python/Data/Data/Users/Guilherme/'
date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_monitoring' + date
create_file(file_name, directory)
t_0 = time()
while True:
	T = read_temperature(LS331, 'A')
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))
