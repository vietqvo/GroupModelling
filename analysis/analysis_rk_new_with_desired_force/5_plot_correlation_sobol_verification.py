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
        labels = ('$v$','$re$','$A_{rep}$', '$B_{rep}$', '$A_{att}$', '$B_{att}$', '$A_{rep}/A_{att}$', '$B_{rep}/B_{att}$')
        N = 8
    else:
        labels = ('$v$','$re$','$A_{rep}$', '$B_{rep}$', '$A_{att}$', '$B_{att}$')
        N = 6

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
        #ax1.set_ylim([0, 1])
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
    figure = plt.gcf()     
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')
    
# ## plot for correlation test, respect to [v,re,s,ra]
group_cohesion_degree = [-0.002, -0.049, 0.118, 0.834, -0.380, -0.341,0.398, 0.897]
plot_correlation(group_cohesion_degree, "c_d")

# ##plot for sobol total indices
group_cohesion_degree = [0.0, 0.0, 0.007700, 0.510752125, 0.1515946,0.16608]
plot_correlation(group_cohesion_degree, "c_d", is_sobol=True)



