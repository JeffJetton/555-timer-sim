# 555 Timer Sim

Simulations of [555 timer](https://en.wikipedia.org/wiki/555_timer_IC) circuits in Python.

### astable.py

Represents a basic circuit that uses the timer in ["astable" (multivibrator) mode](https://en.wikipedia.org/wiki/555_timer_IC#Astable).

1. Set constants at the top of the file to specify values for the capacitor and resistors, as well as the length of time to simulate, etc.
2. When run, stats about the circuit such as frequency and duty cycle are printed to the console
3. An oscilloscope-style graph of capacitor and output voltages is displayed in a separate window
