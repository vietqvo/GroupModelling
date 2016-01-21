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
    
    if is_sobol == False:
        labels = ('$A_{rep}$', '$B_{rep}$', '$A_{att}$', '$B_{att}$', '$A_{rep}/A_{att}$', '$B_{rep}/B_{att}$')
        N = 6
    else:
        labels = ('$A_{rep}$', '$B_{rep}$', '$A_{att}$', '$B_{att}$')
        N = 4
    
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars
    fig, (ax1) = plt.subplots(1) 

    ax1.bar(ind, correlation_measure, width, color='#deebf7')
    ax1.grid(True)
    # ax1.set_ylabel('Correlation')
    ax1.set_xticks(ind + 2 * width)
    ax1.set_xticklabels(labels, fontsize=14)
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
                      
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')

def plot_verification(parameter_measure, model_output, observation_name):
    
    fig, (ax1) = plt.subplots(1) 
    plt.plot(parameter_measure, model_output, 'r--')
    if observation_name == "c_d":  
        str_file_name = "verification_group_cohesion.pdf"
        plt.xlabel('$Interaction\/range$')
        plt.ylabel('$Group\/cohesion\/degree$')
    elif observation_name == "a_s":
        str_file_name = "verification_group_speed.pdf"
        plt.xlabel('$Desired\/velocity$')
        plt.ylabel('$Group\/average\/speed$')
    figure = plt.gcf()     
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')
    
# ## plot for correlation test, respect to [rep_s,rep_ra,att_s,att_ra]
group_cohesion_degree = [0.142, 0.795, -0.364, -0.361, 0.391, 0.877]
plot_correlation(group_cohesion_degree, "c_d")


# ##plot for sobol total indices
group_cohesion_degree = [0.0343, 0.7589, 0.1518, 0.3054]
plot_correlation(group_cohesion_degree, "c_d", is_sobol=True)


# ##plot for verification
group_cohesion_degree = [1.49454794706, 1.65565718431, 1.82110094324, 1.98463713978, 2.15850278054, 2.32000540338, 2.47253632139, 2.61730677406, 2.75474346694, 2.88208100804, 3.00361426377, 3.11922120676, 3.22805320991, 3.33593492143, 3.43089523171, 3.52525688873, 3.61252155255, 3.69647221678, 3.77246557421]
difference = np.max(group_cohesion_degree) - np.min(group_cohesion_degree)
min = np.min(group_cohesion_degree)
group_cohesion_degree = [ (i - min) / difference for i in group_cohesion_degree]
interaction_range = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8]
# plot_verification(interaction_range, group_cohesion_degree, "c_d")

