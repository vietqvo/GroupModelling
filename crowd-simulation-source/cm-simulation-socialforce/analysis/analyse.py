import brewer2mpl
import matplotlib.pyplot as plt
from pylab import *
import datetime
import pandas as pd
import matplotlib
import numpy as np
from scipy import stats

fig = plt.figure(figsize=(10, 90))

def plot_data_and_hypothesis_testing(time,
									escape_num_different_prototype,
									escape_num_average_prototype,
									 
									escape_time_different_prototype,
									escape_time_average_prototype,
									
									escape_rate_different_prototype,
									escape_rate_average_prototype):
	   	
	ax1 = fig.add_subplot(10,2,2*time+1) 
	
	escape_num_plot = [escape_num_different_prototype,escape_num_average_prototype]

	set1 = brewer2mpl.get_map('Set1', 'qualitative', 7).mpl_colors
	#fig = plt.figure(figsize=(10, 6))

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
	
	
	ax2 = fig.add_subplot(10,2,2*time+2) 
	
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
	
	z,pval_different = stats.normaltest(escape_rate_different_prototype)
	z,pval_average = stats.normaltest(escape_rate_average_prototype)
	
	## apply t-test if normality test satisfied
	## apply Mann-Whitney U test when they do not satisfy normality test -non parametric
	param_text = []
	if pval_different > 0.05 and pval_average >0.05:
		t,prob_ttest = stats.ttest_ind(escape_rate_different_prototype, escape_rate_average_prototype)
		param_text.append("$p-value\/escape\/rate_{t-test}$=%.4f" % prob_ttest)
	else:	
		t,prob_utest = stats.mannwhitneyu(escape_rate_different_prototype, escape_rate_average_prototype)
		param_text.append("$p-value\/escape\/rate_{Mann-Whitney}$=%.4f" % prob_utest)
		
	ax2.text(0.98, 0.85, "\n".join(param_text),
                transform=ax2.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif'},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
				
df = pd.read_csv('parameter.csv')

escape_num_different_prototype =[]
escape_num_average_prototype =[]

escape_time_different_prototype =[]
escape_time_average_prototype =[]

## compute escape rate for two prototypes on each sampling time 
## and apply t-test if normality test of two prototypes satisfied, otherwise we apply Mann-Whitney U test
escape_rate_different_prototype = []
escape_rate_average_prototype = []


i=0
while i< 10:
	
	escape_num_different_prototype.clear()
	escape_num_average_prototype.clear()
	
	escape_time_different_prototype.clear()
	escape_time_average_prototype.clear()
	
	escape_rate_different_prototype.clear()
	escape_rate_average_prototype.clear()

	j=0
	while j<20:
		escape_num_different_prototype.append(df['Ndifference'].values[20*i+j])
		escape_num_average_prototype.append(df['Naverage'].values[20*i+j])
		
		escape_time_different_prototype.append(df['Tdifference'].values[20*i+j])
		escape_time_average_prototype.append(df['Taverage'].values[20*i+j])
		
		escape_rate_different_prototype.append(df['Ndifference'].values[20*i+j]/df['Tdifference'].values[20*i+j])
		escape_rate_average_prototype.append(df['Naverage'].values[20*i+j]/df['Taverage'].values[20*i+j])
		j+=1	
		
	plot_data_and_hypothesis_testing(i, escape_num_different_prototype, escape_num_average_prototype, escape_time_different_prototype, escape_time_average_prototype, escape_rate_different_prototype, escape_rate_average_prototype)		
	
	i+=1	

	
fig.savefig('parameter.pdf', bbox_inches='tight')	
