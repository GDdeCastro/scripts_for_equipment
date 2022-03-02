# output functions
from time import sleep
def switch_output(id, onoff):
    '''
    turns output on or off
    onoff = ON/OFF
    '''
    aux = onoff.strip().upper()
    if aux == 'ON' or aux == 'OFF':
        id.write(f'OUTPut {aux}')
    else:
        print('onoff variable in the wrong format.')
    return

def set_range(id, ran):
    '''
    Ran:
    auto
    1
    2
    3
    4
    5
    ...
    120 
    '''
    if type(ran) == str:
        if ran.strip().upper() == 'AUTO':
            id.write(f'CURR:RANG:AUTO ON')
    else:
        id.write(f'CURR:RANG:AUTO OFF')
        sleep(1)
        id.write(f'CURR:RANG {ran}')
    return

def set_amplitude(id, amp):
    '''
    -105e-3 A < amp < 105e-3 A
    '''
    id.write(f'SOUR:CURR {amp}')
    return

def set_voltage_compliance(id, comp):
    '''
     0.1 V < comp < 105 V
    '''
    id.write(f'SOUR:CURR:COMP {comp}')
    return

def clear(id):
    '''
    turns off the output and sets the output level to zero
    '''
    id.write(f'SOUR:CLE')
    return

def set_wave_function(id, func):
    '''
    sets the signal to AC
    func: SIN/SQU/RAMP
    '''
    reset(id)
    sleep(1)
    aux = func.strip().upper()
    id.write(f'SOUR:WAVE:FUNC {aux}')
    return

def arm_wave_mode(cs):
    '''
    this allows the equipment to generate waves
    '''
    cs.write(f'SOUR:WAVE:ARM')
    return

def trigger_wave(cs):
    '''
    this sets the output of the wave to ON
    '''
    cs.write(f'SOUR:WAVE:INIT')
    return

def abort_wave(cs):
    '''
    this stops the wave from being output
    '''
    cs.write(f'SOUR:WAVE:ABOR')
    return

def set_wave_amplitude(id, amp):
    '''
    sets the amplitude of the wave signal
    2e-12 A < amp < 105e-3 A
    '''
    id.write(f'SOUR:WAVE:AMPL {amp}')
    return

def set_wave_frequency(id, f):
    '''
    1e-3 hz < f < 1e5 hz
    '''
    id.write(f'SOUR:WAVE:FREQ {f}')
    return

def set_wave_offset(id, ofs):
    '''
    -105e-3 A < ofs < 105e-3 A
    '''
    id.write(f'SOUR:WAVE:OFFS {ofs}')
    return

def reset(id):
    id.write('*RST')
    return
