'''
Created on 16 Feb 2015

@author: quangv
'''
import numpy as np
import random

timestep              = 0.01 # time step to calculate new position and velocity
total_monitoring_duration_uni_direction = 100 # total time for our simulation in unique directional flow
total_monitoring_duration_bi_direction = 200 # total time for our simulation in bi-directional flow
cut_off_first_period = 10 #second, we cut off first ten-second period for the group cohesion emerge 
cut_off_last_period = 5 #seconds, we cut off the last five-second period to maintain the pattern of group
  

quantification_plot_bin_num = 100 # bin number to plot quantification distribution
max_samples = 100 # the number is used to maximize population when sampling with numpy

parameter_distribution_dir = "../parameter_distribution/" # folder for storing parameter distribution plotting figure

observation_dir  = "../observation/" # folder for storing observation plotting figure
image_dir = "../images/" #folder to store simulation's image
video_dir = "../videos/" #folder to store simulation's video
analysis_dir = "../analysis/" #folder to store analysis plot
log_dir = "../log/" #folder to store log
context_dir = "../context/" #folder to store context
pedestrian_track_dir = "../pedestrian_track/"
threshold_track_pedestrian_pos = 0.5 #this value is used to find pedestrian ID when user clicks on simulation environment

framerate_limit       = int(round(1.0/timestep)) # frame rate per second to draw and update canvas = 5
plot_sample_frequency = 1 #second ~ 1/0.01 = 100 frames

def remove_subset(original_cells, removed_cells):
    #only remove one time in orginal_cess from items in removed_cells
    # since it may be floored before
    removed_items = []
    index=0
    while index<len(original_cells):
        if original_cells[index] in removed_cells and original_cells[index] not in removed_items:
            removed_items.append(original_cells[index])
            original_cells.remove(original_cells[index])
            
        else:
            index+=1;

    return original_cells 
  
def myround(a, decimals=1):
    return np.around(a-10**(-(decimals+5)), decimals=decimals)
  
def _filter_samples_by_mean(array, num):
        filtered_array =[item for item in array if item>0]
        if len(filtered_array) < num:
            return filtered_array
        else:
            return random.sample(filtered_array, num)
        