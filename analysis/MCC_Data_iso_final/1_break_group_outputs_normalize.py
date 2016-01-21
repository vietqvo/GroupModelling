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

def read_csv(fullfilename):
    with open(fullfilename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                return row
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(fullfilename, reader.line_num, e))
    
def normalize_output(fullfilename, str):
    df = pd.read_csv(fullfilename)
    
    # perform centre for output data
    y = df.ix[:, 4].values
    mean = np.mean(y)
    df[str] = df[str] - mean 
    
    # perform normalize for output data
    y = df.ix[:, 4].values
    max_value = max(y)
    min_value = min(y)
    difference = max_value - min_value
    df[str] = (df[str] - min_value) / difference
    # sort data increase
    #df.sort(columns=str, ascending=True, inplace=True)
   
	# replace file
    os.remove(fullfilename)
    if str == "c_d":
        file_dir = "../group_cohesion_output.csv"
    elif str == "a_s":
        file_dir = "../group_speed_output.csv"
        
    df.to_csv(file_dir, header=True, index=False)
    
def parse_directory(sub_folder):

    old_directory = os.getcwd()
    os.chdir(sub_folder)
    
    cohesion_file_dir = "../group_cohesion_output.csv"
    cohesion_file = open(cohesion_file_dir, "w", newline='')
    cohesion_writer = csv.writer(cohesion_file, delimiter=',')
    cohesion_writer.writerow(["v", "re", "s", "ra", "c_d"])
    
    speed_file_dir = "../group_speed_output.csv"
    speed_file = open(speed_file_dir, "w", newline='')
    speed_writer = csv.writer(speed_file, delimiter=',')
    speed_writer.writerow(["v", "re", "s", "ra", "a_s"])
    
    # direction_file_dir = "../group_direction_output.csv"
    # direction_file = open(direction_file_dir, "w", newline='')
    # direction_writer = csv.writer(direction_file, delimiter=',')
    # direction_writer.writerow(["v", "re", "s", "ra", "a_d"])
    
    for files in os.listdir():
        fullfilename = os.path.splitext(files)
        if fullfilename[1] == '.csv':
            if os.path.getsize(files) != 0:
                params = fullfilename[0].split("_")
                v = float(params[0])
                re = float(params[1])
                s = float(params[2])
                ra = float(params[3])
               
                df = read_csv(fullfilename[0] + fullfilename[1])
                
                c_d = float(df[0])
                a_s = float(df[1])
                
                cohesion_writer.writerow([v, re, s, ra, c_d])
                speed_writer.writerow([v, re, s, ra, a_s])
    
    cohesion_file.close()
    speed_file.close()
    
    normalize_output(cohesion_file_dir, "c_d")
    normalize_output(speed_file_dir, "a_s")
    
dirs = "data"
parse_directory(dirs)
