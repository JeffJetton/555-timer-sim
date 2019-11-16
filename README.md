# 555 Timer Sim

Simulations of [555 timer](https://en.wikipedia.org/wiki/555_timer_IC) circuits in Python.

### astable.py

Represents a basic circuit that uses the timer in [astable (multivibrator) mode](https://en.wikipedia.org/wiki/555_timer_IC#Astable).

1. Set the constants at the top of the file to specify values for the capacitor and resistors, as well as the length of time to simulate, etc.
2. When run, the program displays:
    * Stats about the circuit (frequency, duty cycle, and so on) in the console
    * An oscilloscope-style graph of capacitor and output voltages in a separate window

Example run:

![console output](https://github.com/JeffJetton/555-timer-sim/blob/master/img/astable_term.png)

![graph output](https://github.com/JeffJetton/555-timer-sim/blob/master/img/astable_graph.png)


### monostable.py

Represents a basic "one shot" circuit, using the timer in [monostable mode](https://en.wikipedia.org/wiki/555_timer_IC#Monostable), complete with simulated [switch contact bounce](https://en.wikipedia.org/wiki/Switch#Contact_bounce).

1. Set the constants at the top of the file to specify values for the capacitor and resistor, the length of time to simulate, and the various button/bounce parameters
2. When run, the program displays:
    * Stats about the circuit and simulation in the console
    * An oscilloscope-style graph in a separate window showing trigger input, capacitor, and output voltages
    
Example run:

![console output](https://github.com/JeffJetton/555-timer-sim/blob/master/img/monostable_term.png)

![graph output](https://github.com/JeffJetton/555-timer-sim/blob/master/img/monostable_graph.png)
