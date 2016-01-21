import brewer2mpl
import matplotlib.pyplot as plt
from pylab import *
import datetime
import pandas as pd
import matplotlib
import numpy as np
from scipy import stats
import json
import csv
import collections

population_num = 70 
N = 17 #for seventeen ranges

""" load_blockage_frequency_prototypes"""
def load_blockage_frequency_prototypes(blockage_list, chart_type = 0):
	array =['N_differential','N_average','N_a_cutoff_lv3','N_a_cutoff_lv1','N_u_cutoff_lv3','N_u_cutoff_lv1']
	
	blockage_frequency_different_prototype = [0]*17
	blockage_frequency_average_prototype = [0] *17
	blockage_frequency_average_cutoff_lv3_prototype = [0] *17
	blockage_frequency_average_cutoff_lv1_prototype = [0] *17
	blockage_frequency_uniform_cutoff_lv3_prototype = [0] * 17
	blockage_frequency_uniform_cutoff_lv1_prototype = [0] * 17
	
	for i in range(len(array)):
		index=4
		while index<=20:
			str_ped_left = array[i] + "_" + str(index)
			simulation_list = blockage_list[str_ped_left]
			# split to get ids and through this list to increase at index
			blockage_times = len([x.strip() for x in simulation_list.split(',')]) -1
			#print(str_ped_left + str(blockage_times))
			if i==0:		
				blockage_frequency_different_prototype[index-4] += blockage_times
				if chart_type == 1 and blockage_times >0:
					current_point = index-5
					while current_point >=0:
						blockage_frequency_different_prototype[current_point] +=blockage_times
						current_point -=1
			elif i==1:
				blockage_frequency_average_prototype[index-4] += blockage_times
				if chart_type == 1 and blockage_times >0:
					current_point = index-5
					while current_point >=0:
						blockage_frequency_average_prototype[current_point] +=blockage_times
						current_point -=1
			elif i==2:
				#print(str_ped_left + ' ' + str(blockage_times))
				
				blockage_frequency_average_cutoff_lv3_prototype[index-4] += blockage_times
				if chart_type == 1 and blockage_times >0:
					current_point = index-5
					while current_point >=0:
						blockage_frequency_average_cutoff_lv3_prototype[current_point] +=blockage_times
						#print (str(current_point) + 'increase 1= ' + str(blockage_frequency_average_cutoff_lv3_prototype[current_point]))
						current_point -=1
			elif i==3:
				blockage_frequency_average_cutoff_lv1_prototype[index-4] += blockage_times
				if chart_type == 1 and blockage_times >0:
					current_point = index-5
					while current_point >=0:
						blockage_frequency_average_cutoff_lv1_prototype[current_point] +=blockage_times
						current_point -=1
				
			elif i==4:
				blockage_frequency_uniform_cutoff_lv3_prototype[index-4] += blockage_times
				if chart_type == 1 and blockage_times >0:
					current_point = index-5
					while current_point >=0:
						blockage_frequency_uniform_cutoff_lv3_prototype[current_point] +=blockage_times
						current_point -=1
			elif i==5:
				blockage_frequency_uniform_cutoff_lv1_prototype[index-4] += blockage_times
				if chart_type == 1 and blockage_times >0:
					current_point = index-5
					while current_point >=0:
						blockage_frequency_uniform_cutoff_lv1_prototype[current_point] +=blockage_times
						current_point -=1
			
			index+=1	
		
	plot_blockage_frequency(blockage_frequency_different_prototype,
							blockage_frequency_average_prototype,
							blockage_frequency_average_cutoff_lv3_prototype,
							blockage_frequency_average_cutoff_lv1_prototype,
							blockage_frequency_uniform_cutoff_lv3_prototype,
							blockage_frequency_uniform_cutoff_lv1_prototype, chart_type)


""" dump blockage frequency """
def plot_blockage_frequency(blockage_frequency_different_prototype,
							blockage_frequency_average_prototype,
							blockage_frequency_average_cutoff_lv3_prototype,
							blockage_frequency_average_cutoff_lv1_prototype,
							blockage_frequency_uniform_cutoff_lv3_prototype,
							blockage_frequency_uniform_cutoff_lv1_prototype, chart_type
							):
	   	
	ind = np.arange(N) # the x locations for the groups
	width = 0.15       # the width of the bars
	
	fig, ax = plt.subplots(figsize=(12,6))
	
	rects1 = ax.bar(ind, blockage_frequency_different_prototype, width, color='black')
	rects2 = ax.bar(ind+width, blockage_frequency_average_prototype, width, color='red')
	rects3 = ax.bar(ind+2*width, blockage_frequency_average_cutoff_lv3_prototype, width, color='blue')
	rects4 = ax.bar(ind+3*width, blockage_frequency_average_cutoff_lv1_prototype, width, color='yellow')
	rects5 = ax.bar(ind+4*width, blockage_frequency_uniform_cutoff_lv3_prototype, width, color='m')
	rects6 = ax.bar(ind+5*width, blockage_frequency_uniform_cutoff_lv1_prototype, width, color='green')
	
	
	# add some text for labels, title and axes ticks
	ax.set_ylabel('$Frequency\/over\/100\/simulation\/times$')
	fig.suptitle('Blockage occurences over the number of pedestrians left \n total population size = %s' % str(population_num), fontsize=12)
	ax.set_xticks(ind+ 2*width)
	
	# set tick width
	matplotlib.rcParams['xtick.major.size'] = 20
	matplotlib.rcParams['xtick.major.width'] = 10
	matplotlib.rcParams['xtick.minor.size'] = 15
	matplotlib.rcParams['xtick.minor.width'] = 2

	if chart_type ==0:
		ax.set_xticklabels( ('$4$', '$5$', '$6$','$7$','$8$','$9$','$10$',
							 '$11$','$12$','$13$','$14$','$15$','$16$','$17$',
							 '$18$','$19$','$20$') )							 
	else:
		ax.set_xticklabels( ('$\geqslant4$', '$\geqslant5$', '$\geqslant6$','$\geqslant7$','$\geqslant8$','$\geqslant9$','$\geqslant10$',
							 '$\geqslant11$','$\geqslant12$','$\geqslant13$','$\geqslant14$','$\geqslant15$','$\geqslant16$','$\geqslant17$',
							 '$\geqslant18$','$\geqslant19$','$\geqslant20$') )
							 
	ax.text(1,-0.09, '$Pedestrians\/left$', transform=ax.transAxes, ha='right', fontsize=16)

	ax.legend( (rects1[0], rects2[0],rects3[0], rects4[0],rects5[0], rects6[0]), 
			('$Prototype_{differential}$', '$Prototype_{average}$',
			'$Prototype_{average\/lv3}}$','$Prototype_{average\/lv1}}$',
			'$Prototype_{uniform\/lv3}$','$Prototype_{uniform\/lv1}$'))
	
	if chart_type ==0:	
		fig.savefig('blockage_frequency.pdf', bbox_inches='tight')	
	else:
		fig.savefig('blockage_frequency_accumulated_chart.pdf', bbox_inches='tight')	
	

""" dump blockage frequency after verification by real observation"""
real_blockage_file = open('simulation_id_tracker.txt')
json_str = real_blockage_file.read()
blockage_list =  json.loads(json_str)
load_blockage_frequency_prototypes(blockage_list,0) # type ==1 for accumulated chart 
