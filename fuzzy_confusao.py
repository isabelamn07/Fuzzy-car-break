import numpy as np 
import skfuzzy as fuzz
#import random
import matplotlib.pyplot as plt

"""
step1 : create input and output variables
step2: create membership functions of each variable
step3: create rules set
"""


'''
Problem: Car 0 - 100 km/h
         Distance: 0 - 100m

         Define the break pressure
'''
## First version test

#Range of values
#input
speed = np.arange(0, 101, )
x_distance = np.arange(0, 101)

#output
break_pressure = np.arange(0, 101)

## Membership
## Defining values and sets:
## Distance: too_close, almost_too_close short_distance, average_distance, long distance

x_too_close = fuzz.trimf(x_distance,[0, 2, 4])
x_almost_too_close = fuzz.trimf(x_distance, [3, 6, 10])
x_short_distance = fuzz.trimf(x_distance, [10, 20, 30])
x_average_distance = fuzz.trimf(x_distance, [25, 50, 75])
x_long_distance = fuzz.trimf(x_distance,[50, 75, 100])

## Speed: too_slow, slow, avg, fast
#input
v_too_slow = fuzz.trimf(speed,[1, 15, 30])
v_slow = fuzz.trimf(speed, [25, 40, 55])
v_avg = fuzz.trimf(speed, [50, 70, 85])
v_fast = fuzz.trimf(speed, [80, 90, 100])

## break pressure: light,medium, heavy

light_break_pressure = fuzz.trimf(break_pressure, [0, 20, 35])
medium_break_pessure = fuzz.trimf(break_pressure, [30, 50, 60])
heavy_break_pressure = fuzz.trimf(break_pressure, [55, 80, 100])

#TODO
#Gaussian representation

#Some Graphics
plt.figure()

plt.plot(x_distance, x_too_close, 'r', linewidth=1.5, label='Close')
plt.plot(x_distance, x_almost_too_close, 'y', linewidth=1.5, label='Almost')
plt.plot(x_distance, x_short_distance, 'b', linewidth=1.5, label='Short')
plt.plot(x_distance, x_average_distance, 'k', linewidth=1.5, label='Avg')
plt.plot(x_distance, x_long_distance, 'm', linewidth=1.5, label='Long')
plt.title('Distance')


plt.figure()

plt.plot(speed, v_too_slow, 'r', linewidth=1.5, label='Slowest')
plt.plot(speed, v_slow, 'b', linewidth=1.5, label='Slow')
plt.plot(speed, v_avg, 'k', linewidth=1.5, label='Medium')
plt.plot(speed, v_fast, 'm', linewidth=1.5, label='Fast')
plt.title('Speed')


plt.figure()

plt.plot(break_pressure, light_break_pressure, 'b', linewidth=1.5, label='Light')
plt.plot(break_pressure, medium_break_pessure, 'k', linewidth=1.5, label='Half')
plt.plot(break_pressure, heavy_break_pressure, 'm', linewidth=1.5, label='Heavy')
plt.title('Break Pressure')

plt.show()

# Rule application - membership

#R1 = fuzz.relation_product(x_almost_too_close, v_fast)

#What the xx values are for?
#work beter on this------------------------------------------------------------------------------------
too_close_distance = fuzz.interp_membership(x_distance, x_too_close, x_distance)
almost_too_close_distance = fuzz.interp_membership(x_distance, x_almost_too_close, x_distance)
low_distance = fuzz.interp_membership(x_distance, x_short_distance, x_distance )
medium_distance = fuzz.interp_membership(x_distance, medium_break_pessure, x_distance)
high_distance = fuzz.interp_membership(x_distance, heavy_break_pressure, x_distance)

slowest_speed = fuzz.interp_membership(speed, v_too_slow, 99.9)
low_speed = fuzz.interp_membership(speed, v_slow, 99.9)
medium_speed = fuzz.interp_membership(speed, v_avg, 99.9)
high_speed =  fuzz.interp_membership(speed, v_fast, 99.9)


# set of rules
rule1 = np.fmax(high_distance, low_speed)
activate_rule1 = np.fmin(rule1, light_break_pressure)

rule2 = np.fmax(high_distance, medium_speed)
activate_rule2 = np.fmin(rule2, light_break_pressure)

rule3 = np.fmax(high_distance, high_speed)
activate_rule3 = np.fmin(rule3, light_break_pressure)

rule4 = np.fmax(high_distance, slowest_speed)
activate_rule4 = np.fmin(rule4, light_break_pressure)

# Aggregate all three output membership functions together
aggregated = np.fmax(activate_rule1, np.fmax(activate_rule2, np.fmax(activate_rule3, activate_rule4)))

# Calculate defuzzified result,
pressure = fuzz.defuzz(break_pressure, aggregated, 'centroid')
print(pressure)
#--------------------------------------------------------------------------------------------------------












