To install the instrument control software for python in your computer, follow the steps:

1 - copy all .py files in the folder "modules"
2 - paste them into your python installation folder (usually named Python3#, where # stands for a number)

To use the software:

1 - in the beginning of any script that controls the equipment, write:
	import lab_equipment as instruments, signal_recovery_7265 as SR7265,\
       		lakeshore_155 as L155, lakeshore_331 as L331, lakeshore_372 as L372,\
       		keithley_2182a as K2182a, keithley_6221 as K6221
2 - Select the instruments you will need using the calling functions, e.g.:
	
	instr1 = instruments.call_gpib_instrument(12)
	instr2 = instruments.call_general_instrument('USB0::0x0A2D::0x001B::21084591::RAW') 

3 - when sending a command, remember to type first the library name for the equipment used. The library name is always
    given by the initial letter of the name of the instrument brand (K as in Keithley or SR as in Signal Recovery) followed
    by the instrument number (7265 as in Signal Recovery 7265), e.g.:
	SR7265.set_v(sr, 0)

4 - if you need the instrument to do something that the equipment library does not do yet, you can use the raw command strcture:
	instr1.write('command') # for setting
	instr1.query('command') # for asking
	instr1.read('command') # for reading