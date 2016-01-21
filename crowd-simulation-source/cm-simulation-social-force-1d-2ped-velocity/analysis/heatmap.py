import brewer2mpl

from pylab import *
import datetime
import pandas as pd
import matplotlib
import numpy as np
from scipy import stats
import json
import csv

column_labels = [r'$\beta_{x} = \beta_{y}$',r'$\beta_{x} = 2\beta_{y}$',r'$\beta_{x} = 3\beta_{y}$',r'$\beta_{x} = 4\beta_{y}$',r'$\beta_{x} = 5\beta_{y}$']
row_labels = [r'$\alpha_{x} = \alpha_{y}$',r'$\alpha_{x} = 2\alpha_{y}$',r'$\alpha_{x} = 3\alpha_{y}$',r'$\alpha_{x} = 4\alpha_{y}$',r'$\alpha_{x} = 5\alpha_{y}$']
data = np.array([[1.0, 1.0 ,1.0, 1.0,1.0],[0.62, 0.88, 0.92, 0.94, 0.92],[0.24, 0.28, 0.30, 0.42, 0.42],[0.08, 0.20, 0.16, 0.22, 0.20], [0.0, 0.14, 0.10, 0.16, 0.10]])
fig, ax = plt.subplots()
heatmap = ax.pcolor(data, cmap=plt.cm.Blues)

fig = plt.gcf()
fig.set_size_inches(15,11)
# turn off the frame
ax.set_frame_on(False)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
fig.colorbar(heatmap, cax=cbar_ax)

# put the major ticks at the middle of each cell
ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.xaxis.set_ticks_position('both') # THIS IS THE ONLY CHANGE

ax.set_xticklabels(column_labels, minor=False,fontsize=18)
ax.set_yticklabels(row_labels, minor=False,fontsize=18)
fig.savefig('parameter_botteneck_correlation.png')
plt.show()