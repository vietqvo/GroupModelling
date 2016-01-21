import glob, os
import csv
import matplotlib.pyplot as plt
from pylab import *
import datetime
import matplotlib
import numpy as np
from scipy import stats
import pandas as pd

def filter_by_index(df, indexes):
    if len(indexes) < len(df.index):
        new_data_df = df.loc[indexes]
    else:
        new_data_df = df
    
    return new_data_df
def plot_histogram_parameters(array, parameter_name, bin_num, test_time):
    # find mean and max of above three arrays with bin number
    min_value = min(array)
    max_value = max(array)
    if parameter_name == "a_s" or parameter_name == "c_d":
        bins = np.linspace(min_value, max_value, bin_num + 1)
    else:
        bins = np.linspace(min_value, max_value, 66)
    fig, ax1 = plt.subplots(1) 
    weights = np.ones_like(array) / len(array)
    ax1.hist(array, bins, histtype='bar', normed=False, weights=weights, facecolor="blue", alpha=0.7)
    title = r''
    if parameter_name == "c_d":
        title = 'Distribution of cohesion degree'
    elif parameter_name == "a_s":
        title = 'Distribution of average speed'    
    elif parameter_name == "v":
        title = 'Distribution of desired speed'
    elif parameter_name == "re":
        title = 'Distribution of acceleration time'    
    elif parameter_name == "s":
        title = 'Distribution of interaction strength'
        #ax1.set_xlim([1.0, 4.0])
    elif parameter_name == "ra":
        title = 'Distribution of interaction range'
    
    # plt.text(0.0, 3.1, title, horizontalalignment='center', fontsize=13)   
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Probability")    
    figure = plt.gcf()
    file_name = "uni_" + str(test_time) + "_dist_" + parameter_name + ".png"
    figure.savefig(file_name)
    plt.clf()
    plt.close('all')
    
