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
    print("x axis- v spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))  # Spearman rank-order correlation coefficient
    
    r_row, p_value = spearmanr(pc1, re)
    print("x axis- re spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))
    
    r_row, p_value = spearmanr(pc1, s)
    print("x axis- s spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))    
    
    r_row, p_value = spearmanr(pc1, ra)
    print("x axis- ra spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))    
    
    r_row, p_value = spearmanr(pc2, v)
    print("y axis- v spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))
    
    r_row, p_value = spearmanr(pc2, re)
    print("y axis- re spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))
    
    r_row, p_value = spearmanr(pc2, s)
    print("y axis- s spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))    
    
    r_row, p_value = spearmanr(pc2, ra)
    print("y axis- ra spearmanr test: %.3f -  p-value: %.3f" % (r_row, p_value))    

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
    mds = MDS(n_components=lower_dimension, n_init=4, max_iter=500)
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
    
def isomap_analysis(filename, observation_name, K_neighbors, prefix):
    print("process %s" % filename)
    df = pd.read_csv(filename)
    # split data table into data X and group model's output y
    X = df.ix[:, 0:4].values
    y = df.ix[:, 4].values
    n_neighbors = K_neighbors
    # fig = plt.figure(figsize=(8, 8))    

    # test residual variance between ISOMAP, PCA, and MDS
    # test_residual_variance(n_neighbors, y.shape[0], X, observation_name, prefix)
    residual_iso = isomap_residual_variance(n_neighbors, 2, y.shape[0], X)
    print("isomap residual %.3f" % residual_iso)
    # residual_mds = mds_residual_variance(n_neighbors, 2, y.shape[0], X)
    # print("mds residual %.3f" % residual_mds)

    # perform isomap with the lowest K and neighbours
    isomap = Isomap(n_neighbors=n_neighbors, n_components=2)
    X_iso = isomap.fit_transform(X)
     
    cm = mpl.cm.get_cmap('RdYlBu')
    sc = plt.scatter(X_iso[:, 0], X_iso[:, 1], c=y, vmin=min(y), vmax=max(y), s=30, cmap=cm)
    
    # measure the correlation and random testing between axis and variables
    v = X[:, 0]
    re = X[:, 1]
    s = X[:, 2]
    ra = X[:, 3]

    pc1 = X_iso[:, 0]
    pc2 = X_iso[:, 1]

    correlation_test_coordinate(v, re, s, ra, pc1, pc2)
    
    # plot isomap
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
        str_file_name = prefix + "_iso_c_d.png"
        title = r'$Isomap\/of\/group\/cohesion\/degree$' + '\n' + r'$neighbours=' + str(n_neighbors) + '$'
        plt.text(0.0, 2.1, title, horizontalalignment='center', fontsize=13)
         
        #plt.arrow(2.5, -2, -4.5, 0, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)
        #plt.arrow(2.5, -2, 0, 4, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)
        
        #plt.text(1, -2.2, r'$Interaction\/Strength$')
        #plt.text(2.55, -1.0, r'$Desired\/Velocity$', rotation='vertical')
        
    elif observation_name == "a_s":
        str_file_name = prefix + "_iso_a_s.png"
        title = r'$Isomap\/of\/group\/average\/speed$' + '\n' + r'$neighbours=' + str(n_neighbors) + '$'
        plt.text(0.0, 1.6, title, horizontalalignment='center', fontsize=13)
        
        #plt.arrow(2, -1.5, -4, 0, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)  # -3, 0 a desitnation point of arrow is follow direction of original point
        #plt.arrow(2, -1.5, 0, 3, width=0.015, color="k", clip_on=False, head_width=0.12, head_length=0.12)
        
        #plt.text(0.8, -1.6, r'$Interaction\/Strength$')
        #plt.text(2.05, -0.6, r'$Desired\/Velocity$', rotation='vertical')
        
    figure = plt.gcf()
    figure.savefig(str_file_name)
    plt.clf()
    plt.close('all')

Neighbors = [ i for i in range(15, 60)]
def finding_k_isomap(filename, observation_names):
    print("finding K neighbors process %s" % filename)
    df = pd.read_csv(filename)
    # split data table into data X and group model's output y
    X = df.ix[:, 0:4].values
    y = df.ix[:, 4].values
    a = []
    # perform for 2 dimension
    for neighbor in Neighbors:
        residual = isomap_residual_variance(neighbor, 2, y.shape[0], X)
        a.append(residual)
        # print(">>>> %d-neighbor, residual = %.3f " % (neighbor, residual))
    # find the lowest variance
    ind = np.argmin(a)
    print(">>>> lowest K-neighbor %d, residual = %.3f " % (Neighbors[ind], a[ind]))
    return Neighbors[ind]
    
n = 1
filenames = ["_group_cohesion_output_bin.csv", "_group_speed_output_bin.csv"]
observation_names = ["c_d", "a_s"]
for i in range(0, n):
    prefix = "uni_" + str(i)
    filename_c_d = prefix + filenames[0]
    filename_a_s = prefix + filenames[1]
    
    # analysis group cohesion degree
    # find optimal K neighbours so that residual is minimum (<0.1)
    # k_c_d = finding_k_isomap(filename_c_d, observation_names[0])
    isomap_analysis(filename_c_d, observation_names[0], 200, prefix)  # 40
    
    # analysis group average speed
    # k_a_s = finding_k_isomap(filename_a_s, observation_names[0])
    isomap_analysis(filename_a_s, observation_names[1], 300, prefix)  # 40
