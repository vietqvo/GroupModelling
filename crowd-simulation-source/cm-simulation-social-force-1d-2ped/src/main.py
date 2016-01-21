'''
Created on 26 Mar 2015

@author: quangv
'''
import parameters
from src.pygame_drawing.replication import Replication

""" two simulation mode -run with new sample, or replay mode"""

simulation_num = 1
parameters.scenarios['bottleneckbiodirec'].run_aggregate(
                                                         simulation_num,
                                                         parameter_distribution_plot=True,
                                                         simulation=True,
                                                         drawing=True,
                                                         observation_plot=True,
                                                         simulation_recording=True,
                                                         log_generation=True
                                                         )

#replication = Replication("580516_13")._replay()