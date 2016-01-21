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
    
    labels = ('Velocity', 'Acceleration Time', 'Interaction Strength', 'Interaction Range')

    N = 4  # for four ranges

    ind = np.arange(N)  # the x locations for the groups
    width = 0.24  # the width of the bars
    fig, (ax1) = plt.subplots(1) 

    ax1.bar(ind, correlation_measure, width, color='#deebf7')
    ax1.grid(True)
    # ax1.set_ylabel('Correlation')
    ax1.set_xticks(ind + width)
    ax1.set_xticklabels(labels)
    ax1.axhline(0, color='black', lw=2)
    if is_sobol == True:
        ax1.set_title('Sobol total indices')
    else:
    
        ax1.set_title('Spearmanr Correlation testing')
    ax1.set_ylim([0, 1])
    
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
group_cohesion_degree = [-0.070, 0.101, 0.321, 0.914]
group_average_speed = [0.98, -0.096, -0.030, -0.052]
plot_correlation(group_cohesion_degree, "c_d")
plot_correlation(group_average_speed, "a_s")

# ##plot for sobol total indices
group_cohesion_degree = [0.001612646, 0.036832295, 0.169235516, 0.736174361]
group_average_speed = [0.966789036, 0.013210775, 0.002955097, 0.010992766]
plot_correlation(group_cohesion_degree, "c_d", is_sobol=True)
plot_correlation(group_average_speed, "a_s", is_sobol=True)

# ##plot for verification
group_cohesion_degree = [0.84087356782,0.927907880585,0.993584482279,1.08240335437,1.1928221951,1.29968795231,1.40636082545,1.50706784419,1.60147365797,1.69250461545,1.77507575075,1.85510768761,1.93011344873,2.0007894136,2.06874865444,2.13325666601,2.19538469098,2.25349976754,2.30910116949]
difference = np.max(group_cohesion_degree) - np.min(group_cohesion_degree)
min = np.min(group_cohesion_degree)
group_cohesion_degree = [ (i-min)/difference for i in group_cohesion_degree]
interaction_range = [0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8]
plot_verification(interaction_range,group_cohesion_degree,"c_d")

group_average_speed = [0.989407995632, 1.18847947128, 1.38751007434, 1.58531882834, 1.78383979866, 1.98257668872, 2.18227527383, 2.38030337296, 2.57757865394, 2.77431626042]
difference = np.max(group_average_speed) - np.min(group_average_speed)
min = np.min(group_average_speed)
group_average_speed = [ (i-min)/difference for i in group_average_speed]
desired_speed = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8]
plot_verification(desired_speed, group_average_speed, "a_s")


