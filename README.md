# 555 Timer Sim

Simulations of [555 timer](https://en.wikipedia.org/wiki/555_timer_IC) circuits in Python.

### astable.py

Represents a basic circuit that uses the timer in ["astable" (multivibrator) mode](https://en.wikipedia.org/wiki/555_timer_IC#Astable).

1. Set the constants at the top of the file to specify values for the capacitor and resistors, as well as the length of time to simulate, etc.
2. When run, the program displays:
    * Stats about the circuit (frequency, duty cycle, and so on) in the console
    * An oscilloscope-style graph of capacitor and output voltages in a separate window

Example run:

![console output](https://github.com/JeffJetton/555-timer-sim/blob/master/img/astable_term.png)

![graph output](https://github.com/JeffJetton/555-timer-sim/blob/master/img/astable_graph.png)
