import glob, os
import csv
import matplotlib.pyplot as plt
from pylab import *
import datetime
import matplotlib
import numpy as np
from scipy import stats
import pandas as pd
from itertools import islice
from sklearn.preprocessing import StandardScaler

def myround(a, decimals=1):
    return np.around(a-10**(-(decimals+5)), decimals=decimals)
	
def normalize_parameter(df, parameter_name):

    if parameter_name == "v":
        index = 0
    elif parameter_name == "re":
        index = 1
    elif parameter_name == "s":
        index = 2
    elif parameter_name == "ra":
        index = 3
        
    # perform centre for parameter
    y = df.ix[:, index].values
    mean = np.mean(y)
    df[parameter_name] = df[parameter_name] - mean 
    
    # perform normalize for parameter
    y = df.ix[:, index].values
    max_value = max(y)
    min_value = min(y)
    difference = max_value - min_value
    df[parameter_name] = (df[parameter_name] - min_value) / difference
	
    df[parameter_name] = myround(df[parameter_name])
	
    return df
    
def normalize_input(fullfilename, str):
    df = pd.read_csv(fullfilename)
       
    # perform for input parameters
    df = normalize_parameter(df, "v")
    df = normalize_parameter(df, "re")
    df = normalize_parameter(df, "s")
    df = normalize_parameter(df, "ra")

    if str == "c_d":
        file_dir = "group_cohesion_output_sobol.csv"
    elif str == "a_s":
        file_dir = "group_speed_output_sobol.csv"
        
    df.to_csv(file_dir, header=True, index=False)
    

normalize_input("group_cohesion_output.csv", "c_d")
normalize_input("group_speed_output.csv", "a_s")
