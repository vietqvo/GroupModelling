'''
Created on 31 Mar 2015

@author: quangv
'''
from src import constants
import numpy
import json

class Elderly(object):
    def __init__(self, parameters= {}):
        self.parameters = parameters
     
        self._reset_elderly_distribution()
    
    def _reset_elderly_distribution(self):
        self.elderly_desired_velocities = []
        self.elderly_relaxation_times =[]
        self.elderly_interaction_strengths = []
        self.elderly_interaction_ranges =[]
             
    def _generate_elderly_distribution(self,num):
        
        if num ==0:
            return
        self._reset_elderly_distribution()
        
        if self.parameters['elderly_group_velocity_deviation'] > 0.0:
            while len(self.elderly_desired_velocities) < num:
                samples = numpy.random.normal(self.parameters['elderly_group_velocity_mean'], self.parameters['elderly_group_velocity_deviation'], num)
                self.elderly_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.elderly_desired_velocities)))
        else:
            self.elderly_desired_velocities = [self.parameters['elderly_group_velocity_mean']] * num
            
        if self.parameters['elderly_group_relaxation_deviation'] > 0.0:    
            while len(self.elderly_relaxation_times) < num:
                samples = numpy.random.normal(self.parameters['elderly_group_relaxation_mean'], self.parameters['elderly_group_relaxation_deviation'], num)
                self.elderly_relaxation_times.extend(constants._filter_samples_by_mean(samples, num-len(self.elderly_relaxation_times)))
        else:
            self.elderly_relaxation_times = [self.parameters['elderly_group_relaxation_mean']] * num
            
        if self.parameters['elderly_group_force_deviation'] > 0.0:
            while len(self.elderly_interaction_strengths) < num:    
                samples =  numpy.random.normal(self.parameters['elderly_group_force_unit'], self.parameters['elderly_group_force_deviation'], num)
                self.elderly_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.elderly_interaction_strengths)))
        else:
            self.elderly_interaction_strengths = [self.parameters['elderly_group_force_unit']] * num
            
        if self.parameters['elderly_group_range_deviation'] > 0.0:
            while len(self.elderly_interaction_ranges) < num:
                samples = numpy.random.normal(self.parameters['elderly_group_force_range'], self.parameters['elderly_group_range_deviation'], num)
                self.elderly_interaction_ranges.extend(constants._filter_samples_by_mean(samples, num-len(self.elderly_interaction_ranges)))
        else:
            self.elderly_interaction_ranges = [self.parameters['elderly_group_force_range']] * num
    
    def _set_elderly_desired_velocities_distribution(self,elderly_desired_velocities):
        self.elderly_desired_velocities=elderly_desired_velocities
    
    def _set_elderly_relaxation_times_distribution(self,elderly_relaxation_times):
        self.elderly_relaxation_times=elderly_relaxation_times
    
    def _set_elderly_interaction_strengths_distribution(self,elderly_interaction_strengths):
        self.elderly_interaction_strengths=elderly_interaction_strengths
    
    def _set_elderly_interaction_ranges_distribution(self,elderly_interaction_ranges):
        self.elderly_interaction_ranges= elderly_interaction_ranges
       
    def _get_elderly_desired_velocities_distribution(self):
        return self.elderly_desired_velocities
    
    def _get_elderly_relaxation_times_distribution(self):
        return self.elderly_relaxation_times
    
    def _get_elderly_interaction_strengths_distribution(self):
        return self.elderly_interaction_strengths
    
    def _get_elderly_interaction_ranges_distribution(self):
        return self.elderly_interaction_ranges
    
    def _to_JSON(self):
        return  json.dumps(self, cls=ElderlyLog_Encoder)
    
class ElderlyLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Elderly):
            return super(ElderlyLog_Encoder, self).default(obj)

        return obj.__dict__

class ElderlyLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(ElderlyLog_Decoder,self).decode(json_string)
        
        elderly_desired_velocities = []
        for velocity in default_obj['elderly_desired_velocities']:
            elderly_desired_velocities.append(velocity)
        
        elderly_relaxation_times = []
        for relaxation_time in default_obj['elderly_relaxation_times']:
            elderly_relaxation_times.append(relaxation_time)
        
        elderly_interaction_strengths = []
        for interaction_strength in default_obj['elderly_interaction_strengths']:
            elderly_interaction_strengths.append(interaction_strength)
        
        elderly_interaction_ranges = []
        for interaction_range in default_obj['elderly_interaction_ranges']:
            elderly_interaction_ranges.append(interaction_range)
        
        elderly_dist = Elderly()
        elderly_dist._set_elderly_desired_velocities_distribution(elderly_desired_velocities)  
        elderly_dist._set_elderly_relaxation_times_distribution(elderly_relaxation_times) 
        elderly_dist._set_elderly_interaction_strengths_distribution(elderly_interaction_strengths)
        elderly_dist._set_elderly_interaction_ranges_distribution(elderly_interaction_ranges)
        
        return elderly_dist       
