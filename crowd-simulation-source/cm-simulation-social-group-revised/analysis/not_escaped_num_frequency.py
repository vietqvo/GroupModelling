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

				
df = pd.read_csv('parameter_uniform.csv')

different_ped_left_range = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #1st: range >=4, >=5, >=6, >=7, >=8, >=9, >=10,>=11,>=12,>=13,>=14,>=15,>=16,>=17,>=18,>=20
average_ped_left_range = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #for range >=4, >=5, >=6, >=7, >=8, >=9, >=10,>=11,>=12,>=13,>=14,>=15,>=16,>=17,>=18,>=19,>=20

simulation_id_tracker = {'different_p_4':'','different_p_5':'','different_p_6':'','different_p_7':'',
						'different_p_8':'','different_p_9':'','different_p_10':'','different_p_11':'',
						'different_p_12':'','different_p_13':'','different_p_14':'','different_p_15':'',
						'different_p_16':'','different_p_17':'','different_p_18':'','different_p_19':'',
						'different_p_20':'','average_p_4':'','average_p_5':'','average_p_6':'','average_p_7':'',
						'average_p_8':'','average_p_9':'','average_p_10':'','average_p_11':'','average_p_12':'',
						'average_p_13':'','average_p_14':'','average_p_15':'','average_p_16':'','average_p_17':'',
						'average_p_18':'','average_p_19':'','average_p_20':''}

