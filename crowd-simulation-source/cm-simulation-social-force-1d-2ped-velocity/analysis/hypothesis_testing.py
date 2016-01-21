import brewer2mpl
import matplotlib.pyplot as plt
from pylab import *
import datetime
import pandas as pd
import matplotlib
import numpy as np
from scipy import stats

fig = plt.figure()

def plot_data_and_hypothesis_testing(
									escape_num_different_prototype,
									escape_num_average_prototype,
									 
									escape_time_different_prototype,
									escape_time_average_prototype,
									
									escape_rate_different_prototype,
									escape_rate_average_prototype):
	   	
	ax1 = fig.add_subplot(1,2,1) 
	
	escape_num_plot = [escape_num_different_prototype,escape_num_average_prototype]

	set1 = brewer2mpl.get_map('Set1', 'qualitative', 7).mpl_colors
	
	bp1 = ax1.boxplot(escape_num_plot)
	ax1.spines['top'].set_visible(False)
	ax1.spines['right'].set_visible(False)
	ax1.spines['bottom'].set_visible(False)
	ax1.xaxis.set_ticks_position('none')
	ax1.set_xticklabels(['Prototype$_{different}$', 'Prototype$_{average}$'])
	
	ax1.yaxis.set_ticks_position('none')
	ax1.set_title("Total escaped number in t=100", fontsize=12)
	ax1.set_ylabel('Pedestrian Escaped')
	formatter = ScalarFormatter(useOffset=False)
	ax1.yaxis.set_major_formatter(formatter)

	plt.setp(bp1['boxes'], color=set1[1])
	plt.setp(bp1['medians'], color=set1[0])
	plt.setp(bp1['whiskers'], color=set1[1])
	plt.setp(bp1['fliers'], color=set1[1])
	plt.setp(bp1['caps'], color=set1[1])
	
	
	ax2 = fig.add_subplot(1,2,2) 
	
	last_escape_time = [escape_time_different_prototype,escape_time_average_prototype]
	bp2 = ax2.boxplot(last_escape_time)
	ax2.spines['top'].set_visible(False)
	ax2.spines['right'].set_visible(False)
	ax2.spines['bottom'].set_visible(False)
	ax2.xaxis.set_ticks_position('none')
	ax2.set_xticklabels(['Prototype$_{different}$', 'Prototype$_{average}$'])

	ax2.yaxis.set_ticks_position('none')
	ax2.set_title("Time of last escape",fontsize=10)
	ax2.set_ylabel('Time(second)')
	ax2.yaxis.set_major_formatter(formatter)

	plt.setp(bp2['boxes'], color=set1[1])
	plt.setp(bp2['medians'], color=set1[0])
	plt.setp(bp2['whiskers'], color=set1[1])
	plt.setp(bp2['fliers'], color=set1[1])
	plt.setp(bp2['caps'], color=set1[1])
	
	#param_text = []
	
	#param_text.append("$escape\/rate_{different\/prototype}$=%.3f" % np.mean(escape_rate_different_prototype))
	#param_text.append("$escape\/rate_{average\/prototype}$=%.3f" % np.mean(escape_rate_average_prototype))
	#ax2.text(0.98, 0.85, "\n".join(param_text),
    #            transform=ax2.transAxes,
    #            verticalalignment='top',
    #            horizontalalignment='right',
    #            fontdict={'family': 'serif'},
    #            bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
    #            )
				
df = pd.read_csv('parameter_uniform_dist.csv')

escape_num_different_prototype =[]
escape_num_average_prototype =[]

escape_time_different_prototype =[]
escape_time_average_prototype =[]

## compute escape rate for two prototypes on each sampling time 
## and apply t-test if normality test of two prototypes satisfied, otherwise we apply Mann-Whitney U test
escape_rate_different_prototype = []
escape_rate_average_prototype = []

escape_num_different_prototype.clear()
escape_num_average_prototype.clear()
	
escape_time_different_prototype.clear()
escape_time_average_prototype.clear()
	
escape_rate_different_prototype.clear()
escape_rate_average_prototype.clear()
	
i=0
while i< 100:
	
	escape_num_different_prototype.append(df['Ndifference'].values[i])
	escape_num_average_prototype.append(df['Naverage'].values[i])
		
	escape_time_different_prototype.append(df['Tdifference'].values[i])
	escape_time_average_prototype.append(df['Taverage'].values[i])
		
	escape_rate_different_prototype.append(df['Ndifference'].values[i]/df['Tdifference'].values[i])
	escape_rate_average_prototype.append(df['Naverage'].values[i]/df['Taverage'].values[i])	
	i+=1	

		
plot_data_and_hypothesis_testing(escape_num_different_prototype, escape_num_average_prototype, escape_time_different_prototype, escape_time_average_prototype, escape_rate_different_prototype, escape_rate_average_prototype)			
fig.savefig('hypothesis_testing_uniform_dist.pdf', bbox_inches='tight')	