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
         distance: 0 - 100m

         define the break pressure
'''

#Range of values
break_pressure = np.arange(0, 101)
speed = np.arange(0, 101)
x_distance = np.arange(0, 101)

#input
x_short_distance = fuzz.trimf(x_distance,[0, 2, 4])
x_average_distace = fuzz.trimf(x_distance, [3, 30, 60])
x_long_distance = fuzz.trimf(x_distance,[50, 75, 100])

#input
v_fast = fuzz.trimf(speed, [75, 90, 100])
v_avg = fuzz.trimf(speed, [40, 60, 85])
v_slow = fuzz.trimf(speed, [1, 25, 50])

#output
light_break_pressure = fuzz.trimf(break_pressure, [0, 15, 30])
medium_break_pessure = fuzz.trimf(break_pressure, [20, 40, 55])
heavy_break_pressure = fuzz.trimf(break_pressure, [50, 75, 100])

#TODO
#Gaussian representation

#Some Graphics
plt.figure()

plt.plot(x_distance, x_short_distance, 'b', linewidth=1.5, label='Short')
plt.plot(x_distance, x_average_distace, 'k', linewidth=1.5, label='Avg')
plt.plot(x_distance, x_long_distance, 'm', linewidth=1.5, label='Long')
plt.title('Distance')


plt.figure()

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

#What the xx values are for?
low_distance = fuzz.interp_membership(x_distance, x_short_distance, 6.5 )
medium_distance = fuzz.interp_membership(x_distance, medium_break_pessure, 6.5)
high_distance = fuzz.interp_membership(x_distance, heavy_break_pressure, 6.5)

low_speed = fuzz.interp_membership(speed, v_slow, 8.8)
medium_speed = fuzz.interp_membership(speed, v_avg, 8.8)
high_speed =  fuzz.interp_membership(speed, v_fast, 8.8)


# Rules
rule1 = np.fmax(high_distance, low_speed)
activate_rule1 = np.fmin(rule1, light_break_pressure)

rule2 = 

rule3 =








