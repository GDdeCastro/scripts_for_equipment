#source functions
def set_output(id, onoff):
    '''
    0 = off
    1 = on
    '''
    id.write(f'OUTP {onoff}')
    return

def set_terminals(id, position):
    '''
    position = FRONT or REAR
    '''
    aux = position.strip().upper()
    if aux == 'FRONT' or aux =='REAR':
        id.write(f'ROUT:TERM {aux}')
    return


def set_current_amplitude(id, amp):
    '''
    amplitude is set in mA
    DC: -100 mA -> 100 mA
    AC: 0 mA -> 100 mA
    '''
    id.write(f'SOUR:CURR {amp}')
    return

def set_current_offset(id, offset):
    id.write(f'SOUR:CURR:OFFS {offset}')
    return

def set_current_limit(id, limit):
    id.write(f'SOUR:CURR:LIM {limit}')
    return

def set_current_range(id, rang):
    '''
    options: 1E-6, 10E-6, 100E-6, 1E-3, 10E-3, 100E-3
    '''
    id.write(f'SOUR:CURR:RANG {rang}')
    return

def set_current_autorange(id, onoff):
    '''
    1 - on
    0 - off
    '''
    id.write(f'SOUR:CURR:RANG:AUTO {onoff}')
    return

def set_current_DC_compliance(id, comp):
    '''
    sets the DC compliance voltage
    1V to 100V
    '''
    id.write(f'SOUR:CURR:PROT {comp}')
    return

def set_current_ac_compliance(id, comp):
    '''
    sets the AC compliance voltage
    10V to 100V
    '''
    id.write(f'SOUR:CURR:AC:VRANGE {comp}')
    return

def set_freq(id, f):
    '''
    
    '''
    id.write(f'SOUR:FREQ {f}')
    return

def set_function(id, shape):
    '''
    shape is a string that says DC or SIN
    '''
    aux = shape.strip().upper()
    if aux == 'SIN' or aux == 'DC':
        id.write(f'SOUR:FUNC {aux}')
    return

def set_mode(id, mode):
    '''
    mode = CURR or VOLT
    '''
    aux = mode.strip().upper()
    if aux == 'VOLT' or aux == 'CURR':
        id.write(f'SOUR:FUNC:MODE {aux}')
    return

def set_phase(id, phase):
    '''
    phase is given in degrees from -180 to 180
    '''
    id.write(f'SOUR:PHAS {phase}')
    return

def set_voltage_amplitude(id, amp):
    '''
    amplitude is set in V
    DC: -100 V -> 100 V
    AC: 0 V -> 100 V
    '''
    id.write(f'SOUR:VOLT {amp}')
    return

def set_voltage_offset(id, offset):
    id.write(f'SOUR:VOLT:OFFS {offset}')
    return

def set_voltage_limit(id, limit):
    id.write(f'SOUR:VOLT:LIM {limit}')
    return

def set_voltage_range(id, rang):
    '''
    options: 0.01, 0.1, 1, 10, 100
    '''
    id.write(f'SOUR:VOLT:RANG {rang}')
    return

def set_voltage_autorange(id, onoff):
    '''
    1 - on
    0 - off
    '''
    id.write(f'SOUR:VOLT:RANG:AUTO {onoff}')
    return

def set_voltage_DC_compliance(id, comp):
    '''
    sets the DC compliance voltage
    100 nA to 100 mA
    '''
    id.write(f'SOUR:VOLT:PROT {comp}')
    return

