import csv
import matplotlib.pyplot as plt
from pylab import *
import datetime
import matplotlib
import numpy as np
from scipy import stats
from itertools import islice
from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn.manifold import Isomap
from sklearn.manifold import LocallyLinearEmbedding
from matplotlib import cm
from numpy import corrcoef
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from scipy.stats.stats import pearsonr 
from scipy.stats.stats import spearmanr 
from scipy.stats.stats import kendalltau 

def center_normalized(array):
    mean = np.mean(array)
    new = [i - mean for i in array]
    
    min = np.min(new)
    difference = np.max(new) - np.min(new)
    
    new = [(i - min) / difference for i in new]
    return new

def correlation_test_model_output(v, re, s, ra, y, observation_name):
    
    if observation_name == "c_d":
        print("test cohesion degree with parameters")
    else:
        print("test average speed with parameters")
        
    r_row, p_value = spearmanr(y, v)
    print("%s - v spearmanr test: %.3f -  p-value: %.3f" % (observation_name, r_row, p_value)) 
    
    r_row, p_value = spearmanr(y, re)
    print("%s - re spearmanr test: %.3f - p-value: %.3f" % (observation_name, r_row, p_value))
    
    r_row, p_value = spearmanr(y, s)
    print("%s - s spearmanr test: %.3f -  p-value: %.3f" % (observation_name, r_row, p_value))    
    
    r_row, p_value = spearmanr(y, ra)
    print("%s - ra spearmanr test: %.3f - p-value: %.3f" % (observation_name, r_row, p_value))   

  
def correlation_analysis(filename, observation_name):
    print("process %s" % filename)
    df = pd.read_csv(filename)
    # split data table into data X and group model's output y
    X = df.ix[:, 0:4].values
    y = df.ix[:, 4].values
   
    # measure the correlation and random testing between axis and variables
    v = X[:, 0]
    re = X[:, 1]
    s = X[:, 2]
    ra = X[:, 3]

    # centre parameters and normalized
    v = center_normalized(v)
    re = center_normalized(re)
    s = center_normalized(s)
    ra = center_normalized(ra)
    
    correlation_test_model_output(v, re, s, ra, y, observation_name)
   

filename_c_d = "group_cohesion_output.csv"
filename_a_s = "group_speed_output.csv"
    
# analysis group cohesion degree
correlation_analysis(filename_c_d, "c_d") 
    
# analysis group average speed
correlation_analysis(filename_a_s, "a_s") 
