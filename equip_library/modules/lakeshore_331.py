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
    # print(f'SETP {loop},{temperature}')

    instrument.write(f'SETP {loop},{temperature}')
    return

def set_ramp(instrument, rate, onoff = 1, loop = 1):
   
    # print(f'RAMP {loop},{onoff},{rate}')
    instrument.write(f'RAMP {loop},{onoff},{rate}')
    return

def query_ramp(instrument):
   
    # print(f'RAMP {loop},{onoff},{rate}')
    instrument.write(f'RAMP?')
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

def query_temperature(instrument, channel = 'a'):
    '''
    channel = A or B
    '''
    aux = instrument.query(f'KRDG? {channel}')
    return float(aux)

def query_resistance(instrument, channel = 'a'):
    aux = instrument.query(f'SRDG? {channel}')
    return float(aux)
