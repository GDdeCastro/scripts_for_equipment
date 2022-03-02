#import pyvisa as visa
#rm = visa.ResourceManager()

def query_mag(id):
    '''
    Returns you the magitude of the voltage signal read by the Lock In
    '''
    return float(id.query('MAG.'))

def query_xy(id):
    '''
    Returns the X and Y values measured by the Lock In
    '''
    aux = id.query('XY.')
    aux = aux.split(',')
    x = float(aux[0])
    y = float(aux[1])
    return x,y

def query_x(id):
    '''
    Returns you the signal read by the Lock In at the X channel
    '''
    return float(id.query('X.'))

def query_y(id):
    '''
    Returns you the signal read by the Lock In at the Y channel
    '''
    return float(id.query('Y.'))

def set_vmode(id,n):
    '''
    Set the mode of the voltage that is input by the lock in to:
    "GROUND": both A and B are grounded 0
    "A": measure A against ground 1
    "-B": measure B against ground 2 
    "A-B": measure A against B 3
    0<= n <= 3
    '''

    aux = ['A', '-B', 'A-B']
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

def set_sen(id,n):
    '''
    Sets the sensitivity according to the table in page G-16 on the manual

    1 <= n < = 27
    '''
    id.write(f'SEN{n}')
    return

def set_time_constant(id,n):
    '''
    Sets the time constant according to the table on page G-19 in the manual
    0 <= n <= 29
    '''
    id.write("TC "+ str(n))
    
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

def set_reference(id,ref):
    '''
    Sets the reference mode to either "INT", "EXT LOGIC"  or "EXT"
    '''
    aux = ["INT", "EXT LOGIC", "EXT"]
    id.write("IE "+str(aux.index(str(ref).upper())))
    return

def CP(id, a):
    '''
    Sets the coupling to AC or DC

    Or reads the coupling
    '''
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

def set_float(id,n):
    '''
    Sets either "FLOAT" or "GROUND"
    '''
    aux = ["GROUND", "FLOAT"]
    i = aux.index(n.upper())
    id.write("FLOAT "+str(i))
