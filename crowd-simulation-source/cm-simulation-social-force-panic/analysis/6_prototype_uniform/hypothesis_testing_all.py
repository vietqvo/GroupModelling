import brewer2mpl
import matplotlib.pyplot as plt
from pylab import *
import datetime
import pandas as pd
import matplotlib
import numpy as np
from scipy import stats


def hypothesis_testing(element_prototype1, p_value_prototype1, element_prototype2, p_value_prototype2):
	#param_text =""
	
	if p_value_prototype1 > 0.05 and p_value_prototype2 >0.05:
		t,prob_ttest = stats.ttest_ind(element_prototype1, element_prototype2)
		#param_text = "$p-value\/escape\/rate_{normal-test}$=%.4f" % prob_ttest
		return  float("{0:.2f}".format(prob_ttest))
	else:	
		t,prob_utest = stats.mannwhitneyu(element_prototype1, element_prototype2)
		param_text = "$p-value\/escape\/rate_{Mann-Whitney}$=%.4f" % prob_utest
		return  float("{0:.2f}".format(prob_utest))

	#return param_text
	
def plot_element(type, element_differential_prototype, element_average_prototype,
				element_average_cutoff_lv3_prototype, element_average_cutoff_lv1_prototype,
				element_uniform_cutoff_lv3_prototype, element_uniform_cutoff_lv1_prototype):
	
	fig = plt.figure(figsize=(13, 5))	
	ax1 = fig.add_subplot(1,2,1) 
	
	escape_num_plot = [element_differential_prototype,element_average_prototype,
					   element_average_cutoff_lv3_prototype,element_average_cutoff_lv1_prototype,
					   element_uniform_cutoff_lv3_prototype,element_uniform_cutoff_lv1_prototype]

	set1 = brewer2mpl.get_map('Set1', 'qualitative', 7).mpl_colors
	bp1 = ax1.boxplot(escape_num_plot)
	ax1.spines['top'].set_visible(False)
	ax1.spines['right'].set_visible(False)
	ax1.spines['bottom'].set_visible(False)
	ax1.xaxis.set_ticks_position('none')
	ax1.set_xticklabels(['$P_{differential}$','$P_{average}$',
						 '$P_{average\/lv3}$','$P_{average\/lv1}$',
						 '$P_{uniform\/lv3}$','$P_{uniform\/lv1}$'])
	plt.setp(ax1.get_xticklabels(), fontsize=11)
	
	ax1.yaxis.set_ticks_position('none')
	if type ==1:
		ax1.set_title("Total escaped number in t=100", fontsize=12)
		ax1.set_ylabel('Pedestrian Escaped')
	elif type ==2:
		ax1.set_title("Time of last escape in t=100",fontsize=12)
		ax1.set_ylabel('Time(second)')
	
	elif type ==3: ### we measure escape rate by t-test between different prototype with other prototypes
		ax1.set_title("Escape rate",fontsize=12)
		ax1.set_ylabel('Pedestrians/second')
		
		z,pval_differential = stats.normaltest(element_differential_prototype)
		z,pval_average = stats.normaltest(element_average_prototype)
		z,pval_average_lv3 = stats.normaltest(element_average_cutoff_lv3_prototype)
		z,pval_average_lv1 = stats.normaltest(element_average_cutoff_lv1_prototype)
		z,pval_uniform_lv3 = stats.normaltest(element_uniform_cutoff_lv3_prototype)
		z,pval_uniform_lv1 = stats.normaltest(element_uniform_cutoff_lv1_prototype)
		
		## apply t-test if normality test satisfied
		## apply Mann-Whitney U test when they do not satisfy normality test -non parametric
		## apply hypothesis testing to each pair differential with each remaining prototypes
		#param_text = []
		
		
		############### t test of differential prototype
		param_text_with_average = hypothesis_testing(element_differential_prototype,pval_differential, element_average_prototype,pval_average)
		param_text_with_average_lv3 = hypothesis_testing(element_differential_prototype,pval_differential, element_average_cutoff_lv3_prototype,pval_average_lv3)
		param_text_with_average_lv1 = hypothesis_testing(element_differential_prototype,pval_differential, element_average_cutoff_lv1_prototype,pval_average_lv1)
		param_text_with_uniform_lv3 = hypothesis_testing(element_differential_prototype,pval_differential, element_uniform_cutoff_lv3_prototype,pval_uniform_lv3)
		param_text_with_uniform_lv1 = hypothesis_testing(element_differential_prototype,pval_differential, element_uniform_cutoff_lv1_prototype,pval_uniform_lv1)
		
		#ax2 = fig.add_subplot(1,2,2) 
		
		col_labels=['$P_{differential}$']
		row_labels=['$P_{average}$','$P_{average\/lv3}$','$P_{average\/lv1}$','$P_{uniform\/lv3}$','$P_{uniform\/lv1}$']					 
		table_vals=[[param_text_with_average],[param_text_with_average_lv3],[param_text_with_average_lv1],[param_text_with_uniform_lv3],[param_text_with_uniform_lv1]]
		# the rectangle is where I want to place the table
		the_table = plt.table(cellText=table_vals,rowLabels=row_labels,colWidths=[0.1],colLabels=col_labels,loc='center right',bbox=[1.1, 0.5, 0.1, 0.3])
		the_table.set_fontsize(15)
		plt.text(6.25,1.25,'$hypothesis\/testing$',size=10)

	formatter = ScalarFormatter(useOffset=False)
	ax1.yaxis.set_major_formatter(formatter)

	plt.setp(bp1['boxes'], color=set1[1])
	plt.setp(bp1['medians'], color=set1[0])
	plt.setp(bp1['whiskers'], color=set1[1])
	plt.setp(bp1['fliers'], color=set1[1])
	plt.setp(bp1['caps'], color=set1[1])
	
	if type==1:
		fig.savefig('escape_number_analysis.pdf', bbox_inches='tight')
	elif type ==2:
		fig.savefig('escape_time_analysis.pdf', bbox_inches='tight')
	elif type ==3:
		fig.savefig('escape_rate_analysis.pdf', bbox_inches='tight')
	
	plt.clf()
	
