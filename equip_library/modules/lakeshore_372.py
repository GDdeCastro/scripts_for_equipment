#resistance bridge 372 functions
def query_resistance(id, ch):
    '''
    id - instrument id
    ch - channel 1-16
    '''
    return float(id.query(f'RDGR? {ch}'))

def query_temp(id, ch):
    '''
    id - instrument id
    ch - channel 1-16
    '''
    return float(id.query(f'RDGK? {ch}'))

def query_intype(id, ch):
    '''
    the output of this function is a list.
    <mode>,<excitation>,<autorange>,<range>,<cs shunt>,<units>
    '''
    return id.query(f'INTYPE? {ch}').split(',')

def set_intype(id, ch, intype):
    '''
    intype is a list with the parameters' values:
    [<mode>,<excitation>,<autorange>,<range>,<cs shunt>,<units>]
    '''
    aux = ','.join(str(item) for item in intype)
    id.write(f'INTYPE {ch},{aux}')
    return

def query_range(id, ch):
    '''
    the range will be returned.
    ch => 1-16
    '''
    return int(id.query(f'INTYPE? {ch}').split(',')[3])

def query_excitation(id, ch):
    '''
    the excitation index will be returned.
    ch => 1-16
    '''
    return int(id.query(f'INTYPE? {ch}').split(',')[1])

def set_mode(id, ch, mode):
    intype = query_intype(id, ch)
    intype[0] = mode
    set_intype(id, ch, intype)
    return

def set_range(id, ch, new_range):
    '''
    if you set new_range = 0 -> autorange will be activated

    ranges: 1->22
    '''
    intype = query_intype(id, ch)
    if new_range != 0:
        intype[3] = new_range
        set_intype(id, ch, intype)
    else:
        intype[2] = new_range
        set_intype(id, ch, intype)
    return

def set_excitation(id, ch, new_excitation):
    '''
    excitation:
        voltage: 1->12
        current: 1->22
    '''
    intype = get_intype(id, ch)
    intype[1] = new_excitation
    set_intype(id, ch, intype)
    return

def set_cshunt(id,ch,shunt):
    '''
    shunt = 0 -> current shunt off 
    shunt = 0 -> current shunt on (no excitation)
    '''
    intype = get_intype(id, ch)
    intype[5] = shunt
    set_intype(id, ch, intype)
    return

def set_units(id,ch,unit):
    '''
    unit = 1 -> kelvin
    unit = 2 -> ohms
    '''
    intype = get_intype(id, ch)
    intype[6] = unit
    set_intype(id, ch, intype)
    return

def scan_channel(ch, scan_time, autoscan):
    '''
    ch - channel
    autoscan = 0/1 (off/on)
    '''
    id.write(f'SCAN {ch},{autoscan}')
    sleep(scan_time)
    return
