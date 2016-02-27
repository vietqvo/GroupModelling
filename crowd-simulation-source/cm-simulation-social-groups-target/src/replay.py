'''
Created on 29 Sep 2015

@author: quangv
'''

import parameters
from src.utility.context import ContextLog_Decoder 
import os, json
from src import constants

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

context_log_file = open( "%s.json" % os.path.join(constants.context_dir, "context_10"))
json_str = context_log_file.read()
context=  json.loads(json_str, cls =ContextLog_Decoder)

        
total_group_num = 4

v_param = [(1.03234575791284),(1.03234575791284),(1.03234575791284),(1.03234575791284)]
re_param =[(0.646143445558846),(0.646143445558846),(0.646143445558846),(0.646143445558846)]         
rep_s_param = [(2.8077242190484),(2.8077242190484),(2.8077242190484),(2.8077242190484)]
rep_ra_param =  [(0.2884617725387),(0.5884617725387),(0.5884617725387),(0.5884617725387)]
att_s_param = [(0.645807707565837),(0.645807707565837),(0.645807707565837),(0.645807707565837)]
att_ra_param =  [(0.812806584872305),(0.812806584872305),(0.812806584872305),(0.812806584872305)]
        
monte_carlos_simulation.run_aggregate(total_group_num,
                                      v_param, re_param,
                                      rep_s_param, rep_ra_param,
                                      att_s_param, att_ra_param, 
                                      context, simulation=True, drawing=True)
