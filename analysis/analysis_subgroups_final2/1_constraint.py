import csv
import numpy as np
import pandas as pd

r_strength = [40,35,30] 
r_range = [2.0,2.0,2.0]
a_strength = [20,20,20]
a_range = [2.8,2.6,2.4]

analysis_file = open( "data_s1.csv", "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["r_strength","r_range","a_strength","a_range","c"])
k = [ round(0.1 * x,1) for x in range(2,71)]

for i in range(len(r_strength)):
	for c in k:
		writer.writerow((r_strength[i],r_range[i],a_strength[i],a_range[i],c))
	
analysis_file.close()