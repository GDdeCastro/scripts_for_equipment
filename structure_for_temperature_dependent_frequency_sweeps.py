from time import time
from time import sleep
import numpy as np
from random import gauss
import matplotlib.pyplot as plt
from datetime import datetime
import os
import pyvisa
import frequency_sweep_module
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


directory = 'D:/LQMEC-Julio-group/Python/Data/Data/Users/Guilherme/gold_iron_data/'
date = datetime.today().strftime('%d-%m-%Y')

t_0 = time()

##################################################

n = 1

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 11) # in Kelvin
sleep_time = 1 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(11)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)


##################################################
n = 2

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 16) # in Kelvin
sleep_time = 1 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(16)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)


##################################################
n = 3

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 23) # in Kelvin
sleep_time = 1 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(23)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 4

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 30) # in Kelvin
sleep_time = 8 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(30)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

'''
##################################################
n = 5

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 40) # in Kelvin
sleep_time = 15 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(40)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 6

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 50) # in Kelvin
sleep_time = 10 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(50)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 7

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 63) # in Kelvin
sleep_time = 10 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(63)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 8

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 77) # in Kelvin
sleep_time = 10 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(77)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 9

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 80) # in Kelvin
sleep_time = 10 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(80)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 10

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 89) # in Kelvin
sleep_time = 10 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(89)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 11

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 95) # in Kelvin
sleep_time = 2 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(95)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 12

set_PID(LS331, 150, 20, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 103) # in Kelvin
sleep_time = 15 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(103)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 13

set_PID(LS331, 200, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 110) # in Kelvin
sleep_time = 5 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(110)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 14

set_PID(LS331, 200, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 119) # in Kelvin
sleep_time = 15 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(119)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 15
set_PID(LS331, 200, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 127) # in Kelvin
sleep_time = 15 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(127)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 16

set_PID(LS331, 200, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 135) # in Kelvin
sleep_time = 15 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(135)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 17

set_PID(LS331, 200, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 140) # in Kelvin
sleep_time = 15 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(140)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 18

set_PID(LS331, 300, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 178) # in Kelvin
sleep_time = 20 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(178)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 19

set_PID(LS331, 300, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 215) # in Kelvin
sleep_time = 20 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(215)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 20

set_PID(LS331, 300, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 252) # in Kelvin
sleep_time = 20 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(252)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)

##################################################
n = 21

set_PID(LS331, 300, 10, 0) # P I D
set_heater_range(LS331, 3) # from 0 to 3
set_setpoint(LS331, 290) # in Kelvin
sleep_time = 20 # in minutes

date = datetime.today().strftime('%d-%m-%Y')

file_name = 'temperature_time_data' + date + '-' + str(int(290)) + 'K'
create_file(file_name, directory)

print(f'The set PID is {query_PID(LS331)}')
sleep(1)
print(f'The setpoint is {query_setpoint(LS331)} K\n')
sleep(1)
print(f'The heater range is {query_heat_range(LS331)}\n')
sleep(1)
print(f'The heater power is {query_manual_heater_power(LS331)}%\n')
sleep(1)

t_1 = time()
temp_aux = []
while time() - t_1 < sleep_time*60:
	T = read_temperature(LS331, 'A')
	temp_aux.append(T)
	t = time() - t_0
	write2file(file_name, directory, t, T)
	sleep(waiting_time(T))

T_f = np.average(temp_aux[round(len(temp_aux)*0.8):])

print(f'Starting Frequency Sweep - t = {t} s & T = {T_f} K')
frequency_sweep_module.main((n-1)*32)
'''