df = pd.read_csv('parameter.csv')

escape_num_differential_prototype =[]
escape_num_average_prototype =[]
escape_num_average_cutoff_lv3_prototype =[]
escape_num_average_cutoff_lv1_prototype =[]
escape_num_uniform_cutoff_lv3_prototype =[]
escape_num_uniform_cutoff_lv1_prototype =[]

escape_time_differential_prototype =[]
escape_time_average_prototype =[]
escape_time_average_cutoff_lv3_prototype =[]
escape_time_average_cutoff_lv1_prototype =[]
escape_time_uniform_cutoff_lv3_prototype =[]
escape_time_uniform_cutoff_lv1_prototype =[]


## compute escape rate for two prototypes on each sampling time 
## and apply t-test if normality test of two prototypes satisfied, otherwise we apply Mann-Whitney U test
escape_rate_differential_prototype = []
escape_rate_average_prototype = []
escape_rate_average_cutoff_lv3_prototype =[]
escape_rate_average_cutoff_lv1_prototype =[]
escape_rate_uniform_cutoff_lv3_prototype =[]
escape_rate_uniform_cutoff_lv1_prototype =[]

i=0
while i< 100:

	escape_num_differential_prototype.append(df['N_differential'].values[i])
	escape_num_average_prototype.append(df['N_average'].values[i])
	escape_num_average_cutoff_lv3_prototype.append(df['N_a_cutoff_lv3'].values[i])
	escape_num_average_cutoff_lv1_prototype.append(df['N_a_cutoff_lv1'].values[i])
	escape_num_uniform_cutoff_lv3_prototype.append(df['N_u_cutoff_lv3'].values[i])
	escape_num_uniform_cutoff_lv1_prototype.append(df['N_u_cutoff_lv1'].values[i])
		
	escape_time_differential_prototype.append(df['T_differential'].values[i])
	escape_time_average_prototype.append(df['T_average'].values[i])
	escape_time_average_cutoff_lv3_prototype.append(df['T_a_cutoff_lv3'].values[i])
	escape_time_average_cutoff_lv1_prototype.append(df['T_a_cutoff_lv1'].values[i])
	escape_time_uniform_cutoff_lv3_prototype.append(df['T_u_cutoff_lv3'].values[i])
	escape_time_uniform_cutoff_lv1_prototype.append(df['T_u_cutoff_lv1'].values[i])
		
	escape_rate_differential_prototype.append(df['N_differential'].values[i]/df['T_differential'].values[i])
	escape_rate_average_prototype.append(df['N_average'].values[i]/df['T_average'].values[i])
	escape_rate_average_cutoff_lv3_prototype.append(df['N_a_cutoff_lv3'].values[i]/df['T_a_cutoff_lv3'].values[i])
	escape_rate_average_cutoff_lv1_prototype.append(df['N_a_cutoff_lv1'].values[i]/df['T_a_cutoff_lv1'].values[i])
	escape_rate_uniform_cutoff_lv3_prototype.append(df['N_u_cutoff_lv3'].values[i]/df['T_u_cutoff_lv3'].values[i])
	escape_rate_uniform_cutoff_lv1_prototype.append(df['N_u_cutoff_lv1'].values[i]/df['T_u_cutoff_lv1'].values[i])
		
	i+=1	
	
plot_element(1,escape_num_differential_prototype, escape_num_average_prototype,
			 escape_num_average_cutoff_lv3_prototype,escape_num_average_cutoff_lv1_prototype,
			 escape_num_uniform_cutoff_lv3_prototype,escape_num_uniform_cutoff_lv1_prototype)
			 
plot_element(2,escape_time_differential_prototype, escape_time_average_prototype,
			 escape_time_average_cutoff_lv3_prototype,escape_time_average_cutoff_lv1_prototype,
			 escape_time_uniform_cutoff_lv3_prototype,escape_time_uniform_cutoff_lv1_prototype)			 

plot_element(3,escape_rate_differential_prototype, escape_rate_average_prototype,
			 escape_rate_average_cutoff_lv3_prototype,escape_rate_average_cutoff_lv1_prototype,
			 escape_rate_uniform_cutoff_lv3_prototype,escape_rate_uniform_cutoff_lv1_prototype)