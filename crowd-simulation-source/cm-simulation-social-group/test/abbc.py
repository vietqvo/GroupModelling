import csv
import matplotlib.pyplot as plt
from pylab import *
import datetime
import matplotlib
import numpy as np
from scipy import stats
import pandas as pd
from SALib.analyze import sobol

def sobol_analysis(file_name, observation_name):
    print("------process ---" + file_name + " - ")
    df = pd.read_csv(file_name)
    
    problem = {'num_vars': 4,
                'names': ['desired_Velocity', 'acceleration_Time', 'interaction_strength', 'interaction_range'],
                'bounds': [[1.0, 3.0], [0.2, 2.0], [1.0, 4.0], [0.2, 2.0]]
            }
    
    Y = df.ix[:, 4].values
    Si = sobol.analyze(problem, Y, print_to_console=True)

filenames = ["group_cohesion_output.csv", "group_speed_output.csv"]
observation_name = ["c_d", "a_s"]
for i in range(0, 2):
    sobol_analysis(filenames[i], observation_name[i])
