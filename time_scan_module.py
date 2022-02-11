import pymeasure
import pyvisa
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from pyvisa.constants import StopBits, Parity
from time import sleep
import time
from datetime import datetime
from pymeasure.instruments.signalrecovery import DSP7265

sr = DSP7265("GPIB0::12::INSTR")
t0 = time.time()

# Calling the equipment
rm = pyvisa.ResourceManager()
print(rm.list_resources())
sr1 = rm.open_resource("GPIB0::12::INSTR")
LS331 = rm.open_resource("GPIB0::10::INSTR")
print(sr1)
print("Connected")
sr.timeout = 50000

def read_temperature(instrument, channel = 'a'):
    '''
    channel = A or B
    '''

    aux = instrument.query(f'KRDG? {channel}')
    return float(aux)
def mag(id):
    '''
    Returns you the magitude of the voltage signal read by the Lock In
    '''
    return float(id.query('MAG.'))
def xy(id):
    aux = id.query('XY.')
    aux = aux.split(',')
    x = float(aux[0])
    y = float(aux[1])
    return x,y
def x(id):
    '''
    Returns you the signal read by the Lock In at the X channel
    '''
    return float(id.query('X.'))
def y(id):
    '''
    Returns you the signal read by the Lock In at the Y channel
    '''
    return float(id.query('Y.'))
def vmode(id,n):
    '''
    Set the mode of the voltage that is input by the lock in to:
    "GROUND": both A and B are grounded
    "A": measure A against ground
    "-B": measure B against ground
    "A-B": measure A against B
    '''
    aux = ["GROUND", "A", "-B", "A-B"]
    g = aux.index(n.upper())
    id.write(f'VMODE{g}')
    return
def set_harmonic(id,n):
    '''
    Sets the harmonic in which the lock in measurements will be measured

    n = 1 : 1st harmonic
    n = 2: 2nd harmonic
    etc
    '''
    id.write(f'REFN{n}')
    return
def unlocked():
    x = sr1.query("FRQ.")
    # print(f'Frequency read: {x}')
    # print(type(x))
    # x.replace('E','e')
    # x = float(x)
    if x == '0.0E+00' or x== '\00':
        print(x)
        return True
    else:
        return False
def auto_sensitivity(id):
    '''
    Sets the instrument to automatic sensitivity adjustment mode
    '''
    id.write('AS')
    return
def set_v(id,v):
    '''
    Set the amplitude of the peak voltage
    max vpeak is ~ 7V.
    '''
    # v is in volts, but the command reads in mV
    id.write(f'OA.{v}')
    return
def set_f(id,f):
    '''
    sets the frequency to f Hz
    '''
    id.write(f'OF.{f}')
    return
def find_sen(V):

    # V = resistance*current

    sen = {2e-9:1,   5e-9:2,  10e-9:3,  20e-9:4,  50e-9:5,  100e-9:6,  200e-9:7,  500e-9:8,
   1e-6:9, 2e-6:10,  5e-6:11, 10e-6:12, 20e-6:13, 50e-6:14, 100e-6:15, 200e-6:16, 500e-6:17,
   1e-3:18, 2e-3:19, 5e-3:20, 10e-3:21, 20e-3:22, 50e-3:23, 100e-3:24, 200e-3:25, 500e-3:26,
   1:27}

    if   V < 2e-9:   return sen[50e-9]
    elif V < 5e-9:   return sen[50e-9]
    elif V < 10e-9:  return sen[50e-9]
    elif V < 20e-9:  return sen[50e-9]
    elif V < 50e-9:  return sen[50e-9]
    elif V < 100e-9: return sen[50e-9]
    elif V < 200e-9: return sen[100e-9]
    elif V < 500e-9: return sen[200e-9]

    elif V < 1e-6:   return sen[500e-9]
    elif V < 2e-6:   return sen[1e-6]
    elif V < 5e-6:   return sen[2e-6]
    elif V < 10e-6:  return sen[5e-6]
    elif V < 20e-6:  return sen[10e-6]
    elif V < 50e-6:  return sen[20e-6]
    elif V < 100e-6: return sen[50e-6]
    elif V < 200e-6: return sen[100e-6]
    elif V < 500e-6: return sen[200e-6]

    elif V < 1e-3:   return sen[500e-6]
    elif V < 2e-3:   return sen[1e-3]
    elif V < 5e-3:   return sen[2e-3]
    elif V < 10e-3:  return sen[5e-3]
    elif V < 20e-3:  return sen[10e-3]
    elif V < 50e-3:  return sen[20e-3]
    elif V < 100e-3: return sen[50e-3]
    elif V < 200e-3: return sen[100e-3]
    elif V < 500e-3: return sen[200e-3]

    elif V < 1e-6:   return sen[500e-3]

    else:                     return sen[1]