def export_bin_outputs(test_time, filename, observation_name, bin_value, samples_per_bin):
    df = pd.read_csv(filename)
    print("------process ---" + str(test_time) + "---" + filename + " - ")
    
    df_bin1 = df[(df[observation_name] >= 0) & (df[observation_name] < bin_value[0])]
    df_bin2 = df[(df[observation_name] >= bin_value[0]) & (df[observation_name] < bin_value[1])]
    df_bin3 = df[(df[observation_name] >= bin_value[1]) & (df[observation_name] < bin_value[2])]
    df_bin4 = df[(df[observation_name] >= bin_value[2]) & (df[observation_name] < bin_value[3])]
    df_bin5 = df[(df[observation_name] >= bin_value[3]) & (df[observation_name] < bin_value[4])]
    df_bin6 = df[(df[observation_name] >= bin_value[4]) & (df[observation_name] < bin_value[5])]
    df_bin7 = df[(df[observation_name] >= bin_value[5]) & (df[observation_name] < bin_value[6])]
    df_bin8 = df[(df[observation_name] >= bin_value[6]) & (df[observation_name] < bin_value[7])]
    df_bin9 = df[(df[observation_name] >= bin_value[7]) & (df[observation_name] < bin_value[8])]
    df_bin10 = df[(df[observation_name] >= bin_value[8]) & (df[observation_name] <= bin_value[9])]
    
    df_bin1.sort([observation_name], ascending=[True], inplace=True)
    df_bin1.reset_index(drop=True, inplace=True)  
    df_bin2.sort([observation_name], ascending=[True], inplace=True)
    df_bin2.reset_index(drop=True, inplace=True)
    df_bin3.sort([observation_name], ascending=[True], inplace=True)
    df_bin3.reset_index(drop=True, inplace=True)
    df_bin4.sort([observation_name], ascending=[True], inplace=True)
    df_bin4.reset_index(drop=True, inplace=True)
    df_bin5.sort([observation_name], ascending=[True], inplace=True)
    df_bin5.reset_index(drop=True, inplace=True) 
    df_bin6.sort([observation_name], ascending=[True], inplace=True)
    df_bin6.reset_index(drop=True, inplace=True) 
    df_bin7.sort([observation_name], ascending=[True], inplace=True)
    df_bin7.reset_index(drop=True, inplace=True) 
    df_bin8.sort([observation_name], ascending=[True], inplace=True)
    df_bin8.reset_index(drop=True, inplace=True) 
    df_bin9.sort([observation_name], ascending=[True], inplace=True)
    df_bin9.reset_index(drop=True, inplace=True) 
    df_bin10.sort([observation_name], ascending=[True], inplace=True)
    df_bin10.reset_index(drop=True, inplace=True) 
    
    index_df_1 = np.random.randint(0, len(df_bin1.index), samples_per_bin)
    index_df_2 = np.random.randint(0, len(df_bin2.index), samples_per_bin)
    index_df_3 = np.random.randint(0, len(df_bin3.index), samples_per_bin)
    index_df_4 = np.random.randint(0, len(df_bin4.index), samples_per_bin)
    index_df_5 = np.random.randint(0, len(df_bin5.index), samples_per_bin)
    index_df_6 = np.random.randint(0, len(df_bin6.index), samples_per_bin)
    index_df_7 = np.random.randint(0, len(df_bin7.index), samples_per_bin)
    index_df_8 = np.random.randint(0, len(df_bin8.index), samples_per_bin)
    index_df_9 = np.random.randint(0, len(df_bin9.index), samples_per_bin)
    index_df_10 = np.random.randint(0, len(df_bin10.index), samples_per_bin)
    
    new_data_df_1 = filter_by_index(df_bin1, index_df_1)
    new_data_df_2 = filter_by_index(df_bin2, index_df_2)
    new_data_df_3 = filter_by_index(df_bin3, index_df_3)
    new_data_df_4 = filter_by_index(df_bin4, index_df_4)
    new_data_df_5 = filter_by_index(df_bin5, index_df_5)
    new_data_df_6 = filter_by_index(df_bin6, index_df_6)
    new_data_df_7 = filter_by_index(df_bin7, index_df_7)
    new_data_df_8 = filter_by_index(df_bin8, index_df_8)
    new_data_df_9 = filter_by_index(df_bin9, index_df_9)
    new_data_df_10 = filter_by_index(df_bin10, index_df_10)

    final_records = pd.concat([new_data_df_1, new_data_df_2, new_data_df_3, new_data_df_4, new_data_df_5,
    new_data_df_6, new_data_df_7, new_data_df_8, new_data_df_9, new_data_df_10], ignore_index=True).reset_index(drop=True)

    bin_file = "uni_" + str(test_time) + "_" + filename.split(".")[0] + "_bin.csv"    
    final_records.to_csv(path_or_buf=bin_file, sep=',', header=True, index=False, index_label=None, mode='w', encoding=None, line_terminator='\n')
    
    # plot histogram of output
    #plot_histogram_parameters(final_records.ix[:, 4].values, observation_name, len(bin_value), test_time)
    # plot histogram of velocity
    #plot_histogram_parameters(final_records.ix[:, 0].values, "v", len(bin_value), test_time)
    # plot histogram of acceleration time
    #plot_histogram_parameters(final_records.ix[:, 1].values, "re", len(bin_value), test_time)
    # plot histogram of interaction strength
    #plot_histogram_parameters(final_records.ix[:, 2].values, "s", len(bin_value), test_time)
    # plot histogram of interaction range
    #plot_histogram_parameters(final_records.ix[:, 3].values, "ra", len(bin_value), test_time)
    
filenames = ["group_cohesion_output.csv", "group_speed_output.csv"]
observation_name = ["c_d", "a_s"]
bin_value = [0.1 * i for i in range(1, 11)]
test_time = 1
total_samples = 1000
samples_per_bin = total_samples / len(bin_value)

for index in range(0, test_time):
    # perform for group cohesion output
    export_bin_outputs(index, filenames[0], observation_name[0], bin_value, samples_per_bin)
    
    # perform for group average speed
    export_bin_outputs(index, filenames[1], observation_name[1], bin_value, samples_per_bin)
    
    
