'''
Created on 14 Sep 2015

@author: quangv
'''
import parameters
from src.utility.context import ContextGenerator as context_generator
from src.utility.context import ContextLog_Encoder 
import os, csv, json
from src import constants

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

#generate context (radii and placements)
placement_num = 10
context = context_generator(monte_carlos_simulation._get_parameters(),placement_num)
group_num = monte_carlos_simulation._get_parameters()['group_num']
context_filename = "%s-%s" % ("context_new" + str(group_num),str(placement_num))
log_file = open( "%s.json" % os.path.join(constants.context_dir, context_filename), "w")
json_obj = json.dumps(context, cls=ContextLog_Encoder)
log_file.write(json_obj)
log_file.close()

#create log file
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "parameter"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["SimulationId","cohesion_degree"])
        
simulation_strength_vary_step =  monte_carlos_simulation._get_strength_vary_step()
simulation_range_vary_step =  monte_carlos_simulation._get_range_vary_step()
simulation_attraction_strength_vary_step =  monte_carlos_simulation._get_attraction_strength_vary_step()
simulation_attraction_range_vary_step =  monte_carlos_simulation._get_attraction_range_vary_step()

s_index =0
ra_index =0
att_s_index = 0
att_ra_index = 0

while att_ra_index <= simulation_attraction_range_vary_step:
    att_s_index = 0
    while att_s_index <= simulation_attraction_strength_vary_step:
        ra_index = 0
        while ra_index <= simulation_range_vary_step:
            s_index = 0
            while s_index <= simulation_strength_vary_step:
                monte_carlos_simulation.run_aggregate(s_index,
                                                      ra_index,
                                                      att_s_index,
                                                      att_ra_index,
                                                      context,     
                                                      parameter_distribution_plot=False,
                                                      simulation=True,
                                                      drawing=True)
                        
                writer.writerow((monte_carlos_simulation._get_simulation_index(),monte_carlos_simulation._get_avg_cohesion_degree()))
                s_index +=1
            ra_index+=1
        att_s_index+=1
    att_ra_index+=1
    
analysis_file.close()