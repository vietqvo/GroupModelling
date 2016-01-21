'''
Created on 26 Mar 2015

@author: quangv
'''
import parameters
import parameters_uni
from src.pygame_drawing.replication import Replication

sample_num = 1
simulation_num = 20
parameters.scenarios['bottleneckunidirec'].run_aggregate(
                                                         sample_num,
                                                         simulation_num,
                                                         parameter_distribution_plot=True,
                                                         simulation=True,
                                                         drawing=True,
                                                         observation_plot=True,
                                                         simulation_recording=True,
                                                         log_generation=True
                                                         )


"""parameters_uni.scenarios['bottleneckunidirec'].run_aggregate(
                                                         sample_num,
                                                         simulation_num,
                                                         parameter_distribution_plot=True,
                                                         simulation=True,
                                                         drawing=True,
                                                         observation_plot=True,
                                                         simulation_recording=True,
                                                         log_generation=True
                                                         )"""

#replay function params: 0: run both, 1_prototype_different, 2_prototype_average
#pedestrian tracking feature only is supported in replication mode


#simulationId = ["150257_3","150257_7","150257_10","574340_14","527190_15","527190_20","195247_7","195247_12","574340_8","814846_3","814846_4","814846_7","814846_13","835902_2","835902_20",
#                "125921_4","125921_19","1482_8","195247_13","125921_11","835902_19","135919_13","527190_6","527190_9","125921_9","195247_14","195247_16","150257_4","814846_6","135919_8",
#                "135919_14","195247_9","814846_16","150257_13","944359_2","835902_15","135919_10"]

#for i in range(len(simulationId)):
#    replication = Replication(simulationId[i])._replay() # 10 pedestrian LEFT #interaction force of d_p is higher than a_p

#replication = Replication("695860_18")._replay()