def set_sen(id,n):
    id.write(f'SEN{n}')
    return
def create_file(file_name, directory):
    file = open(directory + file_name + '.dat', "w")                                    #Abre arquivo de data
    file.write('[Header]\nTIMEMODE, SECONDS, RELATIVE\nTITLE, Python Log Data File\n')  #Header of data for MultiVu
    file.write('[Data]\n Time (s), Magnitude (V), X (V), Y (V), Frequency (Hz), Temperature (K) \n')
    os.fsync(file)
    file.flush()
def write2file(file,dir,t,m,xx,yy,f, T):
    file = open(dir + file + '.dat', "a")
    file.write(str(t)+","+str(m)+","+str(xx)+","+str(yy)+","+str(f)+ ',' +str(T) +"\n" )
    os.fsync(file)
    file.flush()
def set_time_constant(id,f):
    time_constant = 1/f
    TC = {10e-6:0, 20e-6:1, 40e-6:2, 80e-6:3, 160e-6:4, 320e-6:5, 640e-6:6,
            5e-3:7,   10e-3:8,   20e-3:9,   50e-3:10,   100e-3:11, 200e-3:12, 500e-3:13,
            1:14,   2:15,   5:16,     10:17,     20:18,     50:19,      100:20,    200:21,    500:22,
            1e3:23, 2e3:24, 5e3:25,   10e3 :26,  20e3:27,   50e3:28,    100e3:29}
    candidates = np.array([10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3,
        2e-3,   5e10-3, 10e-3, 20e-3, 50e-3,   100e-3,   200e-3,   500e-3, 1,
        2,   5,     10,     20,     50,      100,    200,    500,
        1e3, 2e3, 5e3,   10e3,  20e3,   50e3,    100e3])
    aux = np.array([time_constant]*31)
    sub = np.abs(candidates - aux)
    a = 10**9
    for j in sub.tolist():
        if j < a:
            a = j
    # a = np.min(sub)
    b = sub.tolist().index(a)
    # print(b)
    # print(TC.get(b))
    id.write("TC "+ str(b))
def is_stable(M, wndw):
    f = len(M)-1
    avg = np.mean(M[(f-wndw):f])
    # print(sqt)
    for i in range(wndw):
        if abs(round(M[f],6) - round(M[f-i],6)) != 0:
            return False
    else:
        return True
def set_phase(id,n):
    '''
    Sets the reference phase in degrees
    '''
    id.write("REFP."+str(n))
def set_gain(id,n):
    '''
    Sets the gain, you can send either "AUTO" or the desired decade, i.e., 10 dB would be 1.
    '''
    if str(n).upper() == "AUTO":
        id.write("AUTOMATIC 1")
    else:
        id.write("AUTOMATIC 0")
        id.write("ACGAIN"+str(n))
def set_reference(id,n):
    '''
    Sets the reference mode to either "INT", "EXT LOGIC" or "EXT"
    '''
    aux = ["INT", "EXT LOGIC", "EXT"]
    id.write("IE "+str(aux.index(str(n))))
def CP(id, a):
    if a == "?":
        return id.query('CP?')
    b = ["AC", "DC"]
    c = a.upper().strip()
    c = str(b.index(c))
    id.write('CP'+c)
def status(id):
    count = 0
    t0 = time.time()
    while count < 10:
        N = id.query('ST')
        aux = bin(int(N)).replace('0b','')
        sleep(1)
        if aux == str(0):
            count += 1
        else:
            if time.time() - t0 > 10*60:
                return False
            auto_sensitivity(sr1)
            sleep(5)
            count = 0
    return False

