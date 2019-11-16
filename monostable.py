####  Libraries  ###############################################################

import math     # Just to get Euler's constant
import matplotlib.pyplot as pplot
import random   # For bouncing



####  Constants  ###############################################################

vin = 5.0           # Voltage in

out_high = 3.3      # Voltage output from pin 3 when "high" 
out_low  = 0.25     # Voltage output from pin 3 when "low"
                    # (These are not simply vin and zero. See datasheet.)

farads = 2/1000000  # Capacitance of primary capacitor, which connects both the
                    # threshold (pin 6) and discharge (pin 7) to ground. It is
                    # fed voltage through one end of the primary resistor.
                    
ohms = 1000000      # Resistance in ohms of the primary resistor. This connects
                    # the input voltage to pins 6 & 7 as well as the capacitor.

sim_time = 3        # Length of time to run the entire simulation (in seconds)

step = sim_time / 1000      # Time increment for each simulation step (seconds)

button_start_time = 0.5     # At what point do we fire off the timer (seconds)

button_hold_time = 0.5      # How long do we press the button? (seconds)

bounce_time = 0.07  # How long to simulate switch bounce after button press
                    # (Set to zero to turn off bounce simulation)
                    
bounce_prob = 0.33  # Chance that switch will bounce open during each step

unbounce_prob = 0.5 # Chance that a bounced switch will re-close during a step

# Note that the bounce/unbounce probabilities will need to be adjusted if
# the step time changes

# Bounce time should not exceed button hold time
if bounce_time > button_hold_time:
    bounce_time = button_hold_time
    


####  Utility functions   ######################################################

def update_latch(latch, trigger, threshold, vin):
    """
    Return a boolean representing the state of the internal SR latch, based on
    trigger and threshold voltages, as they compare to the input voltage.
    """
    # Latch is "set" if the trigger voltage is less than 1/3 vin
    # (But not necessarily "unset" if it's not!)
    if trigger < vin / 3:
        latch = True
    
    # Latch is "unset" if the threshold voltage is above 2/3 vin
    # (But not necessarily "set" if it's not!)
    if threshold > vin * 2 / 3:
        latch = False
        
    # For voltages between these, the latch stays at whatever it was
    return latch
    


def update_capacitor(cap, farads, ohms, vin, latch, step):
    """
    Either charges or discharges (depending on latch state) the capacitor 
    based on resistor (ohms) and vin, over time period 'step'. The percentage
    of change, either way, is based on (1 - 1/e**(t/tc)). That is:
    
        1. Calculate the time constant (capacitance times total resistance)
        2. Figure out the proportion of the time constant that has passed
        3. Raise e to that proportion
        4. Take the inverse of that result
        5. Subtract that from one
    
    Returns the resulting capacitor voltage
    """
    if latch:
        # Charging...
        # Time constant
        tc = farads * ohms
        # Time proportion
        tp = step / tc
        # Percent change from existing voltage to full voltage (vin)
        pc = 1 - (1/math.e**tp)
        cap += (vin - cap) * pc
    else:
        # Discharging...
        # Resistor is bypassed, so discharge is essentially immediate
        cap = 0
        # That was easy!

    return cap



####  Set up  ##################################################################

# At the start of the simulation, the Trigger input voltage is pulled high.
#
# Monostable mode is sort of "backwards" in that an unfired circuit is
# actually feeding voltage to the "trigger" input on pin 2. To fire the
# one-shot, that voltage is pulled low and the trigger input is off.
# The fact that you turn OFF the "trigger" to trigger the ouput is not
# particularly intuitive.
#
# Since the voltage into pin 2 is above 1/3 vin, the latch starts out unset and
# the output of the 555 will be low.
trigger = vin
latch = False
vout = out_low

# Assume the capacitor starts out uncharged. Since the latch is not set, the
# discharge pin (pin 7) is draining to ground, discharging anything that might
# have been in the capacitor anyway (and keeping the capacitor from recharging
# through the primary resistor).
cap = 0

# The "*_list" vectors store simulated states at each time slice
# Everything is constant/stable before the trigger happens, so we can just fill
# in those steps and jump right to the trigger time:
pre_trigger_steps = round(button_start_time / step)
trigger_list = [trigger] * pre_trigger_steps
cap_list = [cap] * pre_trigger_steps
out_list = [vout] * pre_trigger_steps
time_list = [i * step for i in range(pre_trigger_steps)]
time = button_start_time


####  Simulate  ################################################################

# Seed for bounce randomness
random.seed(8675309)

# Press the button! :-)
trigger = 0
button_time = 0

while time < sim_time:
    latch = update_latch(latch, trigger, cap, vin)
    cap = update_capacitor(cap, farads, ohms, vin, latch, step)
    if latch:
        vout = out_high
    else:
        vout = out_low
    trigger_list.append(trigger)
    cap_list.append(cap)
    out_list.append(vout)
    time_list.append(time)
    time += step
    button_time += step
    # Should we check for bounce?
    if button_time <= bounce_time:
        r = random.randint(0, 100) / 100
        # If trigger is low (button pressed) will it bounce open?
        if trigger == 0 and r < bounce_prob:
            trigger = vin
        # If trigger is high (button has bounced open), will it re-close?
        elif trigger != 0 and r < unbounce_prob:
            trigger = 0
    else:
        # If we're not bouncing, button is either pressed or unpressed
        if button_time > button_hold_time:
            trigger = vin
        else:
            trigger = 0
    

####  Print Stats  #############################################################

# Print constants
print()
print('Capacitor: ' + str(farads * 1000000) + 'mf')
print('Resistor: ' + str(ohms/1000) + 'K')
print('Vcc: +' + str(vin) + 'V')
print()

# Print out timing info (formula from the datasheet)
time_high = round(1.1 * ohms * farads, 2)
print('Time high: ' + str(time_high*1000) + 'ms')
print('Periods simulated: ' + str(len(time_list)))
print('Bounce time: ' + str(bounce_time*1000) + 'ms')
print()


####  Plot  ####################################################################

# Trigger (pin 7) voltages
pplot.plot(time_list, trigger_list, linewidth=0.7, label='Trigger (Pin 2)')
# Output (Q) voltages
pplot.plot(time_list, out_list, label='Output (Pin 3)')
# Capacitor voltages
pplot.plot(time_list, cap_list, label='Capacitor')
pplot.xlabel('Time (Seconds)')
pplot.ylabel('Volts')
pplot.ylim(0-vin*0.1, vin*1.1)
pplot.legend(loc='upper right')

pplot.show()



