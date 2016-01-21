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

""" find not escape_num """
def find_not_escape_num(df):

	simulation_id_tracker = {'N_differential_4':'','N_differential_5':'','N_differential_6':'','N_differential_7':'',
						'N_differential_8':'','N_differential_9':'','N_differential_10':'','N_differential_11':'',
						'N_differential_12':'','N_differential_13':'','N_differential_14':'','N_differential_15':'',
						'N_differential_16':'','N_differential_17':'','N_differential_18':'','N_differential_19':'', 'N_differential_20':'',
						
						'N_average_4':'','N_average_5':'','N_average_6':'','N_average_7':'',
						'N_average_8':'','N_average_9':'','N_average_10':'','N_average_11':'','N_average_12':'',
						'N_average_13':'','N_average_14':'','N_average_15':'','N_average_16':'','N_average_17':'',
						'N_average_18':'','N_average_19':'','N_average_20':'',
						
						'N_a_cutoff_lv3_4':'','N_a_cutoff_lv3_5':'','N_a_cutoff_lv3_6':'','N_a_cutoff_lv3_7':'',
						'N_a_cutoff_lv3_8':'','N_a_cutoff_lv3_9':'','N_a_cutoff_lv3_10':'','N_a_cutoff_lv3_11':'','N_a_cutoff_lv3_12':'',
						'N_a_cutoff_lv3_13':'','N_a_cutoff_lv3_14':'','N_a_cutoff_lv3_15':'','N_a_cutoff_lv3_16':'','N_a_cutoff_lv3_17':'',
						'N_a_cutoff_lv3_18':'','N_a_cutoff_lv3_19':'','N_a_cutoff_lv3_20':'',
						
						'N_a_cutoff_lv1_4':'','N_a_cutoff_lv1_5':'','N_a_cutoff_lv1_6':'','N_a_cutoff_lv1_7':'',
						'N_a_cutoff_lv1_8':'','N_a_cutoff_lv1_9':'','N_a_cutoff_lv1_10':'','N_a_cutoff_lv1_11':'','N_a_cutoff_lv1_12':'',
						'N_a_cutoff_lv1_13':'','N_a_cutoff_lv1_14':'','N_a_cutoff_lv1_15':'','N_a_cutoff_lv1_16':'','N_a_cutoff_lv1_17':'',
						'N_a_cutoff_lv1_18':'','N_a_cutoff_lv1_19':'','N_a_cutoff_lv1_20':'',
						
						'N_u_cutoff_lv3_4':'','N_u_cutoff_lv3_5':'','N_u_cutoff_lv3_6':'','N_u_cutoff_lv3_7':'',
						'N_u_cutoff_lv3_8':'','N_u_cutoff_lv3_9':'','N_u_cutoff_lv3_10':'','N_u_cutoff_lv3_11':'','N_u_cutoff_lv3_12':'',
						'N_u_cutoff_lv3_13':'','N_u_cutoff_lv3_14':'','N_u_cutoff_lv3_15':'','N_u_cutoff_lv3_16':'','N_u_cutoff_lv3_17':'',
						'N_u_cutoff_lv3_18':'','N_u_cutoff_lv3_19':'','N_u_cutoff_lv3_20':'',
					
						'N_u_cutoff_lv1_4':'','N_u_cutoff_lv1_5':'','N_u_cutoff_lv1_6':'','N_u_cutoff_lv1_7':'',
						'N_u_cutoff_lv1_8':'','N_u_cutoff_lv1_9':'','N_u_cutoff_lv1_10':'','N_u_cutoff_lv1_11':'','N_u_cutoff_lv1_12':'',
						'N_u_cutoff_lv1_13':'','N_u_cutoff_lv1_14':'','N_u_cutoff_lv1_15':'','N_u_cutoff_lv1_16':'','N_u_cutoff_lv1_17':'',
						'N_u_cutoff_lv1_18':'','N_u_cutoff_lv1_19':'','N_u_cutoff_lv1_20':'',
						}

	array =['N_differential','N_average','N_a_cutoff_lv3','N_a_cutoff_lv1','N_u_cutoff_lv3','N_u_cutoff_lv1']
	for element in array:
		i=0
		while i< 200:		
			if (population_num - df[str(element)].values[i]) ==4:
				str_id = str(element) + str('_4')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==5:
				str_id = str(element) + str('_5')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==6:
				str_id = str(element) + str('_6')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==7:
				str_id = str(element) + str('_7')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==8:
				str_id = str(element) + str('_8')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==9:
				str_id = str(element) + str('_9')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==10:
				str_id = str(element) + str('_10')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==11:
				str_id = str(element) + str('_11')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==12:
				str_id = str(element) + str('_12')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==13:
				str_id = str(element) + str('_13')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==14:
				str_id = str(element) + str('_14')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==15:
				str_id = str(element) + str('_15')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==16:
				str_id = str(element) + str('_16')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==17:
				str_id = str(element) + str('_17')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==18:
				str_id = str(element) + str('_18')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) ==19:
				str_id = str(element) + str('_19')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	
			elif (population_num - df[str(element)].values[i]) >=20:
				str_id = str(element) + str('_20')
				simulation_id_tracker[str_id] += df['SimulationId'].values[i] + ','	

			i+=1	

	return simulation_id_tracker
	
