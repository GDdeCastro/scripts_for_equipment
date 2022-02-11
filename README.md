# scripts_for_equipment
In this repository, I will add scripts that were written to control laboratory equipment such as lock-in amplifiers (lakeshore 7265) and temperature controllers. They were used in the Laboratory for Quantum Matter under Extreme Conditions, IFUSP.

In this file, I will add a short description for each script to explain their objective. 

reset_code.py -> 

Involves SIgnal Recovery 7265 (Lock-in Amplifier), Keithley 2182 (Nanovoltmeter), and Lakeshore 331 (Temperature controller)

This is a very simple code. Its objective is to make sure "everything" is "tuned off". It means no signal is being sent nor are there any power sources being used.

frequency_sweep_module.py ->

Involves the Lock-in amplifier (SIgnal Recovery 7265) only. 

This is basically a "library" where many of the equipment commands (all I think are necessary for performing a complex measurement such as a frequency scan of the amplitude of the voltage signal in the nth harmonic) are translated into python functions. It also involves a function to perform the frequency scan. (the lock in is the power generator here)

time_scan_module.py ->

Involves SIgnal Recovery 7265 (Lock-in amplifier)

Very similar to the frequency_sweep_module.py, but it has a different scanning mode (time, not frequency) dependence. (the lock in is the power generator here)

structure_for_temperature_dependent_frequency_sweeps.py ->

Involves SIgnal Recovery 7265, and Lakeshore 331

This code is a temperature controller that performs a frequency scan at 21 different temperatures. It was used in the measurement of the heat capacity of a Strontium Titanite Sample in LQMEC, IFUSP.

v_ac_fixed_freq.py -> 

Involves SIgnal Recovery 7265 (Lock-in Amplifier), and Lakeshore 331 (Temperature controller)

This script performs a temperature ramp of the measured voltage signal by the lock-in at one fixed frequency. (the lock in is the power generator here)

DC_heat_error_measurement.py -> 

Involves SIgnal Recovery 7265 (Lock-in Amplifier), Keithley 2182 (Nanovoltmeter), and Lakeshore 331 (Temperature controller)

This script performs the measurement of the residual signal in the 1st harmonic caused by the lock in (when turned on and off) to the signal in our experiments. It basically performs a ramp that measures voltage with the NANOVOLTMETER due to the power supplied by the Lock-In amplifier attached to a resistor. 

monitor_temperature.py -> 

Involves Lakeshore 331

Performs a continuous time scan of the temperature for a determined time.
