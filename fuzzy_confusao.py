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

         choose between break and presure ???
'''


break_pressure = np.arange(0, 101)
velocity = np.arange(0, 101)
x_distance = np.arange(0, 101)

x_short_distance = fuzz.trimf(x_distance,[0, 10, 20])
x_average_distace = fuzz.trimf(x_distance, [15, 45, 60])
x_long_distance = fuzz.trimf(x_distance,[50, 75, 100])

v_fast = fuzz.trimf(velocity, [80, 90, 100])
v_avg = fuzz.trimf(velocity, [40, 60, 80])
v_slow = fuzz.trimf(velocity, [1, 20, 40])

plt.figure()

plt.plot(x_distance, x_short_distance, 'b', linewidth=1.5, label='Short')
plt.plot(x_distance, x_average_distace, 'k', linewidth=1.5, label='AVG')
plt.plot(x_distance, x_long_distance, 'm', linewidth=1.5, label='Long')
plt.title('Distance')

plt.show()


# Rules membership
#rule1 = np.fmax(x_long_distance, v_fast)
#activate_pressure









