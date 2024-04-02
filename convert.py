import numpy as np
import csv
import random
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from scipy.interpolate import CubicSpline
def convert_day_in_energy(day):
    x_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    y_values = np.array([0, 0, 0, 0.29, 0.29, 0.54, 0.67, 0.91, 1.34, 1.58, 2.42, 2.72, 4.63, 5.73, 7.11, 8.44, 8.86, 10.28])

    # Normalize data
    x_values_norm = x_values / x_values.max()
    y_values_norm = y_values / y_values.max()

    cs = CubicSpline(x_values_norm, y_values_norm)

    x_new = day / 18  # Normalize input
    y_new = cs(x_new) * 10.28  # Denormalize output

    return y_new

def convert_hours_in_minutes(hours ,minutes):
    return (hours * 60)+minutes

def normalize_input(minutes, x_values_max=1440):
    return minutes / x_values_max

def denormalize_output(y_new, y_values_max=1):
    return y_new * y_values_max

def normalize_minutes(minutes):
    x_values = np.array([0, 60, 120, 180 ,240 ,720, 1440])
    y_values = np.array([0, 0.1, 0.2 ,0.3, 0.4 , 0.5, 1])

    x_values_norm = x_values / x_values.max()
    y_values_norm = y_values / y_values.max()

    cs = CubicSpline(x_values_norm, y_values_norm)

    x_new = normalize_input(minutes)
    y_new = cs(x_new)

    return denormalize_output(y_new)
#day + hours  
def convert_time_in_energy(day , hours , minutes):
    hours = hours
    #print("minutes converted :" , round(normalize_minutes(convert_hours_in_minutes(hours)),2))
    day = day+round(normalize_minutes(convert_hours_in_minutes(hours , minutes)),2)
    print("day :" , day)
    Q = convert_day_in_energy(day)
    print("Q :" , Q)
    return Q