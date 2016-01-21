'''
Created on 19 Nov 2015

@author: quangv
'''
import parameters
from src.utility.context import ContextGenerator as context_generator
from src.utility.context import ContextLog_Decoder 
from src.utility.context import ContextLog_Encoder 
import os, json
from src import constants
import csv

#current alpha = 10 degree homogeneous

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)

step = 0.2
 
desired_velocity = [1.0,3.0]

acceleration_time = [0.2,2.0]

interaction_strength = [1.0,4.0]

interaction_range = [0.2,2.0]

attraction_strength = [1.0,4.0]

attraction_range = [0.2,2.0]
   
#test for desired_velocity
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "verification_velocity"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["v","re","rep_s","rep_ra","att_s","att_ra","cohesion_degree","average_speed","average_direction"])

start = desired_velocity[0]
while start <=desired_velocity[1]:
    monte_carlos_simulation.run_aggregate(start,acceleration_time[0],
                                          interaction_strength[0],interaction_range[0],
                                          attraction_strength[0],attraction_range[0],
                                          context,parameter_distribution_plot=False, simulation=True, drawing=False,rep=True)
    writer.writerow((start,acceleration_time[0],
                     interaction_strength[0],interaction_range[0],
                     attraction_strength[0],attraction_range[0],
                     monte_carlos_simulation._get_avg_cohesion_degree(),
                     monte_carlos_simulation._get_avg_speed(),
                     monte_carlos_simulation._get_avg_direction()))
    start += step
    
analysis_file.close()
    
#test for acceleration_time
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "verification_acceleration"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["v","re","rep_s","rep_ra","att_s","att_ra","cohesion_degree","average_speed","average_direction"])

start = acceleration_time[0]
while start <=acceleration_time[1]:
    monte_carlos_simulation.run_aggregate(desired_velocity[0],start,
                                          interaction_strength[0],interaction_range[0],
                                          attraction_strength[0],attraction_range[0],
                                          context,parameter_distribution_plot=False, simulation=True, drawing=False,rep=True)
    writer.writerow((desired_velocity[0],start,
                     interaction_strength[0],interaction_range[0],
                     attraction_strength[0],attraction_range[0],
                     monte_carlos_simulation._get_avg_cohesion_degree(),
                     monte_carlos_simulation._get_avg_speed(),
                     monte_carlos_simulation._get_avg_direction()))
    start += step
    
analysis_file.close()

#test for interaction strength
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "verification_interaction_strength"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["v","re","rep_s","rep_ra","att_s","att_ra","cohesion_degree","average_speed","average_direction"])

start = interaction_strength[0]
while start <=interaction_strength[1]:
    monte_carlos_simulation.run_aggregate(desired_velocity[0],acceleration_time[0],
                                          start,interaction_range[0],
                                          attraction_strength[0],attraction_range[0],
                                          context,parameter_distribution_plot=False, simulation=True, drawing=False,rep=True)
    writer.writerow((desired_velocity[0],acceleration_time[0],
                     start,interaction_range[0],
                     attraction_strength[0],attraction_range[0],
                     monte_carlos_simulation._get_avg_cohesion_degree(),
                     monte_carlos_simulation._get_avg_speed(),
                     monte_carlos_simulation._get_avg_direction()))
    start += step

analysis_file.close()
    
#test for interaction range
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "verification_interaction_range"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["v","re","rep_s","rep_ra","att_s","att_ra","cohesion_degree","average_speed","average_direction"])

start = interaction_range[0]
while start <=interaction_strength[1]:
    monte_carlos_simulation.run_aggregate(desired_velocity[0],acceleration_time[0],
                                          interaction_strength[0],start,
                                          attraction_strength[0],attraction_range[0],
                                          context,parameter_distribution_plot=False, simulation=True, drawing=False,rep=True)
    writer.writerow((desired_velocity[0],acceleration_time[0],
                     interaction_strength[0],start,
                     attraction_strength[0],attraction_range[0],
                     monte_carlos_simulation._get_avg_cohesion_degree(),
                     monte_carlos_simulation._get_avg_speed(),
                     monte_carlos_simulation._get_avg_direction()))
    start += step 
    
analysis_file.close()    

#test for attraction strength
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "verification_attraction_strength"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["v","re","rep_s","rep_ra","att_s","att_ra","cohesion_degree","average_speed","average_direction"])

start = attraction_strength[0]
while start <=attraction_strength[1]:
    monte_carlos_simulation.run_aggregate(desired_velocity[0],acceleration_time[0],
                                          interaction_strength[0],interaction_range[0],
                                          start,attraction_range[0],
                                          context,parameter_distribution_plot=False, simulation=True, drawing=False,rep=True)
    writer.writerow((desired_velocity[0],acceleration_time[0],
                     interaction_strength[0],interaction_range[0],
                     start,attraction_range[0],
                     monte_carlos_simulation._get_avg_cohesion_degree(),
                     monte_carlos_simulation._get_avg_speed(),
                     monte_carlos_simulation._get_avg_direction()))
    start += step 
    
analysis_file.close()  


#test for attraction range
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "verification_attraction_range"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["v","re","rep_s","rep_ra","att_s","att_ra","cohesion_degree","average_speed","average_direction"])

start = attraction_range[0]
while start <=attraction_range[1]:
    monte_carlos_simulation.run_aggregate(desired_velocity[0],acceleration_time[0],
                                          interaction_strength[0],interaction_range[0],
                                          attraction_strength[0],start,
                                          context,parameter_distribution_plot=False, simulation=True, drawing=False,rep=True)
    writer.writerow((desired_velocity[0],acceleration_time[0],
                     interaction_strength[0],interaction_range[0],
                     attraction_strength[0],start,
                     monte_carlos_simulation._get_avg_cohesion_degree(),
                     monte_carlos_simulation._get_avg_speed(),
                     monte_carlos_simulation._get_avg_direction()))
    start += step 
    
analysis_file.close()