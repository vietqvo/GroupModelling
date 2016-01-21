'''
Created on 29 Sep 2015

@author: quangv
'''
from src.pygame_drawing.replication import Replication

"""replication = Replication("1.0_0.2_1.0_0.2_7")._replay() """

import parameters
from src.utility.context import ContextGenerator as context_generator
from src.utility.context import ContextLog_Decoder 
from src.utility.context import ContextLog_Encoder 
import os, json
from src import constants


#current alpha = 10 degree homogeneous

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)
monte_carlos_simulation.run_aggregate(1.2,0.8,1.4,2.4,context,parameter_distribution_plot=False, simulation=True, drawing=True,rep=True)
#2.0,1.8,3.2,1.8

#2.0,1.8,4.0,2.0

#2.2,2.0,3.8,1.6