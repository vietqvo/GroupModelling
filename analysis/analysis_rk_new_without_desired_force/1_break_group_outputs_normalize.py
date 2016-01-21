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
    # y = df.ix[:, 6].values
    # mean = np.mean(y)
    # df[str] = df[str] - mean 
    
    # perform normalize for output data
    y = df.ix[:, 4].values
    max_value = max(y)
    min_value = min(y)
    difference = max_value - min_value
    df[str] = (df[str] - min_value) / difference
  
    # replace file
    os.remove(fullfilename)
    if str == "c_d":
        file_dir = "../group_cohesion_output.csv"
        
    df.to_csv(file_dir, header=True, index=False)
    
def parse_directory(sub_folder):

    old_directory = os.getcwd()
    os.chdir(sub_folder)
    
    cohesion_file_dir = "../group_cohesion_output.csv"
    cohesion_file = open(cohesion_file_dir, "w", newline='')
    cohesion_writer = csv.writer(cohesion_file, delimiter=',')
    cohesion_writer.writerow(["rep_s", "rep_ra", "att_s", "att_ra", "c_d", "rep_s_att_s", "rep_ra_att_ra"])
    
    for files in os.listdir():
        fullfilename = os.path.splitext(files)
        if fullfilename[1] == '.csv' and os.path.getsize(files) != 0:       
            df = read_csv(fullfilename[0] + fullfilename[1])
                
            rep_s = float(df[0])
            rep_ra = float(df[1])
            att_s = float(df[2])
            att_ra = float(df[3])                
            c_d = float(df[4])
            rep_s_att_s = rep_s / att_s
            rep_ra_att_ra = rep_ra / att_ra
            
            cohesion_writer.writerow([rep_s, rep_ra, att_s, att_ra, c_d, rep_s_att_s, rep_ra_att_ra])
    
    cohesion_file.close()
    
    normalize_output(cohesion_file_dir, "c_d")
    
dirs = "data"
parse_directory(dirs)
