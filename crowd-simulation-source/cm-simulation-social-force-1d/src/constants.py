'''
Created on 16 Feb 2015

@author: quangv
'''
import numpy as np
import random

timestep              = 0.01 # time step to calculate new position and velocity
total_monitoring_duration_bi_direction = 100 # total time for our simulation in bi-directional flow

quantification_plot_bin_num = 100

parameter_distribution_dir = "../parameter_distribution/" 
observation_dir  = "../observation/" 
image_dir = "../images/"
video_dir = "../videos/" 
analysis_dir = "../analysis/" 
log_dir = "../log/" 
pedestrian_track_dir = "../pedestrian_track/"
threshold_track_pedestrian_pos = 0.5 

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
        