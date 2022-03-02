def set_mode(nv, mode):
    '''
    selects the measuring mode:
    Temperature: TEMP
    Voltage: VOLT
    the mode variable is a string
    '''
    aux = mode.strip().upper()
    if aux == 'TEMP' or aux == 'VOLT':
        nv.write('SENS:FUNC \'{aux}\'')
    return

def set_range(nv, ran, ch):
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
            nv.write(f':SENS:VOLT:CHAN{ch}:RANG:AUTO 1')
    else:
        nv.write(f':SENS:VOLT:CHAN{ch}:RANG:AUTO 0')
        sleep(1)
        nv.write(f':SENS:VOLT:CHAN{ch}:RANG {ran}')
    return 

def query_voltage(nv, ch):
    '''
    performs the measurement of voltage
    ch is the channel
    '''
    # nv.write(f'SENS:DATA:FRES?')
    # which one is better? comment one of them and test
    t = nv.query(":READ?")
    return float(t)

def reset(nv):
    '''
    
    '''
    nv.write('*RST')
    nv.write('INIT:CONT OFF; :ABORT')

def set_gain(nv, m):
    '''
    goes from -100e6 to 100e6
    '''
    nv.write(f'OUTP:GAIN {m}')
