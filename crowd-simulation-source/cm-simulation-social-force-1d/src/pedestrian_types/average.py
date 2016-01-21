'''
Created on 31 Mar 2015

@author: quangv
'''
from src import constants
import numpy
import json

class Average(object):
    def __init__(self, parameters= {}):
        self.parameters = parameters
     
        self._reset_average_distribution()
    
    def _reset_average_distribution(self):
        self.average_desired_velocities = []
        self.average_interaction_strengths = []
             
    def _generate_average_normal_distribution(self, mean_desired_velocity, std_desired_velocity,
                                       mean_interaction_strength, std_interaction_strength,
                                       num):      
        if num ==0:
            return
        self._reset_average_distribution()
        
        while len(self.average_desired_velocities) < num:
            samples = numpy.random.normal(mean_desired_velocity, std_desired_velocity, num)
            self.average_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.average_desired_velocities)))          
            
            
        while len(self.average_interaction_strengths) < num :
            samples = numpy.random.normal(mean_interaction_strength, std_interaction_strength, num)
            self.average_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.average_interaction_strengths)))          
            
       
    def _generate_average_uniform_distribution(self, 
                                                mean_children_desired_velocity,
                                                mean_elder_desired_velocity,                                             
                                             
                                                mean_children_interaction_strength,                                           
                                                mean_elder_interaction_strength,
                                                  
                                                num):      
        if num ==0:
            return
        self._reset_average_distribution()
        
        # we choose the minimum and maximum of each parameter
        # since the standard deviation is equal for each prototype, we get 2*SD and cutoff with 5% of maximum and minimum mean values
        # let the minimum and maximum value cuff off by above value 
        # calculate uniform in this range
        
        ################ for desired velocity ######################
        min_desired_velocity_value = min(mean_children_desired_velocity, mean_elder_desired_velocity)   
        max_desired_velocity_value = max(mean_children_desired_velocity, mean_elder_desired_velocity)
        
        self.velocity_min_uniform = min_desired_velocity_value - 2* self.parameters['young_velocity_deviation'] 
        self.velocity_max_uniform = max_desired_velocity_value + 2*self.parameters['young_velocity_deviation'] 
        
        while len(self.average_desired_velocities) < num:
            samples = numpy.random.uniform(self.velocity_min_uniform, self.velocity_max_uniform, num)
            self.average_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.average_desired_velocities)))          
            
        ################ for interaction strength ######################
        min_interaction_strength_value = min(mean_children_interaction_strength, mean_elder_interaction_strength)   
        max_interaction_strength_value = max(mean_children_interaction_strength, mean_elder_interaction_strength)
        
        self.interaction_strength_min_uniform = min_interaction_strength_value - 2* self.parameters['young_force_deviation']    
        self.interaction_strength_max_uniform = max_interaction_strength_value + 2*self.parameters['young_force_deviation']
        
        
        while len(self.average_interaction_strengths) < num :
            samples = numpy.random.uniform(self.interaction_strength_min_uniform, self.interaction_strength_max_uniform, num)
            self.average_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.average_interaction_strengths)))          
                             
    def _set_average_desired_velocities_distribution(self,average_desired_velocities):
        self.average_desired_velocities=average_desired_velocities
     
    def _set_average_interaction_strengths_distribution(self,average_interaction_strengths):
        self.average_interaction_strengths=average_interaction_strengths
    
    def _set_parameters(self,parameters):         
        self.parameters = parameters
          
    def _get_average_desired_velocities_distribution(self):
        return self.average_desired_velocities
    
    def _get_average_interaction_strengths_distribution(self):
        return self.average_interaction_strengths
     
    def _get_parameters(self):
        return self.parameters
    
    def _get_velocity_min_uniform(self):
        return self.velocity_min_uniform
    
    def _get_velocity_max_uniform(self):
        return self.velocity_max_uniform
    
    def _get_interaction_strength_min_uniform(self):
        return self.interaction_strength_min_uniform
    
    def _get_interaction_strength_max_uniform(self):
        return self.interaction_strength_max_uniform
      
    def _to_JSON(self):
        return  json.dumps(self, cls=AverageLog_Encoder)
    
class AverageLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Average):
            return super(AverageLog_Encoder, self).default(obj)

        return obj.__dict__

class AverageLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(AverageLog_Decoder,self).decode(json_string)
        
        average_desired_velocities = []
        for velocity in default_obj['average_desired_velocities']:
            average_desired_velocities.append(velocity)
        
        average_interaction_strengths = []
        for interaction_strength in default_obj['average_interaction_strengths']:
            average_interaction_strengths.append(interaction_strength)
        
        """ sharing parameters extraction"""
        
        parameter_data = default_obj['parameters']
  
        average_dist = Average()
        average_dist._set_average_desired_velocities_distribution(average_desired_velocities)  
        average_dist._set_average_interaction_strengths_distribution(average_interaction_strengths)
        average_dist._set_parameters(parameter_data)
        
        return average_dist