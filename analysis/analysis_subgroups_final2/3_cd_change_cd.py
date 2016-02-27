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


filename1 = "group_outputdata_cd.csv"
df = pd.read_csv(filename1)

s1 = df[(df.R == 40) & (df.r == 2.0) & (df.A == 20) & (df.a == 2.8)]
s1.sort(['constant'], ascending=[True], inplace=True)


constant1 = s1.ix[:,4].values
cd_hat = s1.ix[:, 7].values
cd_bar = s1.ix[:, 8].values
plt.plot(constant1, cd_hat, '-r^',label=r'$\hat cd$') 
plt.plot(constant1, cd_bar, '-b^',label=r'$\bar cd$')

legend = plt.legend(loc='upper center', shadow=True)
plt.title(r'$R=40,\/ r= 2.0,\/A=20,\/a=2.8$')
plt.xlabel(r'$constant$', fontsize=21)
plt.ylabel(r'$Value$', rotation='horizontal', fontsize=23)
plt.grid()
plt.show()
