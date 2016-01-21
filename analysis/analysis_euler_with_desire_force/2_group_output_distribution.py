import glob, os
import csv
import matplotlib.pyplot as plt
from pylab import *
import datetime
import matplotlib
import numpy as np
from scipy import stats
import pandas as pd

def export_bin_outputs(filename, observation_name):
    df = pd.read_csv(filename)
    dfList = df[observation_name].tolist()
    arr = np.array(dfList)
    
    # find mean and max of above three arrays with bin number
    min_value = min(arr)
    max_value = max(arr)
    bins = np.linspace(min_value, max_value, 11)
    
    fig, ax1 = plt.subplots(1) 
    weights = np.ones_like(arr) / len(arr)
    ax1.hist(arr, bins, histtype='bar', normed=False, weights=weights, facecolor="blue", alpha=0.8)
    if observation_name == "c_d":
        plt.title('Cohesion Degree Distribution')
    elif observation_name == "a_s":
        plt.title('Average Speed Distribution')
    elif observation_name == "a_d":
        plt.title('Velocity Direction Distribution')
      
    # normal test    
    z, pval_value = stats.normaltest(arr)
    # if pval_different > 0.05:
    ax1_param_text = []
    if pval_value < 0.05:
        ax1_param_text.append("$ normal\/test (p_{value} < 0.05)$")
           
    ax1.text(0.98, 0.95, "\n".join(ax1_param_text),
                transform=ax1.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 10},
                bbox={'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5})
    
    
    plt.xlabel("Value")
    plt.ylabel("Probability")    
    figure = plt.gcf()
    file_name = "dist_" + observation_name + ".png"
    figure.savefig(file_name)
    plt.clf()
    plt.close('all')
    
filenames = ["group_cohesion_output.csv", "group_speed_output.csv"]
observation_name = ["c_d", "a_s"]
for i in range(0, 2):
    export_bin_outputs(filenames[i], observation_name[i])
