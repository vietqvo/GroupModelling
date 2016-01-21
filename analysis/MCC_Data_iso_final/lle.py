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
    new = [i - np.mean(array) for i in array]
    new = [(i - np.min(new)) / (np.max(new) - np.min(new)) for i in new]
    return new
    
def correlation_test_coordinate(v, re, s, ra, pc1, pc2):
    r_row, p_value = spearmanr(pc1, v)
    print("1-corre spearmanr v: %.3f -  %.3f" % (r_row, p_value))  # Spearman rank-order correlation coefficient
    
    r_row, p_value = spearmanr(pc1, re)
    print("1-corre spearmanr re: %.3f -  %.3f" % (r_row, p_value))
    
    r_row, p_value = spearmanr(pc1, s)
    print("1-corre spearmanr s: %.3f -  %.3f" % (r_row, p_value))    
    
    r_row, p_value = spearmanr(pc1, ra)
    print("1-corre spearmanr ra: %.3f -  %.3f" % (r_row, p_value))    
    
    r_row, p_value = spearmanr(pc2, v)
    print("2-corre spearmanr v: %.3f -  %.3f" % (r_row, p_value))
    
    r_row, p_value = spearmanr(pc2, re)
    print("2-corre spearmanr re: %.3f -  %.3f" % (r_row, p_value))
    
    r_row, p_value = spearmanr(pc2, s)
    print("2-corre spearmanr s: %.3f -  %.3f" % (r_row, p_value))    
    
    r_row, p_value = spearmanr(pc2, ra)
    print("2-corre spearmanr ra: %.3f -  %.3f" % (r_row, p_value))    

def correlation_test_model_output(v, re, s, ra, y, observation_name):
    
    if observation_name == "c_d":
        print("test cohesion degree with parameters")
    else:
        print("test average speed with parameters")
        
    r_row, p_value = spearmanr(y, v)
    print("corre spearmanr v: %.3f -  %.3f" % (r_row, p_value)) 
    
    r_row, p_value = spearmanr(y, re)
    print("corre spearmanr re: %.3f -  %.3f" % (r_row, p_value))
    
    r_row, p_value = spearmanr(y, s)
    print("corre spearmanr s: %.3f -  %.3f" % (r_row, p_value))    
    
    r_row, p_value = spearmanr(y, ra)
    print("corre spearmanr ra: %.3f -  %.3f" % (r_row, p_value))   

    
def isomap_residual_variance(n_neighbors, lower_dimension, no_of_samples, X):
    isomap = Isomap(n_neighbors, lower_dimension)
    X_iso = isomap.fit_transform(X)
    geodesic = isomap.dist_matrix_
    manifold_distance = euclidean_distances(X_iso, X_iso)
    A = reshape(geodesic, (no_of_samples ** 2))
    D = reshape(manifold_distance, (no_of_samples ** 2))
    r2 = 1 - corrcoef(A, D) ** 2; 
    return r2[1][0]

def mds_residual_variance(n_neighbors, lower_dimension, no_of_samples, X):
    mds = MDS(n_components=lower_dimension, n_init=4, max_iter=300)
    X_mds = mds.fit_transform(X)
    original_distance = euclidean_distances(X, X)
    manifold_distance = euclidean_distances(X_mds, X_mds)
    A = reshape(original_distance, (no_of_samples ** 2))
    D = reshape(manifold_distance, (no_of_samples ** 2))
    r2 = 1 - corrcoef(A, D) ** 2; 
    return r2[1][0]
    
def test_residual_variance(n_neighbors, no_of_samples, X, observation_name, prefix):
    dimension = [1, 2, 3, 4]  # this is dimension
    residual_iso_map = []  # this is residual variance value
    residual_iso_pca = []
    residual_iso_mds = []
            
    # perform for ISOMAP method
    for lower_dimension in range(1, 5):
        residual = isomap_residual_variance(n_neighbors, lower_dimension, no_of_samples, X)
        residual_iso_map.append(residual)
    
    # perform for PCA method
    for lower_dimension in range(1, 5):
        pca = PCA(n_components=lower_dimension)
        X_r = pca.fit_transform(X)
        residual_iso_pca.append(1 - np.sum(pca.explained_variance_ratio_))
    
    # perform for MDS method
    for lower_dimension in range(1, 5):
        residual = mds_residual_variance(n_neighbors, lower_dimension, no_of_samples, X)
        residual_iso_mds.append(residual)
    
    # plot residual variance, at k = 80
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('$Dimension$')
    ax.set_ylabel('$Residual\/Variance$')
    ax.set_xlim([0, 5])
    ax.set_ylim([0, 1])

    ax.plot(dimension, residual_iso_map, 'bo', color='black', linestyle="-", label="$isomap$")
    ax.plot(dimension, residual_iso_pca, 'b^', color='black', linestyle="-", label="$pca$")
    ax.plot(dimension, residual_iso_mds, 'bs', color='black', linestyle="-", label="$mds$")
    plt.legend(loc='upper right')
    plt.legend(frameon=False)
    figure = plt.gcf()
    if observation_name == "c_d":
        str_file_name = prefix + "_res_var_c_d.png"
    elif observation_name == "a_s":
        str_file_name = prefix + "_res_var_a_s.png"
        
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')
    
