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

population_num = 70 
N = 17 #for seventeen ranges

def plot_blockage_frequency(ecape_num_different_prototype,
							escape_num_average_prototype,
							):
	   	
	ind = np.arange(N) # the x locations for the groups
	width = 0.35       # the width of the bars
	
	fig, ax = plt.subplots()
	
	rects1 = ax.bar(ind+width, escape_num_average_prototype, width, color='red')
	rects2 = ax.bar(ind, ecape_num_different_prototype, width, color='black')
		
	# add some text for labels, title and axes ticks
	ax.set_ylabel('$Frequency\/over\/200\/simulation\/times$')
	fig.suptitle('Blockage occurences over different sizes \n population size = %s' % str(population_num), fontsize=12)
	ax.set_xticks(ind+width)
	ax.set_xticklabels( ('$ 4$', '$5$', '$6$','$7$','$8$','$9$','$10$',
						 '$11$','$12$','$13$','$14$','$15$','$16$','$17$',
						 '$18$','$19$','$20$') )
	ax.text(1,-0.09, '$Pedestrians\/left$', transform=ax.transAxes, ha='right', fontsize=16)

	ax.legend( (rects1[0], rects2[0]), ('$Prototype_{uniform\/average}$', '$Prototype_{different}$'))
	fig.savefig('blockage_frequency_uniform_exactnum.pdf', bbox_inches='tight')	
				
df = pd.read_csv('simulation_id_tracker_uniform_blockage_escape_time_p_different.csv')

different_ped_left_range = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #1st: range >=4, >=5, >=6, >=7, >=8, >=9, >=10,>=11,>=12,>=13,>=14,>=15,>=16,>=17,>=18,>=20
average_ped_left_range = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #for range >=4, >=5, >=6, >=7, >=8, >=9, >=10,>=11,>=12,>=13,>=14,>=15,>=16,>=17,>=18,>=19,>=20

i=0
while i< 8:	
	
	if (population_num - df['Ndifference'].values[i]) ==4: 
		different_ped_left_range[0] +=1			
	if (population_num - df['Ndifference'].values[i]) ==5:	
		different_ped_left_range[1] +=1	
	if (population_num - df['Ndifference'].values[i]) ==6: 
		different_ped_left_range[2] +=1	
	if (population_num - df['Ndifference'].values[i]) == 7: 
		different_ped_left_range[3] +=1	
	if (population_num - df['Ndifference'].values[i]) == 8: 
		different_ped_left_range[4] +=1	
	if (population_num - df['Ndifference'].values[i]) == 9: 
		different_ped_left_range[5] +=1	
	if (population_num - df['Ndifference'].values[i]) == 10: 
		different_ped_left_range[6] +=1
	if (population_num - df['Ndifference'].values[i]) == 11: 
		different_ped_left_range[7] +=1
	if (population_num - df['Ndifference'].values[i]) == 12: 
		different_ped_left_range[8] +=1
	if (population_num - df['Ndifference'].values[i]) == 13: 
		different_ped_left_range[9] +=1
	if (population_num - df['Ndifference'].values[i]) == 14: 
		different_ped_left_range[10] +=1
	if (population_num - df['Ndifference'].values[i]) == 15: 
		different_ped_left_range[11] +=1
	if (population_num - df['Ndifference'].values[i]) == 16: 
		different_ped_left_range[12] +=1
	if (population_num - df['Ndifference'].values[i]) == 17: 
		different_ped_left_range[13] +=1
	if (population_num - df['Ndifference'].values[i]) == 18: 
		different_ped_left_range[14] +=1
	if (population_num - df['Ndifference'].values[i]) == 19: 
		different_ped_left_range[15] +=1
	if (population_num - df['Ndifference'].values[i]) == 20: 
		different_ped_left_range[16] +=1
	
	i+=1	

	
	#################### consider for Average prototype ##################################################
df = pd.read_csv('simulation_id_tracker_uniform_blockage_escape_time_p_average.csv')

i=0
while i< 48:	

	if (population_num - df['Naverage'].values[i]) ==4: 
		average_ped_left_range[0] +=1
	
	if (population_num - df['Naverage'].values[i]) ==5:
		average_ped_left_range[1] +=1	
	if (population_num - df['Naverage'].values[i])  == 6: 
		average_ped_left_range[2] +=1	
	if (population_num - df['Naverage'].values[i])  == 7: 
		average_ped_left_range[3] +=1	
	if (population_num - df['Naverage'].values[i])  == 8: 
		average_ped_left_range[4] +=1	
	if (population_num - df['Naverage'].values[i])  == 9: 
		average_ped_left_range[5] +=1	
	if (population_num - df['Naverage'].values[i])  == 10: 
		average_ped_left_range[6] +=1
	if (population_num - df['Naverage'].values[i])  == 11: 
		average_ped_left_range[7] +=1	
	if (population_num - df['Naverage'].values[i])  == 12: 
		average_ped_left_range[8] +=1	
	if (population_num - df['Naverage'].values[i])  == 13: 
		average_ped_left_range[9] +=1	
	if (population_num - df['Naverage'].values[i])  == 14: 
		average_ped_left_range[10] +=1	
	if (population_num - df['Naverage'].values[i])  == 15: 
		average_ped_left_range[11] +=1	
	if (population_num - df['Naverage'].values[i])  == 16: 
		average_ped_left_range[12] +=1	
	if (population_num - df['Naverage'].values[i])  == 17: 
		average_ped_left_range[13] +=1	
	if (population_num - df['Naverage'].values[i])  == 18: 
		average_ped_left_range[14] +=1		
	if (population_num - df['Naverage'].values[i])  == 19: 
		average_ped_left_range[15] +=1	
	if (population_num - df['Naverage'].values[i])  == 20: 
		average_ped_left_range[16] +=1
		
	i+=1	

plot_blockage_frequency(different_ped_left_range, average_ped_left_range)	
