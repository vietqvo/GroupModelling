'''
Created on 16 Feb 2015

@author: quangv
'''
import numpy as np

timestep              = 0.01 # time step to plot and generate new pedestrians
total_monitoring_duration = 500 # total time for our simulation
observation_range =[20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 460, 480, 500] # measure total pedestrians escaped at time t = 20,50, etc

quantification_plot_bin_num = 100 # bin number to plot free velocity distribution

quantification_plot_dir = "../quantification_plots/" # folder for storing quantification plotting figure
observation_plot_dir  = "../observation_plots/" # folder for storing observation plotting figure
image_dir             = "../images/" # folder for storing captured image

framerate_limit       = int(round(1.0/timestep)) # frame rate per second to draw and update canvas = 100

plot_sample_frequency = 0.1
flowrate_moving_avg   = 5.0

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