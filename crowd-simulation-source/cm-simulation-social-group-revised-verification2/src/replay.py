'''
Created on 29 Sep 2015

@author: quangv
'''
#from src.pygame_drawing.replication import Replication

"""replication = Replication("1.0_0.2_1.0_0.2_7")._replay() """

import parameters
from src.utility.context import ContextGenerator as context_generator
from src.utility.context import ContextLog_Decoder 
from src.utility.context import ContextLog_Encoder 
import os, json
from src import constants


#current alpha = 10 degree homogeneous

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_new10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)

desire_velocity = 1.33234575791284
acceleration_time = 0.646143445558846
rep_strength =  2.8077242190484
rep_range= 0.375884617725387
att_strength = 0.645807707565837
att_range = 0.712806584872305
monte_carlos_simulation.run_aggregate(desire_velocity,acceleration_time,rep_strength,rep_range,att_strength,att_range,context,parameter_distribution_plot=False, simulation=True, drawing=True,rep=True)

"""
desire_velocity = 1.2
acceleration_time = 0.3
rep_strength =  3.0
rep_range= 0.3
att_strength = 1.0
att_range = 0.7

desire_velocity = 1.0
acceleration_time = 0.2 
rep_strength =  2.0
rep_range= 0.2
att_strength = 2.0 
att_range = 2.0"""
#