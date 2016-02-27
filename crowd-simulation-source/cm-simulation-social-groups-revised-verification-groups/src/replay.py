import parameters
from src.utility.context import ContextLog_Decoder 
import os, json
from src import constants
import math as m

monte_carlos_simulation = parameters.scenarios['corridorunidirec']
context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)

in_group_r_strength =40  
in_group_r_range = 2.0
in_group_a_strength = 20
in_group_a_range = 2.8

c = 2.0

out_group_r_strength = in_group_r_strength * c
out_group_r_range = in_group_r_range
out_group_a_strength = in_group_a_strength * (1/c)
out_group_a_range = in_group_a_range 

if (out_group_r_strength * m.pow(out_group_r_range,2) >    out_group_a_strength * m.pow(out_group_a_range,2)) and (out_group_r_strength > out_group_a_strength) and (out_group_a_range > out_group_r_range) :
 
    monte_carlos_simulation.run_aggregate(in_group_a_strength, in_group_a_range,
                                      in_group_r_strength, in_group_r_range,
                                      out_group_a_strength, out_group_a_range, 
                                      out_group_r_strength, out_group_r_range,
                                      context, simulation=True, drawing=True)
else:
    print("Constraint unsatisfied")
           
