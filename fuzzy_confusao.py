import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz

## Final version

"""
Problem: Car 0 - 100 km/h
         Distance: 0 - 100m
         Define the break pressure
"""

# functions used on the rules set
def average(val1, val2):
    return (val1 + val2) / 2

def getIntermediate(val1, val2):
    return val2 if (val1 > 0.75) else val1

# Main program
def fuzzy_result(def_speed, def_distance):
    # input
    speed_axis = np.arange(0, 101)
    distance_axis = np.arange(0, 101)

    # output
    break_pressure = np.arange(0, 101)

    # # Membership
    # # Defining values and sets:
    # # Distance: too_close, short_distance, medium_distance, long distance

    x_close_distance = fuzz.gaussmf(distance_axis, 0, 10)
    x_short_distance = fuzz.gaussmf(distance_axis, 27, 6)
    x_medium_distance = fuzz.gaussmf(distance_axis, 50, 7.1)
    x_long_distance = fuzz.gaussmf(distance_axis, 100, 30)

    # # Speed: too_slow, slow, avg, fast
    # input
    v_slowest = fuzz.gaussmf(speed_axis, 0, 16)
    v_slow = fuzz.gaussmf(speed_axis, 25, 8)
    v_avg = fuzz.gaussmf(speed_axis, 50, 16)
    v_fast = fuzz.gaussmf(speed_axis, 100, 10)

    # # break pressure: light,medium, heavy

    light_break_pressure = fuzz.gaussmf(break_pressure, 0, 20)
    medium_break_pressure = fuzz.gaussmf(break_pressure, 50, 10)
    heavy_break_pressure = fuzz.gaussmf(break_pressure, 100, 20)

    # Some Graphics
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    ax0.plot(distance_axis, x_close_distance, 'r', linewidth=1.5, label='Close')
    ax0.plot(distance_axis, x_short_distance, 'b', linewidth=1.5, label='Short')
    ax0.plot(distance_axis, x_medium_distance, 'k', linewidth=1.5, label='Avg')
    ax0.plot(distance_axis, x_long_distance, 'm', linewidth=1.5, label='Long')
    ax0.set_title('Distance')
    ax0.legend(('Close', 'Short', 'Medium', 'Long'),
        loc='center right')

    ax1.plot(speed_axis, v_slowest, 'r', linewidth=1.5, label='Slowest')
    ax1.plot(speed_axis, v_slow, 'b', linewidth=1.5, label='Slow')
    ax1.plot(speed_axis, v_avg, 'k', linewidth=1.5, label='Medium')
    ax1.plot(speed_axis, v_fast, 'm', linewidth=1.5, label='Fast')
    ax1.set_title('Speed')
    ax1.legend(('Very Slow', 'Slow', 'Medium', 'Fast'),
        loc='center right')

    ax2.plot(break_pressure, light_break_pressure, 'b', linewidth=1.5, label='Light')
    ax2.plot(break_pressure, medium_break_pressure, 'k', linewidth=1.5, label='Half')
    ax2.plot(break_pressure, heavy_break_pressure, 'm', linewidth=1.5, label='Heavy')
    ax2.set_title('Break Pressure')
    ax2.legend(('Light', 'Medium', 'Heavy'),
        loc='center right')

    # Turn off top/right axes
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    # Membership
    member_close_dist = fuzz.interp_membership(distance_axis, x_close_distance, def_distance)
    member_short_dist = fuzz.interp_membership(distance_axis, x_short_distance, def_distance)
    member_medium_dist = fuzz.interp_membership(distance_axis, x_medium_distance, def_distance)
    member_high_dist = fuzz.interp_membership(distance_axis, x_long_distance, def_distance)
    
    member_slowest_speed = fuzz.interp_membership(speed_axis, v_slowest, def_speed)
    member_low_speed = fuzz.interp_membership(speed_axis, v_slow, def_speed)
    member_medium_speed = fuzz.interp_membership(speed_axis, v_avg, def_speed)
    member_high_speed = fuzz.interp_membership(speed_axis, v_fast, def_speed)

    ######################## Set of rules ######################## 
    """
    Rules: 
    Distance  /  Speed    /  Pressure 
R1  High         Slowest     low pressure 
R2  Medium       Slowest     low pressure
R3  Short        Slowest     medium pressure
R4  Close        Slowest     medium pressure

R5  High         Low        low pressure      
R6  Medium       Low         low pressure
R7  Short        Low         medium pressure
R8  Close        Low         heavy pressure 

R9 High          Medium      low pressure   
R10 Medium       Medium      medium pressure
R11 Short        Medium      medium pressure
R12 Close        Medium      heavy pressure 

R13 High         Fast        medium pressure   
R14 Medium       Fast        medium pressure
R15 Short        Fast        heavy pressure
R16 Close        Fast        heavy pressure

"""
    ###### First subset - Low Pressure
    rule_low_1 = np.fmax(member_high_dist, member_slowest_speed)
    rule_low_2 = np.fmin(member_medium_dist, member_slowest_speed)
    if (member_slowest_speed > 0.75) :
        rule_low_2 = np.fmin(member_medium_dist, member_slowest_speed)
    rule_low_3 = np.fmin(member_high_dist, member_low_speed)
    if (member_high_dist > 0.75) :
        rule_low_3 = np.fmax(member_high_dist, member_low_speed)
    rule_low_4 = member_low_speed
    rule_low_5 = np.fmin(member_high_dist, member_medium_speed)
    if (member_high_dist > 0.75) :
        rule_low_5 = np.fmax(member_high_dist, member_medium_speed)

    activate_rule_low = np.fmax(rule_low_1, np.fmax(rule_low_2, 
    np.fmax(rule_low_3, np.fmax(rule_low_4, rule_low_5))))

    #print("rule_low_1: ", rule_low_1)
    #print("rule_low_2: ", rule_low_2)
    #print("rule_low_3: ", rule_low_3)
    #print("rule_low_4: ", rule_low_4)
    #print("rule_low_5: ", rule_low_5)
    #print("LOW RULE: ", activate_rule_low)

    ###### Second subset - Medium Pressure
    rule_medium_1 = member_short_dist
    rule_medium_2 = np.fmin(member_close_dist, member_slowest_speed)
    if (member_short_dist > 0.75 and member_slowest_speed > 0.75) :
        rule_medium_2 = np.fmax(member_close_dist, member_slowest_speed)
    rule_medium_3 = average(member_short_dist, member_low_speed)
    rule_medium_4 = np.fmin(member_medium_dist, member_medium_speed)
    if (member_medium_dist > 0.75 and member_medium_dist > 0.75) :
        rule_medium_4 = np.fmax(member_medium_dist, member_medium_speed)
    rule_medium_5 = np.fmin(member_short_dist, member_medium_speed)
    if (member_short_dist> 0.75 and member_medium_speed > 0.75) :
        rule_medium_5 = np.fmax(member_short_dist, member_medium_speed)
    rule_medium_6 = np.fmin(member_high_dist, member_high_speed)
    if (member_high_dist > 0.75 and member_high_speed > 0.75) :
        rule_medium_6 = np.fmax(member_high_dist, member_high_speed)
    rule_medium_7 = np.fmin(member_medium_dist, member_high_speed)
    if (member_medium_dist > 0.75 and member_high_speed > 0.75) :
        rule_medium_7 = np.fmax(member_medium_dist, member_high_speed)

    activate_rule_medium = np.fmax(rule_medium_1, np.fmax(rule_medium_2, np.fmax(rule_medium_3, 
    np.fmax(rule_medium_4, np.fmax(rule_medium_5, np.fmax(rule_medium_6, rule_medium_7))))))

    #print("rule_medium_1: ", rule_medium_1)
    #print("rule_medium_2: ", rule_medium_2)
    #print("rule_medium_3: ", rule_medium_3)
    #print("rule_medium_4: ", rule_medium_4)
    #print("rule_medium_5: ", rule_medium_5)
    #print("rule_medium_6: ", rule_medium_6)
    #print("rule_medium_7: ", rule_medium_7)
    #print("MEDIUM RULE: ", activate_rule_medium)

    ###### Third subset - High Pressure
    rule_high_1 = getIntermediate(member_close_dist, member_low_speed)
    rule_high_2 = getIntermediate(member_close_dist, member_medium_speed)
    rule_high_3 = 0
    if (member_short_dist > 0.75) :
        rule_high_3 = np.fmax(member_short_dist, member_high_speed)
    rule_high_4 = np.fmax(member_close_dist, member_high_speed)

    activate_rule_high = np.fmax(rule_high_1, np.fmax(rule_high_2, np.fmax(rule_high_3, rule_high_4)))

    #print("rule_high_1: ", rule_high_1)
    #print("rule_high_2: ", rule_high_2)
    #print("rule_high_3: ", rule_high_3)
    #print("rule_high_4: ", rule_high_4)
    #print("HIGH RULE: ", activate_rule_high)

    ###### Rule activations
    brake_activation_low = np.fmin(activate_rule_low, light_break_pressure)
    brake_activation_medium = np.fmin(activate_rule_medium,  medium_break_pressure)
    brake_activation_high = np.fmin(activate_rule_high,  heavy_break_pressure)

    aggregated = np.fmax(brake_activation_low, np.fmax(brake_activation_medium, brake_activation_high))

    # Calculate defuzzified result
    pressure = fuzz.defuzz(break_pressure, aggregated, 'centroid')
    if (pressure < 17 or pressure > 83):
        pressure = fuzz.defuzz(break_pressure, aggregated, 'mom')
    pressure_value = fuzz.interp_membership(break_pressure, aggregated, pressure)

    print("Break pressure: ", pressure)

    # Activation area graph
    break0 = np.zeros_like(break_pressure)
    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.plot(break_pressure, brake_activation_low, 'b', linewidth=0.5, linestyle='--', )
    ax0.plot(break_pressure, brake_activation_medium, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(break_pressure, brake_activation_high, 'r', linewidth=0.5, linestyle='--')
    ax0.fill_between(break_pressure, break0, aggregated, facecolor='Orange', alpha=0.7)
    ax0.plot([pressure, pressure], [0, pressure_value], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Aggregated membership and result (line)')

    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    plt.show()

   
speed = float(input("Speed: "))
distance = float(input("Distance: "))
fuzzy_result(speed, distance)
