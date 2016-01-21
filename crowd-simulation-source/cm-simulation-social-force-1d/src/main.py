'''
Created on 26 Mar 2015

@author: quangv
'''
import parameters
import parameters_uni
from src.pygame_drawing.replication import Replication

""" two simulation mode -run with new sample, or replay mode"""

sample_num = 1
simulation_num = 1
parameters.scenarios['bottleneckbiodirec'].run_aggregate(
                                                         sample_num,
                                                         simulation_num,
                                                         distribution_average_prototype = "normal",
                                                         parameter_distribution_plot=True,
                                                         simulation=True,
                                                         drawing=True,
                                                         observation_plot=True,
                                                         simulation_recording=True,
                                                         log_generation=True
                                                         )

"""parameters_uni.scenarios['bottleneckbiodirec'].run_aggregate(
                                                         sample_num,
                                                         simulation_num,
                                                         distribution_average_prototype = "uniform",
                                                         parameter_distribution_plot=True,
                                                         simulation=True,
                                                         drawing=True,
                                                         observation_plot=True,
                                                         simulation_recording=True,
                                                         log_generation=True
                                                         )"""
                                                         
#replay function params: 0: run both, 1_prototype_different, 2_prototype_average
#pedestrian tracking feature only is supported in replication mode

#replication = Replication("725970_5")._replay() #bottle neck 
#replication = Replication("137775_12")._replay() #bottle neck 
#replication = Replication("137775_15")._replay() #bottle neck 
#replication = Replication("725373_8")._replay() #bottle neck 
#replication = Replication("725373_3")._replay() #bottle neck  
#replication = Replication("583481_18")._replay() #bottle neck 
#replication = Replication("555340_5")._replay() #bottle neck 
#replication = Replication("406438_6")._replay() #bottle neck
#replication = Replication("406438_2")._replay() #bottle neck 
 

#replication = Replication("725970_3")._replay() #go backward
#replication = Replication("137775_5")._replay() #go backward 
#replication = Replication("597706_9")._replay() #go backward 
#replication = Replication("625638_4")._replay(2)