i=0
while i< 200:	
	
	if (population_num - df['Ndifference'].values[i]) >=4: 
		different_ped_left_range[0] +=1		
		if (population_num - df['Ndifference'].values[i]) ==4:
			simulation_id_tracker['different_p_4']+=  df['SimulationId'].values[i] + ','		
		elif (population_num - df['Ndifference'].values[i]) ==5:
			simulation_id_tracker['different_p_5']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==6:
			simulation_id_tracker['different_p_6']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==7:
			simulation_id_tracker['different_p_7']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==8:
			simulation_id_tracker['different_p_8']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==9:
			simulation_id_tracker['different_p_9']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==10:
			simulation_id_tracker['different_p_10']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==11:
			simulation_id_tracker['different_p_11']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==12:
			simulation_id_tracker['different_p_12']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==13:
			simulation_id_tracker['different_p_13']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==14:
			simulation_id_tracker['different_p_14']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==15:
			simulation_id_tracker['different_p_15']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==16:
			simulation_id_tracker['different_p_16']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==17:
			simulation_id_tracker['different_p_17']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==18:
			simulation_id_tracker['different_p_18']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) ==19:
			simulation_id_tracker['different_p_19']+=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Ndifference'].values[i]) >=20:
			simulation_id_tracker['different_p_20']+=  df['SimulationId'].values[i] + ','

			
	if (population_num - df['Ndifference'].values[i]) >=5:	
		different_ped_left_range[1] +=1	
	if (population_num - df['Ndifference'].values[i]) >=6: 
		different_ped_left_range[2] +=1	
	if (population_num - df['Ndifference'].values[i]) >= 7: 
		different_ped_left_range[3] +=1	
	if (population_num - df['Ndifference'].values[i]) >= 8: 
		different_ped_left_range[4] +=1	
	if (population_num - df['Ndifference'].values[i]) >= 9: 
		different_ped_left_range[5] +=1	
	if (population_num - df['Ndifference'].values[i]) >= 10: 
		different_ped_left_range[6] +=1
	if (population_num - df['Ndifference'].values[i]) >= 11: 
		different_ped_left_range[7] +=1
	if (population_num - df['Ndifference'].values[i]) >= 12: 
		different_ped_left_range[8] +=1
	if (population_num - df['Ndifference'].values[i]) >= 13: 
		different_ped_left_range[9] +=1
	if (population_num - df['Ndifference'].values[i]) >= 14: 
		different_ped_left_range[10] +=1
	if (population_num - df['Ndifference'].values[i]) >= 15: 
		different_ped_left_range[11] +=1
	if (population_num - df['Ndifference'].values[i]) >= 16: 
		different_ped_left_range[12] +=1
	if (population_num - df['Ndifference'].values[i]) >= 17: 
		different_ped_left_range[13] +=1
	if (population_num - df['Ndifference'].values[i]) >= 18: 
		different_ped_left_range[14] +=1
	if (population_num - df['Ndifference'].values[i]) >= 19: 
		different_ped_left_range[15] +=1
	if (population_num - df['Ndifference'].values[i]) >= 20: 
		different_ped_left_range[16] +=1
			
	#################### consider for Average prototype ##################################################

	if (population_num - df['Naverage'].values[i]) >=4: 
		average_ped_left_range[0] +=1
		
		if (population_num - df['Naverage'].values[i]) ==4:
			simulation_id_tracker['average_p_4'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==5:
			simulation_id_tracker['average_p_5'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==6:
			simulation_id_tracker['average_p_6'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==7:
			simulation_id_tracker['average_p_7'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==8:
			simulation_id_tracker['average_p_8'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==9:
			simulation_id_tracker['average_p_9'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==10:
			simulation_id_tracker['average_p_10'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==11:
			simulation_id_tracker['average_p_11'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==12:
			simulation_id_tracker['average_p_12'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==13:
			simulation_id_tracker['average_p_13'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==14:
			simulation_id_tracker['average_p_14'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==15:
			simulation_id_tracker['average_p_15'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==16:
			simulation_id_tracker['average_p_16'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==17:
			simulation_id_tracker['average_p_17'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==18:
			simulation_id_tracker['average_p_18'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) ==19:
			simulation_id_tracker['average_p_19'] +=  df['SimulationId'].values[i] + ','
		elif (population_num - df['Naverage'].values[i]) >=20:
			simulation_id_tracker['average_p_20'] +=  df['SimulationId'].values[i] + ','
	
	if (population_num - df['Naverage'].values[i]) >=5:
		average_ped_left_range[1] +=1	
	if (population_num - df['Naverage'].values[i])  >= 6: 
		average_ped_left_range[2] +=1	
	if (population_num - df['Naverage'].values[i])  >= 7: 
		average_ped_left_range[3] +=1	
	if (population_num - df['Naverage'].values[i])  >= 8: 
		average_ped_left_range[4] +=1	
	if (population_num - df['Naverage'].values[i])  >= 9: 
		average_ped_left_range[5] +=1	
	if (population_num - df['Naverage'].values[i])  >= 10: 
		average_ped_left_range[6] +=1
	if (population_num - df['Naverage'].values[i])  >= 11: 
		average_ped_left_range[7] +=1	
	if (population_num - df['Naverage'].values[i])  >= 12: 
		average_ped_left_range[8] +=1	
	if (population_num - df['Naverage'].values[i])  >= 13: 
		average_ped_left_range[9] +=1	
	if (population_num - df['Naverage'].values[i])  >= 14: 
		average_ped_left_range[10] +=1	
	if (population_num - df['Naverage'].values[i])  >= 15: 
		average_ped_left_range[11] +=1	
	if (population_num - df['Naverage'].values[i])  >= 16: 
		average_ped_left_range[12] +=1	
	if (population_num - df['Naverage'].values[i])  >= 17: 
		average_ped_left_range[13] +=1	
	if (population_num - df['Naverage'].values[i])  >= 18: 
		average_ped_left_range[14] +=1		
	if (population_num - df['Naverage'].values[i])  >= 19: 
		average_ped_left_range[15] +=1	
	if (population_num - df['Naverage'].values[i])  >= 20: 
		average_ped_left_range[16] +=1
		
	i+=1	

log_file = open( "simulation_id_tracker_uniform.txt", "w")
json_obj = json.dumps(simulation_id_tracker, indent=4)
log_file.write(json_obj)
log_file.close()
