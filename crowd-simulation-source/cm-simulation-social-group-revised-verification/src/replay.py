'''
Created on 29 Sep 2015

@author: quangv
'''

import parameters
from src.utility.context import ContextLog_Decoder 
import os, json
from src import constants

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_new50-10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)

repulsive_strength =  40 #20 #2.5
repulsive_range =  2.0 #0.3
attraction_strength =  20 #1.0
attraction_range = 2.85 # 0.46
monte_carlos_simulation.run_aggregate(repulsive_strength,repulsive_range,attraction_strength,attraction_range,context,parameter_distribution_plot=False, simulation=True, drawing=True,rep=True)


"""
context_new40-10
context_new30-10
context_new20-10
context_new10-10
context_new5-10
context_new50-10

repulsive_strength = 2.5 #3.0 
repulsive_range = 0.3
attraction_strength = 1.0#0.5 #0.8
attraction_range = 0.8#1.0

 """