def lle_analysis(filename, observation_name, k_neighbors, prefix):
    print("process lle - %s" % filename)
    df = pd.read_csv(filename)
    # split data table into data X and group model's output y
    X = df.ix[:, 0:4].values
    y = df.ix[:, 4].values

    # perform lle with the lowest K and neighbours
    lle = LocallyLinearEmbedding(k_neighbors, n_components=2, method='standard')
    X_lle = lle.fit_transform(X)
    print("error rate %.7f" % lle.reconstruction_error_)
    cm = mpl.cm.get_cmap('RdYlBu')
    sc = plt.scatter(X_lle[:, 0], X_lle[:, 1], c=y, vmin=min(y), vmax=max(y), s=30, cmap=cm)
    
    # measure the correlation and randoom testing between axis and variables
    v = X[:, 0]
    re = X[:, 1]
    s = X[:, 2]
    ra = X[:, 3]
    
    # center parameters and normalized
    v = center_normalized(v)
    re = center_normalized(re)
    s = center_normalized(s)
    ra = center_normalized(ra)

    
    pc1 = X_lle[:, 0]
    pc2 = X_lle[:, 1]
    
    correlation_test_coordinate(v, re, s, ra, pc1, pc2)
    
    correlation_test_model_output(v, re, s, ra, y, observation_name)
    

    # plot lle
    cbar = plt.colorbar(sc)
    if observation_name == "c_d":
        cbar.ax.set_ylabel('$cohesion\/degree$')
    elif observation_name == "a_s":
        cbar.ax.set_ylabel('$average\/speeed$')
    plt.legend()
    frame1 = plt.gca()
    frame1.axes.xaxis.set_ticklabels([])
    frame1.axes.yaxis.set_ticklabels([])

    if observation_name == "c_d":
        str_file_name = prefix + "_lle_c_d.png"
        title = r'$LLE\/of\/group\/cohesion\/degree$'
        plt.text(0.0, 3.2, title, horizontalalignment='center', fontsize=13)
         
        # plt.arrow(-3, -3, 7, 0, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)
        # plt.arrow(-3, -3, 0, 6, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)
        
        # plt.text(-3, -3.5, r'$Interaction\/Range$')
        # plt.text(-3.5, 0, r'$Interaction\/Strength$', rotation='vertical')
        
    elif observation_name == "a_s":
        str_file_name = prefix + "_lle_a_s.png"
        title = r'$LLE\/of\/group\/average\/speed$'
        plt.text(0.0, 3.2, title, horizontalalignment='center', fontsize=13)
        
        # plt.arrow(3, -3, -6, 0, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)  # -3, 0 a desitnation point of arrow is follow direction of original point
        # plt.arrow(3, -3, 0, 6, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)
        
        # plt.text(1.5, -3.5, r'$Desired\/Velocity$')
        # plt.text(3.1, -1.0, r'$Interaction\/Strength$', rotation='vertical')
        
    figure = plt.gcf()
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')
    
n = 1
filenames = ["_group_cohesion_output_bin.csv", "_group_speed_output_bin.csv"]
observation_names = ["c_d", "a_s"]
for i in range(0, n):
    prefix = "uni_" + str(i)
    filename_c_d = prefix + filenames[0]
    filename_a_s = prefix + filenames[1]
    
    # analysis group cohesion degree
    lle_analysis(filename_c_d, observation_names[0], 200, prefix)  # 40
    
    # analysis group average speed
    lle_analysis(filename_a_s, observation_names[1], 300, prefix)  # 40
