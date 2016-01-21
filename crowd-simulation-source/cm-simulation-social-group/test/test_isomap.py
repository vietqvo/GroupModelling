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
from sklearn.neighbors import NearestNeighbors,kneighbors_graph
from sklearn.utils.graph import graph_shortest_path
from sklearn.decomposition import KernelPCA
import matplotlib as ml
from scipy.stats.stats import pearsonr 
from sklearn.decomposition import PCA
from sklearn.manifold import MDS

def isomap_implement(n_neighbors, lower_dimension, no_of_samples, X):
    isomap = Isomap(n_neighbors, lower_dimension)
    X_iso = isomap.fit_transform(X)
    geodesic = isomap.dist_matrix_
    manifold_distance = euclidean_distances(X_iso, X_iso)

    A = reshape(geodesic, (no_of_samples ** 2))
    D = reshape(manifold_distance, (no_of_samples ** 2))
    r2 = 1 - corrcoef(A, D) ** 2; 
    return r2[1][0]


a = [[1,0,0],
     [2,0,0],
     [3,0,0],
     [0,1,0],
     [0,2,0],
     [0,3,0],
     [0,0,1],
     [0,0,2],
     [0,0,3]]

n_neighbors = 2
A = np.array(a)
print(">>>> %.3f" % isomap_implement(2,2,9,A))

"""isomap = Isomap(n_neighbors=n_neighbors, n_components=2)
X_iso = isomap.fit_transform(A)
print(X_iso)"""

nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(A)
kng = kneighbors_graph(nbrs, n_neighbors, mode='distance')
dist_matrix_ = graph_shortest_path(kng,method='auto',directed=False)
G = dist_matrix_ ** 2
G *= -0.5
kernel_pca_ = KernelPCA(n_components=2,kernel="precomputed",eigen_solver='auto',tol=0, max_iter=None)
embedding_ = kernel_pca_.fit_transform(G)

""" test residual variance"""
manifold_distance = euclidean_distances(embedding_, embedding_)
d1 = reshape(dist_matrix_, (9 ** 2))
d2 = reshape(manifold_distance, (9 ** 2))   
r2 = 1 - corrcoef(d1,d2) ** 2; 
print(">>>> %.3f" % r2[1][0])

""" plot in 2D """    
x = embedding_[:,0]
y = embedding_[:,1]
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
labels = [ "(" + str(A[i][0]) + "," + str(A[i][1]) + "," + str(A[i][2]) + ")" for i in range(A.shape[0])]
ax.scatter(x, y)

"""test correlation"""
d_1 = A[:,0]
d_2 = A[:,1]
d_3 = A[:,2]

#print("1-corre d_1 % .3f" % corrcoef(x,d_1)[1][0])
#print("1-corre d_2 % .3f" % corrcoef(x,d_2)[1][0])
#print("1-corre d_3 % .3f" % corrcoef(x,d_3)[1][0])
print(pearsonr(x,d_1))
print(pearsonr(x,d_2))
print(pearsonr(x,d_3))
#print("2-corre d_1 % .3f" % corrcoef(y,d_1)[1][0])
#print("2-corre d_2 % .3f" % corrcoef(y,d_2)[1][0])
#print("2-corre d_3 % .3f" % corrcoef(y,d_3)[1][0])
print(pearsonr(y,d_1))
print(pearsonr(y,d_2))
print(pearsonr(y,d_3))

""" plot labels """
"""
for label, x, y in zip(labels, x, y):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

plt.show()"""

""" PCA method """
pca = PCA(n_components=2)
X_r = pca.fit_transform(A)
residual_iso_pca = (1 - np.sum(pca.explained_variance_ratio_))

#test LLE method
lle = LocallyLinearEmbedding(2,n_components=2, method='standard')
X_lle = lle.fit_transform(A)
print(lle.get_reconstruction_error_())
print("error rate %.8f" %  lle.reconstruction_error_) 
 
