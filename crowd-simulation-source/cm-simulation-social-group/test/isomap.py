'''
Created on 29 Oct 2015

@author: quangv
'''
import numpy as np
import math
from scipy import linalg


def floyd_algorithm(A):
    n = np.shape(A)[0]
    k=0
    while (k <= n-1):
        i=0
        while (i<=n-1):
            j=0
            while(j<=n-1):
                if(A[i][k] + A[k][j] < A[i][j]):
                    A[i][j] = A[i][k] + A[k][j]
                j += 1
            i += 1
        k += 1

    return A

a = [[1,0,0],
     [2,0,0],
     [3,0,0],
     [0,1,0],
     [0,2,0],
     [0,3,0],
     [0,0,1],
     [0,0,2],
     [0,0,3],]

A = np.array(a)
n,m= np.shape(A)
MAX = 999999 #default maximum value

#STEP 0: compute distance matrix between all n objects
distance_matrix = np.zeros((n,n),"float")
for i in range(n):
    for j in range(i+1,n):
        difference = A[i] -A[j]
        distance_matrix[i][j] = math.sqrt(np.dot(difference,difference))
        distance_matrix[j][i]= distance_matrix[i][j]

#STEP 1: construct graph matrix based on distance and K neighbors
K=1
graph = np.zeros((n, n), "float")
for i in range(n):
    for j in range(n):
        graph[i][j] = 0


for i in range(n):
    indexes = [] # indexes content nearest point j of i
    for j in range(n): #construct graph matrix with K nearest point j of i; firstly will be itself
        indexes.append([distance_matrix[i][j], j])
    
    k_index = 0    
    while k_index < K+1: # find K nearest points j of vertex i          
        minlen = MAX
        ki=-1
        t = 0
        k=-1
        for line in indexes:
            if (line[0] <= minlen):
                    minlen = line[0] #assign distance from distance_matrix[i][j] if this is an edge between i and j
                    ki = line[1] #find the nearest point j of i
                    k= t
            else:
                t+=1
        if (ki !=-1 and graph[i][ki]==0):
            graph[i][ki] = distance_matrix[i][ki]       
            if (k!=-1):    
                indexes.pop(k)
            
        k_index+=1
        
for i in range(n):
    for j in range(n):
        if (graph[i][j] < graph[j][i]):
            graph[j][i] = graph[i][j]
#print(graph)

#Step 2: obtain graph of shortest path
#The graph distances are the shortest path distances between all pairs of points in the graph . Points that are not neighbors of each other
#are connected by a sequence of neighbor-to-neighbor links.
graph_path = floyd_algorithm(graph)
spath=[]
for i in range(n):
    spathline=[]
    for j in range(n):
        spathline.append(graph_path[i][j])
    spath.append(spathline)
    
path=np.array(spath)
#print(path)
print(path)
#Step3: apply MDS on shortespath
#convert to mean-centered coordinates
matrixA = np.zeros((n,n), "float")
for i in range(n):
    for j in range(n):
        matrixA[i][j] = path[i][j] **2

matrixA*= -0.5
#print(matrixA)
#compute fit_rows, sum of each row        
a1 = np.zeros(n, "float")
for i in range(n):
    a1[i] = 0.0
    for j in range(n):
        a1[i] = a1[i] + matrixA[i][j]/n
print(a1)
        
a2 = 0.0
for i in range(n):
    for j in range(n):
        a2 = a2 + matrixA[i][j]/(n * n)
        
matrixB = np.zeros((n, n), "float")
for i in range(n):
    for j in range(n):
        matrixB[i][j] = matrixA[i][j] - a1[i] - a1[j] + a2

print(matrixB)

#with 2 components output    
o = 2    
eigenvals, eigenvecs = np.linalg.eig(matrixB)
outdata = np.zeros((n,o), "float")
for i in range(n):
    for j in range(o):
        outdata[i][j] = eigenvecs[i][j] * math.sqrt(eigenvals[j])
        
#print(outdata)  

"""       
G = path ** 2
G *= -0.5
print(G)          
#with 2 components output    
o = 2    
#eigenvals, eigenvecs = np.linalg.eig(matrixB)
eigenvals, eigenvecs = linalg.eigh(G, eigvals=(G.shape[0] - o, G.shape[0] - 1))
#sort by component
indices = eigenvals.argsort()[::-1]
eigenvals= eigenvals[indices]
eigenvecs = eigenvecs[:, indices]
# remove eigenvectors with a zero eigenvalue
eigenvecs = eigenvecs[:, eigenvals > 0]    
eigenvals= eigenvals[eigenvals > 0]  
  
outdata = np.zeros((n,o), "float")
for i in range(n):
    for j in range(o):
        outdata[i][j] = eigenvecs[i][j] * math.sqrt(eigenvals[j])
        
print(outdata)"""        