import numpy as np 
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# # Second version test
"""
Problem: Car 0 - 100 km/h
         Distance: 0 - 100m
         Define the break pressure
"""

def fuzzy_result(def_speed, def_distance):
    # Range of values
    # input
    speed = np.arange(0, 101)
    x_distance = np.arange(0, 101)

    # output
    break_pressure = np.arange(0, 101)

    # # Membership
    # # Defining values and sets:
    # # Distance: too_close, almost_too_close short_distance, medium_distance, long distance

    x_too_close = fuzz.gaussmf(x_distance, 0, 4)
    x_almost_too_close = fuzz.gaussmf(x_distance, 10, 3)
    x_short_distance = fuzz.gaussmf(x_distance, 27, 6)
    x_medium_distance = fuzz.gaussmf(x_distance, 50, 7.1)
    x_long_distance = fuzz.gaussmf(x_distance, 100, 30)

    # # Speed: too_slow, slow, avg, fast
    # input
    v_too_slow = fuzz.gaussmf(x_distance, 0, 16)
    v_slow = fuzz.gaussmf(x_distance, 40, 6)
    v_avg = fuzz.gaussmf(x_distance, 70, 7)
    v_fast = fuzz.gaussmf(x_distance, 100, 16)

    # # break pressure: light,medium, heavy

    light_break_pressure = fuzz.trimf(break_pressure, [0, 20, 35])
    medium_break_pessure = fuzz.trimf(break_pressure, [30, 50, 60])
    heavy_break_pressure = fuzz.trimf(break_pressure, [55, 80, 100])

    # Some Graphics
    plt.figure()

    plt.plot(x_distance, x_too_close, 'r', linewidth=1.5, label='Close')
    plt.plot(x_distance, x_almost_too_close, 'y', linewidth=1.5, label='Almost')
    plt.plot(x_distance, x_short_distance, 'b', linewidth=1.5, label='Short')
    plt.plot(x_distance, x_medium_distance, 'k', linewidth=1.5, label='Avg')
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
    too_close_distance = fuzz.interp_membership(x_distance, x_too_close, def_distance)
    almost_too_close_distance = fuzz.interp_membership(x_distance, x_almost_too_close, def_distance)
    low_distance = fuzz.interp_membership(x_distance, x_short_distance, def_distance)
    medium_distance = fuzz.interp_membership(x_distance, medium_break_pessure, def_distance)
    high_distance = fuzz.interp_membership(x_distance, heavy_break_pressure, def_distance)

    slowest_speed = fuzz.interp_membership(speed, v_too_slow, def_speed)
    low_speed = fuzz.interp_membership(speed, v_slow, def_speed)
    medium_speed = fuzz.interp_membership(speed, v_avg, def_speed)
    high_speed = fuzz.interp_membership(speed, v_fast, def_speed)

    ######################## Set of rules ######################## 
    """
    Rules: 
    Distance  /  Speed    /  Pressure 
R1  Big          Slowest      lowest pressure - 0
R2  Medium       Slowest     low pressure
R3  Short        Slowest     low pressure
R4  Close        Slowest     medium pressure
R5  Too close    Slowest     medium pressure

R6  Big          Low         low pressure      
R7  Medium       Low         low pressure
R8  Short        Low         low pressure
R9  Close        Low         medium pressure 
R10 Too close    Low         medium pressure

R11 Big          Medium         low pressure   
R12 Medium       Medium         low pressure
R13 Short        Medium         medium pressure
R14 Close        Medium         heavy pressure 
R15 Too close    Medium         heaviest pressure

R16 Big          Fast         low pressure   
R17 Medium       Fast         low pressure
R18 Short        Fast         medium pressure
R19 Close        Fast         heavy pressure
R20 Too close    Fast         heavy pressure
"""

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

