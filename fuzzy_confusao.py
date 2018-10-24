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
    # input
    speed_axis = np.arange(0, 101)
    distance_axis = np.arange(0, 101)

    # output
    break_pressure = np.arange(0, 101)

    # # Membership
    # # Defining values and sets:
    # # Distance: too_close, almost_too_close short_distance, medium_distance, long distance

    x_too_close = fuzz.gaussmf(distance_axis, 0, 10)
    x_short_distance = fuzz.gaussmf(distance_axis, 27, 6)
    x_medium_distance = fuzz.gaussmf(distance_axis, 50, 7.1)
    x_long_distance = fuzz.gaussmf(distance_axis, 100, 30)

    # # Speed: too_slow, slow, avg, fast
    # input
    v_too_slow = fuzz.gaussmf(speed_axis, 0, 16)
    v_slow = fuzz.gaussmf(speed_axis, 40, 6)
    v_avg = fuzz.gaussmf(speed_axis, 70, 7)
    v_fast = fuzz.gaussmf(speed_axis, 100, 16)

    # # break pressure: light,medium, heavy

    light_break_pressure = fuzz.gaussmf(speed_axis, 0, 20)
    medium_break_pessure = fuzz.gaussmf(speed_axis, 50, 10)
    heavy_break_pressure = fuzz.gaussmf(speed_axis, 100, 20)

    # Some Graphics
    plt.figure()

    plt.plot(distance_axis, x_too_close, 'r', linewidth=1.5, label='Close')
    plt.plot(distance_axis, x_short_distance, 'b', linewidth=1.5, label='Short')
    plt.plot(distance_axis, x_medium_distance, 'k', linewidth=1.5, label='Avg')
    plt.plot(distance_axis, x_long_distance, 'm', linewidth=1.5, label='Long')
    plt.title('Distance')

    plt.figure()

    plt.plot(speed_axis, v_too_slow, 'r', linewidth=1.5, label='Slowest')
    plt.plot(speed_axis, v_slow, 'b', linewidth=1.5, label='Slow')
    plt.plot(speed_axis, v_avg, 'k', linewidth=1.5, label='Medium')
    plt.plot(speed_axis, v_fast, 'm', linewidth=1.5, label='Fast')
    plt.title('Speed')

    plt.figure()

    plt.plot(break_pressure, light_break_pressure, 'b', linewidth=1.5, label='Light')
    plt.plot(break_pressure, medium_break_pessure, 'k', linewidth=1.5, label='Half')
    plt.plot(break_pressure, heavy_break_pressure, 'm', linewidth=1.5, label='Heavy')
    plt.title('Break Pressure')

    plt.show()

    # Membership
    member_close_dist = fuzz.interp_membership(distance_axis, x_too_close, def_distance)
    member_short_dist = fuzz.interp_membership(distance_axis, x_short_distance, def_distance)
    member_medium_dist = fuzz.interp_membership(distance_axis, x_medium_distance, def_distance)
    member_high_dist = fuzz.interp_membership(distance_axis, x_long_distance, def_distance)
    
    member_slowest_speed = fuzz.interp_membership(speed_axis, v_too_slow, def_speed)
    member_low_speed = fuzz.interp_membership(speed_axis, v_slow, def_speed)
    member_medium_speed = fuzz.interp_membership(speed_axis, v_avg, def_speed)
    member_high_speed = fuzz.interp_membership(speed_axis, v_fast, def_speed)

    ######################## Set of rules ######################## 
    """
    Rules: 
    Distance  /  Speed    /  Pressure 
R1  High          Slowest     low pressure 
R2  Medium       Slowest     low pressure
R3  Short        Slowest     low pressure
R4  Close        Slowest     medium pressure

R5  High          Low         low pressure      
R6  Medium       Low         low pressure
R7  Short        Low         medium pressure
R8  Close        Low         heavy pressure 

R9 High           Medium      low pressure   
R10 Medium       Medium      medium pressure
R11 Short        Medium      medium pressure
R12 Close        Medium      heavy pressure 

R13 High         Fast        medium pressure   
R14 Medium       Fast        medium pressure
R15 Short        Fast        heavy pressure
R16 Close        Fast        heavy pressure

"""

    rule1 = np.fmax(member_high_dist, member_low_speed)
    print(rule1)
    activate_rule1 = np.fmin(rule1, light_break_pressure)

    rule2 = np.fmax(member_high_dist, member_medium_speed)
    activate_rule2 = np.fmin(rule2, light_break_pressure)

    rule3 = np.fmax(member_high_dist, member_high_speed)
    activate_rule3 = np.fmin(rule3, light_break_pressure)

    rule4 = np.fmax(member_high_dist, member_slowest_speed)
    activate_rule4 = np.fmin(rule4, light_break_pressure)

    

    # Aggregate all three output membership functions together
    aggregated = np.fmax(activate_rule1, np.fmax(activate_rule2, np.fmax(activate_rule3, activate_rule4)))

    # Calculate defuzzified result,
    pressure = fuzz.defuzz(break_pressure, aggregated, 'centroid')
    print(pressure)

fuzzy_result(9.9, 26.1)

