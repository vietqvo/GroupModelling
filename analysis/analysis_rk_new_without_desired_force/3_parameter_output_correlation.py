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

def correlation_test_model_output(rep_s, rep_ra, att_s, att_ra, y, observation_name, rep_s_att_s, rep_ra_att_ra):
    
    if observation_name == "c_d":
        print("test cohesion degree with parameters")
   
    r_row, p_value = spearmanr(y, rep_s)
    print("%s - rep_s spearmanr test: %.3f -  p-value: %.3f" % (observation_name, r_row, p_value))    
    
    r_row, p_value = spearmanr(y, rep_ra)
    print("%s - rep_ra spearmanr test: %.3f - p-value: %.3f" % (observation_name, r_row, p_value))   

    r_row, p_value = spearmanr(y, att_s)
    print("%s - att_s spearmanr test: %.3f -  p-value: %.3f" % (observation_name, r_row, p_value))    
    
    r_row, p_value = spearmanr(y, att_ra)
    print("%s - att_ra spearmanr test: %.3f - p-value: %.3f" % (observation_name, r_row, p_value))   
    
    r_row, p_value = spearmanr(y, rep_s_att_s)
    print("%s - rep_s_att_s spearmanr test: %.3f -  p-value: %.3f" % (observation_name, r_row, p_value))    
    
    r_row, p_value = spearmanr(y, rep_ra_att_ra)
    print("%s - rep_ra_att_ra spearmanr test: %.3f - p-value: %.3f" % (observation_name, r_row, p_value))   
    
def correlation_analysis(filename, observation_name):
    print("process %s" % filename)
    df = pd.read_csv(filename)
    # split data table into data X and group model's output y
    X = df.ix[:, 0:4].values
    y = df.ix[:, 4].values
   
    # measure the correlation and random testing between axis and variables
    rep_s = X[:, 0]
    rep_ra = X[:, 1]
    att_s = X[:, 2]
    att_ra = X[:, 3]
    
    # centre parameters and normalized
    rep_s = center_normalized(rep_s)
    rep_ra = center_normalized(rep_ra)
    att_s = center_normalized(att_s)
    att_ra = center_normalized(att_ra)
    
    # select rep_s_att_s,rep_ra_att_ra and normalized and then test correlation
    rep_s_att_s = df.ix[:, 5].values
    rep_ra_att_ra = df.ix[:, 6].values
    rep_s_att_s = center_normalized(rep_s_att_s)
    rep_ra_att_ra = center_normalized(rep_ra_att_ra)
    correlation_test_model_output(rep_s, rep_ra, att_s, att_ra, y, observation_name, rep_s_att_s, rep_ra_att_ra)
   

filename_c_d = "group_cohesion_output.csv"


# analysis group cohesion degree
correlation_analysis(filename_c_d, "c_d")
