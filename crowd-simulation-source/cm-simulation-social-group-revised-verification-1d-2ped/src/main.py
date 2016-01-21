'''
Created on 14 Sep 2015

@author: quangv
'''
import parameters
from src.utility.context import ContextGenerator as context_generator

monte_carlos_simulation = parameters.scenarios['corridorunidirec']

context = context_generator(monte_carlos_simulation._get_parameters())
group_num = monte_carlos_simulation._get_parameters()['group_num']

monte_carlos_simulation.run_aggregate(context,simulation=True,drawing=True)

    