def measure(id1,ts,dir,file,measuring_time, f):
    # global gain, t
    stop = True
    aux = []
    t0 = time.time()
    t = 0
    print("Starting measurement")
    while t <= measuring_time:
        xny = (sr.x, sr.y)
        xx = xny[0]; yy = xny[1];
        m = np.sqrt(xx**2+yy**2)
        aux.append(m)
        T = read_temperature(LS331, 'A')
        t = time.time() - t0
        #print('got here- measure')
        write2file(file,dir,t,m,xx,yy,f, T)
        sleep(ts)

def temp(id,ch):
    id.write(":SENS:TEMP:CHAN" + str(ch))
    t = id.query(":FETCH?")
    return t
def thermcpl(id,type):
    id.write(":SENS:TEMP:TC:TYPE"+type)
def set_float(id,n):
    '''
    Sets either "FLOAT" or "GROUND"
    '''
    aux = ["GROUND", "FLOAT"]
    i = aux.index(n.upper())
    id.write("FLOAT "+str(i))
def tscan(dir, id1, freq, measuring_time, sleep_time,cpl):
    # defining the global file name index
    # global index
    CP(id1,cpl)
    T = read_temperature(LS331, 'A')
    #file = "s" + str('{0:03d}'.format(index))
    file = f't_scan_{round(T,1)}K'
    f = freq
    # print(str(f) + ' Hz | Coupling:' + cpl)
    ts = 1
    create_file(file,dir)
    set_time_constant(sr1, f)
    sleep(sleep_time[f])
    sr.frequency = f
    sen = {2e-9:1,   5e-9:2,  10e-9:3,  20e-9:4,  50e-9:5,  100e-9:6,  200e-9:7,  500e-9:8,
    1e-6:9, 2e-6:10,  5e-6:11, 10e-6:12, 20e-6:13, 50e-6:14, 100e-6:15, 200e-6:16, 500e-6:17,
    1e-3:18, 2e-3:19, 5e-3:20, 10e-3:21, 20e-3:22, 50e-3:23, 100e-3:24, 200e-3:25, 500e-3:26,
    1:27}
    if f <= 0.38:
        set_sen(sr1, sen[50e-6])
    elif f<= 1.51:
        set_sen(sr1, sen[20e-6])
    elif f<= 4.24:
        set_sen(sr1, sen[10e-6])
    elif f<= 5.99:
        set_sen(sr1, sen[2e-6])
    sleep(sleep_time[f])
    #print('got here - tscan')
    measure(sr1,ts,dir,file, measuring_time[f], f);

    print("Measurement finished")

# lock_in_settings(1.06, 'AC', 'A-B', 2, '6', 25e-3)

def lock_in_settings(f, cpl, AB, harmonic, gain, I, id1):
    phase = 90 # phase of reference
    ref = "INT" # defines where the reference is coming from
    ground = "float" 

    date = datetime.today().strftime('%d-%m-%Y')

    # REMEMBER TO CHANGE THESE VALUES BEFORE YOU START MEASURING!!!
    R0 = 99.8
    V =I*R0
    P = I**2*17.74e-3
    t = time.time()
    sr.set_phase = phase; set_reference(sr1,ref); vmode(sr1,AB)
    sr.harmonic = harmonic; sr.voltage = V; set_float(sr1,ground)
    set_gain(sr1,gain); CP(id1,cpl); set_time_constant(sr1, f)
    sr.frequency = f

    sleep(5)

    sen = {2e-9:1,   5e-9:2,  10e-9:3,  20e-9:4,  50e-9:5,  100e-9:6,  200e-9:7,  500e-9:8,
    1e-6:9, 2e-6:10,  5e-6:11, 10e-6:12, 20e-6:13, 50e-6:14, 100e-6:15, 200e-6:16, 500e-6:17,
    1e-3:18, 2e-3:19, 5e-3:20, 10e-3:21, 20e-3:22, 50e-3:23, 100e-3:24, 200e-3:25, 500e-3:26,
    1:27}
    
    if f <= 0.38:
        set_sen(sr1, sen[50e-6])
    elif f<= 1.51:
        set_sen(sr1, sen[20e-6])
    elif f<= 4.24:
        set_sen(sr1, sen[10e-6])
    elif f<= 5.99:
        set_sen(sr1, sen[2e-6])

    sleep(5)
    
    return

