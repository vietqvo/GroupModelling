'''
Created on 14 Sep 2015

@author: quangv
'''
import parameters
from src.utility.context import ContextGenerator as context_generator
from src.utility.context import ContextLog_Decoder 
from src.utility.context import ContextLog_Encoder 
import os, csv, json
from src import constants


#current alpha = 10 degree homogeneous

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

#generate radii and placements for placement_num 
"""placement_num = 10
context = context_generator(monte_carlos_simulation._get_parameters(),placement_num)
context_filename = "%s" % ("context_" + str(placement_num))
log_file = open( "%s.json" % os.path.join(constants.context_dir, context_filename), "w")
json_obj = json.dumps(context, cls=ContextLog_Encoder)
log_file.write(json_obj)
log_file.close() """


context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)
            
            
#compute varying times for group social force parameters
simulation_velocity_vary_step =  monte_carlos_simulation._get_velocity_vary_step()
simulation_relax_vary_step =  monte_carlos_simulation._get_relax_vary_step()
simulation_strength_vary_step =  monte_carlos_simulation._get_strength_vary_step()
simulation_range_vary_step =  monte_carlos_simulation._get_range_vary_step()

#create log file
analysis_file = open( "%s.csv" % os.path.join(constants.analysis_dir, "parameter"), "w", newline='')
writer = csv.writer(analysis_file,delimiter=',')
writer.writerow(["SimulationId","cohesion_degree","average_speed","average_direction"])
        
#write log file
v_index =0
re_index =0
s_index =0
ra_index =0

while ra_index <= simulation_range_vary_step:
    s_index = 0
    while s_index <= simulation_strength_vary_step:
        re_index = 0
        while re_index <= simulation_relax_vary_step:
            v_index = 0
            while v_index <= simulation_velocity_vary_step:
                       
                
                monte_carlos_simulation.run_aggregate(v_index,
                                                      re_index,
                                                      s_index,
                                                      ra_index,
                                                      context,     
                                                      parameter_distribution_plot=False,
                                                      simulation=True,
                                                      drawing=True)
                
                writer.writerow((monte_carlos_simulation._get_simulation_index(),monte_carlos_simulation._get_avg_cohesion_degree(),
                                monte_carlos_simulation._get_avg_speed(),
                                monte_carlos_simulation._get_avg_direction()))

                v_index +=1
            re_index+=1 
        s_index +=1
    ra_index+=1

analysis_file.close()