'''
Created on 26 Mar 2015

@author: quangv
'''
import parameters
from src.pygame_drawing.replication import Replication

""" two simulation mode -run with new sample, or replay mode"""


experiment= []

experiment.append(dict(average_velocity_mean= [1.6,0.8],average_force_unit =[2.0,10.0]))

experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[2.0,4.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[2.0,6.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[2.0,8.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[2.0,10.0]))

experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[2.0,4.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[2.0,6.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[2.0,8.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[2.0,10.0]))

experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[2.0,4.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[2.0,6.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[2.0,8.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[2.0,10.0]))
            

#################################################################################################
experiment.append(dict(average_velocity_mean= [0.8,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [0.8,0.8],average_force_unit =[4.0,2.0]))
experiment.append(dict(average_velocity_mean= [0.8,0.8],average_force_unit =[6.0,2.0]))
experiment.append(dict(average_velocity_mean= [0.8,0.8],average_force_unit =[8.0,2.0]))
experiment.append(dict(average_velocity_mean= [0.8,0.8],average_force_unit =[10.0,2.0]))

experiment.append(dict(average_velocity_mean= [1.6,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [1.6,0.8],average_force_unit =[4.0,2.0]))
experiment.append(dict(average_velocity_mean= [1.6,0.8],average_force_unit =[6.0,2.0]))
experiment.append(dict(average_velocity_mean= [1.6,0.8],average_force_unit =[8.0,2.0]))
experiment.append(dict(average_velocity_mean= [1.6,0.8],average_force_unit =[10.0,2.0]))

experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[4.0,2.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[6.0,2.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[8.0,2.0]))
experiment.append(dict(average_velocity_mean= [2.4,0.8],average_force_unit =[10.0,2.0]))

experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[4.0,2.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[6.0,2.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[8.0,2.0]))
experiment.append(dict(average_velocity_mean= [3.2,0.8],average_force_unit =[10.0,2.0]))

experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[2.0,2.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[4.0,2.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[6.0,2.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[8.0,2.0]))
experiment.append(dict(average_velocity_mean= [4.0,0.8],average_force_unit =[10.0,2.0]))


simulation_num = 50
for i in range(len(experiment)):
    average_velocity_mean= experiment[i]["average_velocity_mean"]  
    average_force_unit = experiment[i]["average_force_unit"]             

    parameters.scenarios['bottleneckbiodirec'].run_aggregate(i,
                                                         average_velocity_mean,
                                                         average_force_unit,   
                                                         simulation_num,
                                                         parameter_distribution_plot=True,
                                                         simulation=True,
                                                         drawing=True,
                                                         observation_plot=True,
                                                         simulation_recording=True,
                                                         log_generation=True
                                                         )

#replication = Replication("452896_1")._replay()