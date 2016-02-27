'''
Created on 14 Sep 2015

@author: quangv
'''
import parameters
from src.utility.context import ContextGenerator as context_generator
from src.utility.context import ContextLog_Encoder 
import os,json
from src import constants


monte_carlos_simulation = parameters.scenarios['corridorunidirec']

#generate radii and placements for placement_num 
placement_num = 99
parameters = monte_carlos_simulation._get_parameters()
context = context_generator(parameters,placement_num)
context_filename = "%s" % ("context_" + str(placement_num))

log_file = open( "%s.json" % os.path.join(constants.context_dir, context_filename), "w")
json_obj = json.dumps(context, cls=ContextLog_Encoder)
log_file.write(json_obj)
log_file.close()

