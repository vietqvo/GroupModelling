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
    
def parse_directory(sub_folder):

    old_directory = os.getcwd()
    os.chdir(sub_folder)
    
    cohesion_file_dir = "../group_output" + str(sub_folder) + ".csv"
    cohesion_file = open(cohesion_file_dir, "w", newline='')
    cohesion_writer = csv.writer(cohesion_file, delimiter=',')
    cohesion_writer.writerow(["R", "r", "A", "a", "constant","equil_time", "cd_hat_cd_bar","cd_hat","cd_bar"])

    for files in os.listdir():
        fullfilename = os.path.splitext(files)
        if fullfilename[1] == '.csv' and os.path.getsize(files) != 0:       
            df = read_csv(fullfilename[0] + fullfilename[1])
            
           
            cohesion_writer.writerow([float(df[0]),float(df[1]),float(df[2]),float(df[3]),float(df[4]),float(df[5]),float(df[6]),float(df[7]),float(df[8])])
    
    cohesion_file.close()
    
dirs = "data_cd"
parse_directory(dirs)