""" load_blockage_frequency_prototypes"""

def load_blockage_frequency_prototypes(blockage_list):
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
			if i==0:
				blockage_frequency_different_prototype[index-4] += len([x.strip() for x in simulation_list.split(',')])
			elif i==1:
				blockage_frequency_average_prototype[index-4] += len([x.strip() for x in simulation_list.split(',')])
			elif i==2:
				blockage_frequency_average_cutoff_lv3_prototype[index-4] += len([x.strip() for x in simulation_list.split(',')])
			elif i==3:
				blockage_frequency_average_cutoff_lv1_prototype[index-4] += len([x.strip() for x in simulation_list.split(',')])
			elif i==4:
				blockage_frequency_uniform_cutoff_lv3_prototype[index-4] += len([x.strip() for x in simulation_list.split(',')])
			elif i==5:
				blockage_frequency_uniform_cutoff_lv1_prototype[index-4] += len([x.strip() for x in simulation_list.split(',')])
				
			index+=1	
				
	plot_blockage_frequency(blockage_frequency_different_prototype,
							blockage_frequency_average_prototype,
							blockage_frequency_average_cutoff_lv3_prototype,
							blockage_frequency_average_cutoff_lv1_prototype,
							blockage_frequency_uniform_cutoff_lv3_prototype,
							blockage_frequency_uniform_cutoff_lv1_prototype)

""" dump blockage frequency """
def plot_blockage_frequency(blockage_frequency_different_prototype,
							blockage_frequency_average_prototype,
							blockage_frequency_average_cutoff_lv3_prototype,
							blockage_frequency_average_cutoff_lv1_prototype,
							blockage_frequency_uniform_cutoff_lv3_prototype,
							blockage_frequency_uniform_cutoff_lv1_prototype
							):
	   	
	ind = np.arange(N) # the x locations for the groups
	width = 0.1       # the width of the bars
	
	fig, ax = plt.subplots()
	
	rects1 = ax.bar(ind, blockage_frequency_different_prototype, width, color='black')
	rects2 = ax.bar(ind+width, blockage_frequency_average_prototype, width, color='red')
	rects3 = ax.bar(ind+2*width, blockage_frequency_average_cutoff_lv3_prototype, width, color='blue')
	rects4 = ax.bar(ind+3*width, blockage_frequency_average_cutoff_lv1_prototype, width, color='yellow')
	rects5 = ax.bar(ind+4*width, blockage_frequency_uniform_cutoff_lv3_prototype, width, color='m')
	rects6 = ax.bar(ind+5*width, blockage_frequency_uniform_cutoff_lv1_prototype, width, color='green')
	
	
	# add some text for labels, title and axes ticks
	ax.set_ylabel('$Frequency\/over\/100\/simulation\/times$')
	fig.suptitle('Blockage occurences over the number of pedestrians left \n total population size = %s' % str(population_num), fontsize=12)
	ax.set_xticks(ind+ 6*width)
	ax.set_xticklabels( ('$4$', '$5$', '$6$','$7$','$8$','$9$','$10$',
						 '$11$','$12$','$13$','$14$','$15$','$16$','$17$',
						 '$18$','$19$','$20$') )
	ax.text(1,-0.09, '$Pedestrians\/left$', transform=ax.transAxes, ha='right', fontsize=16)

	ax.legend( (rects1[0], rects2[0],rects3[0], rects4[0],rects5[0], rects6[0]), 
			('$Prototype_{differential}$', '$Prototype_{average}$',
			'$Prototype_{average\/lv3}}$','$Prototype_{average\/lv1}}$',
			'$Prototype_{uniform\/lv3}$','$Prototype_{uniform\/lv1}$'))
	fig.savefig('blockage_frequency.pdf', bbox_inches='tight')	
	
	

population_num = 70 
N = 17 #for seventeen ranges
			
df = pd.read_csv('with_parameter1.csv')

""" write simulation tracker for real observation on blockages of each simulation"""
simulation_id_tracker = find_not_escape_num(df)
log_file = open( "simulation_id_tracker.txt", "w")
od = collections.OrderedDict(sorted(simulation_id_tracker.items()))
json_obj = json.dumps(od, indent=4)
log_file.write(json_obj)
log_file.close()
