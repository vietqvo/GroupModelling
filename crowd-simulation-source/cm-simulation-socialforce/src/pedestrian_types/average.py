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
        self.average_relaxation_times =[]
        self.average_interaction_strengths = []
        self.average_interaction_ranges =[]
             
    def _generate_average_distribution(self, mean_desired_velocity, std_desired_velocity,
                                       mean_relaxation_time, std_relaxation_time,
                                       mean_interaction_strength, std_interaction_strength,
                                       mean_interaction_range, std_interaction_range,
                                       num):      
        if num ==0:
            return
        self._reset_average_distribution()
        
        while len(self.average_desired_velocities) < num:
            samples = numpy.random.normal(mean_desired_velocity, std_desired_velocity, num*constants.max_samples)
            self.average_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.average_desired_velocities)))          
            
        while len(self.average_relaxation_times) < num:
            samples = numpy.random.normal(mean_relaxation_time, std_relaxation_time, num*constants.max_samples)
            self.average_relaxation_times.extend(constants._filter_samples_by_mean(samples, num-len(self.average_relaxation_times)))          
            
        while len(self.average_interaction_strengths) < num :
            samples = numpy.random.normal(mean_interaction_strength, std_interaction_strength, num*constants.max_samples)
            self.average_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.average_interaction_strengths)))          
            
        while len(self.average_interaction_ranges) < num:
            samples = numpy.random.normal(mean_interaction_range, std_interaction_range, num*constants.max_samples)
            self.average_interaction_ranges.extend(constants._filter_samples_by_mean(samples, num-len(self.average_interaction_ranges)))          
            
    def _set_average_desired_velocities_distribution(self,average_desired_velocities):
        self.average_desired_velocities=average_desired_velocities
    
    def _set_average_relaxation_times_distribution(self,average_relaxation_times):
        self.average_relaxation_times=average_relaxation_times
    
    def _set_average_interaction_strengths_distribution(self,average_interaction_strengths):
        self.average_interaction_strengths=average_interaction_strengths
    
    def _set_average_interaction_ranges_distribution(self,average_interaction_ranges):
        self.average_interaction_ranges=average_interaction_ranges
    
    def _set_parameters(self,parameters):         
        self.parameters = parameters
          
    def _get_average_desired_velocities_distribution(self):
        return self.average_desired_velocities
    
    def _get_average_relaxation_times_distribution(self):
        return self.average_relaxation_times
    
    def _get_average_interaction_strengths_distribution(self):
        return self.average_interaction_strengths
    
    def _get_average_interaction_ranges_distribution(self):
        return self.average_interaction_ranges
    
    def _get_parameters(self):
        return self.parameters
    
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
        
        average_relaxation_times = []
        for relaxation_time in default_obj['average_relaxation_times']:
            average_relaxation_times.append(relaxation_time)
        
        average_interaction_strengths = []
        for interaction_strength in default_obj['average_interaction_strengths']:
            average_interaction_strengths.append(interaction_strength)
        
        average_interaction_ranges = []
        for interaction_range in default_obj['average_interaction_ranges']:
            average_interaction_ranges.append(interaction_range)
        
        """ sharing parameters extraction"""
        
        parameter_data = default_obj['parameters']
  
        average_dist = Average()
        average_dist._set_average_desired_velocities_distribution(average_desired_velocities)  
        average_dist._set_average_relaxation_times_distribution(average_relaxation_times) 
        average_dist._set_average_interaction_strengths_distribution(average_interaction_strengths)
        average_dist._set_average_interaction_ranges_distribution(average_interaction_ranges)
        average_dist._set_parameters(parameter_data)
        
        return average_dist