def info(dir,id,AB, phase, ref, harmonic,gain,ground,V,I,P):
    '''
    Creates an info file at the root of the data directory containing all the parameters of the lockin
    '''
    file = open(dir + 'info.dat', "w")
    file.write("Lockin configuration:\n")
    file.write("Voltage: "+str(V) +" V\n")
    file.write("Current: "+str(I) +" A\n")
    file.write("Power: "+str(P) +" W\n")

    # file.write("Coupling mode: " + cpl +"\n")
    file.write("Voltage configuration mode: " + AB + "\n")
    file.write("Phase: " + str(phase) + "º \n")
    file.write("Reference mode: " + ref + "\n")
    file.write("Harmonic: "+ str(harmonic) +"\n")
    file.write("AC gain: "+ str(gain) +"\n")
    file.write("Grounded/Floating: "+ str(ground) +"\n")
    file.write("Thermocouple: "+ "AuFe/Chromel" +"\n")

def main():
    
    # Here you set the parameters of the lockin
    # cpl = "AC" # coupling method
    AB = "A-B" # how the lockin measures
    phase = 90 # phase of reference
    ref = "INT" # defines where the reference is coming from
    harmonic = 2
    gain = "6"
    ground = "float"
    # f = 1.1;

    # Creates a folder into which the data wil be saved
    date = datetime.today().strftime('%d-%m-%Y')

    # REMEMBER TO CHANGE THESE VALUES BEFORE YOU START MEASURING!!!
    R0 = 99.8
    I = 25e-3
    V =I*R0
    P = I**2*17.74e-3
    t = time.time()
    sr.set_phase = phase; set_reference(sr1,ref); vmode(sr1,AB)
    sr.harmonic = harmonic; sr.voltage = V; set_float(sr1,ground)
    sleep(5)
    set_gain(sr1,gain);

    t_ref = read_temperature(LS331, 'A')
    dir = "D:/LQMEC-Julio-group/Python/Data/Data/Users/Guilherme/time_scans/" + date + "("+str(round(V,1))+" V)/"
    Path(dir).mkdir(parents=True,exist_ok=True)

    f = {0.0011:15000, 0.0021:7000, 0.0031:7000, 0.0048:3500, 0.0078:5000, 0.011:1600, 0.023:1600, 0.052:1300, 0.083:1300, 0.134:1300, 0.134:1300, 0.19:1300, 0.27:1300,0.38:1300, 0.53:1100, 0.76:1100, 1.06:800, 1.51:800, 2.12:800, 2.99:800,4.24:800, 5.99:400, 8.45:400, 11.9:200, 16.9:200, 23.8:200, 33.7:200, 47.54:200, 67.2:120, 94.7:120, 134.0:120, 189:120}
    f_dc = [k for k in f if k <= 0.134];
    f_ac = [k for k in f if k >= 0.134];

    # measuring_time = {0.0011:12700, 0.011:1050, 0.19:1000, 0.0021:12700, 0.023:800, 0.27:1000, 0.0031:12700, 0.38:1000, 0.0048:2500, 0.052:700, 0.53:875, 0.76:875, 0.0078:2250, 0.083:650, 0.134:1000, 1.06:800, 1.51:800, 2.12:600, 2.99:600, 4.24:600, 5.99:400, 8.45:400, 11.9:200, 16.9:200, 23.8:200, 33.7:200, 47.54:200, 67.2:120, 94.7:120, 134:120, 189:120}

    sleep_time = {0.0011:10, 0.011:10, 0.19:10, 0.0021:10, 0.023:200, 0.27:10, 0.0031:10, 0.38:10, 0.0048:10, 0.052:10, 0.53:10, 0.76:10, 0.0078:10, 0.083:10, 0.134:100, 1.06:10, 1.51:10, 2.12:10, 2.99:10, 4.24:10, 5.99:10, 8.45:10, 11.9:10, 16.9:10, 23.8:10, 33.7:10, 47.54:10, 67.2:10, 94.7:10, 134:10, 189:10}

    tscan(dir,sr1,1.06,f,sleep_time,"DC")

    sr.voltage = 0
