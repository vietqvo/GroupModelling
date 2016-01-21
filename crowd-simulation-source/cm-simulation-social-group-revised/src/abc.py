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

def plot_correlation(correlation_measure, observation_name, is_sobol=False):
    
    labels = ('Velocity', 'Acceleration Time', 'Interaction Strength', 'Interaction Range', 'Attraction Strength', 'Attraction Range')

    N = 6  # for four ranges

    ind = np.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars
    fig, (ax1) = plt.subplots(1) 

    ax1.bar(ind, correlation_measure, width, color='#deebf7')
    ax1.grid(True)
    # ax1.set_ylabel('Correlation')
    ax1.set_xticks(ind + 2 * width)
    ax1.set_xticklabels(labels, fontsize=7)
    ax1.axhline(0, color='black', lw=2)
    if is_sobol == True:
        ax1.set_title('Sobol total indices')
        ax1.set_ylim([0, 1])
    else:
        ax1.set_title('Spearmanr Correlation testing')
    # ax1.set_ylim([0, 1])
    
    figure = plt.gcf()
    if observation_name == "c_d":
        if is_sobol == True:    
            str_file_name = "sobol_group_cohesion.pdf"
        else:
            str_file_name = "spearman_corr_group_cohesion.pdf"
            
    elif observation_name == "a_s":
        if is_sobol == True:    
            str_file_name = "sobol_group_speed.pdf"
        else:
            str_file_name = "spearman_corr_group_speed.pdf"
            
            
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')

def plot_verification(parameter_measure, model_output, observation_name):
    
    fig, (ax1) = plt.subplots(1) 
    plt.plot(parameter_measure, model_output, 'r--')
    if observation_name == "c_d":  
        str_file_name = "verification_group_cohesion.pdf"
        plt.xlabel('$Group\/cohesion\/degree$')
        plt.ylabel('$Interaction\/range$')
    elif observation_name == "a_s":
        str_file_name = "verification_group_speed.pdf"
        plt.xlabel('$Desired\/velocity$')
        plt.ylabel('$Group\/average\/speed$')
    figure = plt.gcf()     
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')
    
# ## plot for correlation test, respect to [v,re,s,ra]
group_cohesion_degree = [-0.037, 0.097, 0.336, 0.532, -0.279, -0.538]
group_average_speed = [0.98, -0.006, -0.036, 0.000, -0.004, 0.018]
plot_correlation(group_cohesion_degree, "c_d")
plot_correlation(group_average_speed, "a_s")

# ##plot for sobol total indices
group_cohesion_degree = [0.01230296, 0.02873205, 0.19829917, 0.50926055, 0.13349338, 0.39474554]
group_average_speed = [1.0330454448, 0.0013704528, -0.0062102045, 0.0052854656, -0.0047766788, -0.0009141093]
plot_correlation(group_cohesion_degree, "c_d", is_sobol=True)
plot_correlation(group_average_speed, "a_s", is_sobol=True)

# ##plot for verification
group_cohesion_degree = [1.49454794706, 1.65565718431, 1.82110094324, 1.98463713978, 2.15850278054, 2.32000540338, 2.47253632139, 2.61730677406, 2.75474346694, 2.88208100804, 3.00361426377, 3.11922120676, 3.22805320991, 3.33593492143, 3.43089523171, 3.52525688873, 3.61252155255, 3.69647221678, 3.77246557421]
difference = np.max(group_cohesion_degree) - np.min(group_cohesion_degree)
min = np.min(group_cohesion_degree)
group_cohesion_degree = [ (i - min) / difference for i in group_cohesion_degree]
interaction_range = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8]
plot_verification(interaction_range, group_cohesion_degree, "c_d")

group_average_speed = [1.00063319287, 1.20088631095, 1.40114360777, 1.60145285686, 1.80178220732, 2.00215166277, 2.20249421758, 2.40294163464, 2.60338706326, 2.80373264388]
difference = np.max(group_average_speed) - np.min(group_average_speed)
min = np.min(group_average_speed)
group_average_speed = [ (i - min) / difference for i in group_average_speed]
desired_speed = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8]
plot_verification(desired_speed, group_average_speed, "a_s")
