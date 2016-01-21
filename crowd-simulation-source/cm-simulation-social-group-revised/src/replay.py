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

context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)
monte_carlos_simulation.run_aggregate(2.69504208350554,0.365904157795012,3.21379170450382,1.29654491604306,3.69684035750106,1.33654526737519,context,parameter_distribution_plot=False, simulation=True, drawing=True,rep=True)
