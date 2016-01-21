'''
Created on 26 Mar 2015

@author: quangv
'''
import parameters
from src.pygame_drawing.replication import Replication


""" two simulation mode -run with new sample, or replay mode"""

"""sample_num = 1
simulation_num = 1
parameters.scenarios['bottleneckunidirec'].run_aggregate(
                                                         sample_num,
                                                         simulation_num,
                                                         drawing=True,
                                                         parameter_distribution_plot=True,
                                                         observation_plot=True,
                                                         simulation_recording=True,
                                                         log_generation=True
                                                         );"""


"""replay function params: 0: run both, 1_prototype_different, 2_prototype_average """
""" pedestrian tracking feature only is supported in replication mode """

#group pedestrian left
#replication = Replication("898837_1")._replay(2) #people increase their speed

# 4 pedestrians left
replication = Replication("691620_1")._replay(2)

#3 pedestrians left
#replication = Replication("423792_1")._replay(2)

#2 pedestrians left
#replication = Replication("5428_1")._replay(2)

# 1 pedestrian left
#replication = Replication("898837_4")._replay(2) #people increase their speed

