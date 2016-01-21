'''
Created on 31 Mar 2015

@author: quangv
'''
from src import constants
import numpy
import json

class Adults(object):
    def __init__(self, parameters= {}):
        self.parameters = parameters
     
        self._reset_adults_distribution()
    
    def _reset_adults_distribution(self):
        self.adults_desired_velocities = []
        self.adults_relaxation_times =[]
        self.adults_interaction_strengths = []
        self.adults_interaction_ranges =[]
             
    def _generate_adults_distribution(self,num):
        
        if num ==0:
            return
        self._reset_adults_distribution()
        
        if self.parameters['adult_velocity_deviation'] > 0.0:
            while len(self.adults_desired_velocities) < num:
                samples = numpy.random.normal(self.parameters['adult_velocity_mean'], self.parameters['adult_velocity_deviation'], num*constants.max_samples)
                self.adults_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.adults_desired_velocities)))   
        else:
            self.adults_desired_velocities = [self.parameters['adult_velocity_mean']] * num
            
        if self.parameters['adult_relaxation_deviation'] > 0.0:
            while len(self.adults_relaxation_times) < num:  
                samples = numpy.random.normal(self.parameters['adult_relaxation_mean'], self.parameters['adult_relaxation_deviation'], num*constants.max_samples)
                self.adults_relaxation_times.extend(constants._filter_samples_by_mean(samples, num-len(self.adults_relaxation_times)))
        else:
            self.adults_relaxation_times = [self.parameters['adult_relaxation_mean']] * num
            
        if self.parameters['adult_force_deviation'] > 0.0:
            while len(self.adults_interaction_strengths) < num:        
                samples =  numpy.random.normal(self.parameters['adult_force_unit'], self.parameters['adult_force_deviation'], num*constants.max_samples)
                self.adults_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.adults_interaction_strengths)))
        else:
            self.adults_interaction_strengths = [self.parameters['adult_force_unit']] * num
            
        if self.parameters['adult_range_deviation'] > 0.0:
            while len(self.adults_interaction_ranges) < num:
                samples = numpy.random.normal(self.parameters['adult_force_range'], self.parameters['adult_range_deviation'], num*constants.max_samples)
                self.adults_interaction_ranges.extend(constants._filter_samples_by_mean(samples, num-len(self.adults_interaction_ranges)))
        else:
            self.adults_interaction_ranges =  [self.parameters['adult_force_range']] * num
        
    
    def _set_adults_desired_velocities_distribution(self,adults_desired_velocities):
        self.adults_desired_velocities = adults_desired_velocities
    
    def _set_adults_relaxation_times_distribution(self,adults_relaxation_times):
        self.adults_relaxation_times = adults_relaxation_times
    
    def _set_adults_interaction_strengths_distribution(self,adults_interaction_strengths):
        self.adults_interaction_strengths = adults_interaction_strengths
    
    def _set_adults_interaction_ranges_distribution(self,adults_interaction_ranges):
        self.adults_interaction_ranges = adults_interaction_ranges
                
    def _get_adults_desired_velocities_distribution(self):
        return self.adults_desired_velocities
    
    def _get_adults_relaxation_times_distribution(self):
        return self.adults_relaxation_times
    
    def _get_adults_interaction_strengths_distribution(self):
        return self.adults_interaction_strengths
    
    def _get_adults_interaction_ranges_distribution(self):
        return self.adults_interaction_ranges
    
    def _to_JSON(self):
        return  json.dumps(self, cls=AdultLog_Encoder)
    
class AdultLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Adults):
            return super(AdultLog_Encoder, self).default(obj)

        return obj.__dict__

class AdultLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(AdultLog_Decoder,self).decode(json_string)
        
        adults_desired_velocities = []
        for velocity in default_obj['adults_desired_velocities']:
            adults_desired_velocities.append(velocity)
        
        adults_relaxation_times = []
        for relaxation_time in default_obj['adults_relaxation_times']:
            adults_relaxation_times.append(relaxation_time)
        
        adults_interaction_strengths = []
        for interaction_strength in default_obj['adults_interaction_strengths']:
            adults_interaction_strengths.append(interaction_strength)
        
        adults_interaction_ranges = []
        for interaction_range in default_obj['adults_interaction_ranges']:
            adults_interaction_ranges.append(interaction_range)
        
        adult_dist = Adults()
        adult_dist._set_adults_desired_velocities_distribution(adults_desired_velocities)  
        adult_dist._set_adults_relaxation_times_distribution(adults_relaxation_times) 
        adult_dist._set_adults_interaction_strengths_distribution(adults_interaction_strengths)
        adult_dist._set_adults_interaction_ranges_distribution(adults_interaction_ranges)
        
        return adult_dist
        