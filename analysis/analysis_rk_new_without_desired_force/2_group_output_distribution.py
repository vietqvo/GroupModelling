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
        plt.title('$Cohesion\/Degree\/Distribution$')
    elif observation_name == "rep_s":
        plt.title('$A_{rep}-Repulsive\/Strength\/Distribution$')
    elif observation_name == "rep_ra":
        plt.title('$B_{rep}-Repulsive\/Range\/Distribution$')
    elif observation_name == "att_s":
        plt.title('$A_{att}-Attractive\/Strength\/Distribution$')
    elif observation_name == "att_ra":
        plt.title('$B_{att}-Attractive\/Range\/Distribution$')
    elif observation_name == "rep_s_att_s":
        plt.title("$A_{rep}/A_{att}\/Distribution$")
    elif observation_name == "rep_ra_att_ra":
        plt.title("$B_{rep}/B_{att}\/Distribution$")    
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
    
filenames = ["group_cohesion_output.csv"]
observation_name = ["c_d", "rep_s", "rep_ra", "att_s", "att_ra", "rep_s_att_s", "rep_ra_att_ra"]
for i in range(0, 7):
    export_bin_outputs(filenames[0], observation_name[i])
