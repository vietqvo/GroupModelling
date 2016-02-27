import glob, os
import csv
import matplotlib.pyplot as plt
from pylab import *
import datetime
import numpy as np
from scipy import stats
import pandas as pd
from itertools import islice
from sklearn.preprocessing import StandardScaler
from matplotlib import cm


filename1 = "group_outputdata_context10.csv"
df = pd.read_csv(filename1)

s1 = df[(df.R == 40) & (df.r == 2.0) & (df.A == 20) & (df.a == 2.8)]
s1.sort(['constant'], ascending=[True], inplace=True)
#s1.to_csv("final_data1.csv", header=True, index=False)

s2 = df[(df.R == 35) & (df.r == 2.0) & (df.A == 20) & (df.a == 2.6)]
s2.sort(['constant'], ascending=[True], inplace=True)
#s2.to_csv("final_data2.csv", header=True, index=False)

s3 = df[(df.R == 30) & (df.r == 2.0) & (df.A == 20) & (df.a == 2.4)]
s3.sort(['constant'], ascending=[True], inplace=True)
#s3.to_csv("final_data3.csv", header=True, index=False)

constant1 = s1.ix[:,4].values
cd_ratio1 = s1.ix[:, 6].values
plt.plot(constant1, cd_ratio1, '-r^',label=r'$R=40,\/ r= 2.0,\/A=20,\/a=2.8$') 

constant2 = s2.ix[:,4].values
cd_ratio2 = s2.ix[:, 6].values
#plt.plot(constant2, cd_ratio2, '-g^',label=r'$R=35,\/ r= 2.0,\/A=20,\/a=2.6$')

constant3 = s3.ix[:,4].values
cd_ratio3 = s3.ix[:, 6].values
#plt.plot(constant3, cd_ratio3, '-b^',label=r'$R=30,\/ r= 2.0,\/A=20,\/a=2.4$')

legend = plt.legend(loc='upper center', shadow=True)
plt.xlabel(r'$constant$', fontsize=21)
plt.ylabel(r'$\frac{\hat{cd}}{\bar{cd}}$', rotation='horizontal', fontsize=25)
plt.grid()
plt.show()
