'''
Created on 31 Mar 2015

@author: quangv
'''
from src import constants
import numpy
import json

class Children(object):
    def __init__(self, parameters= {}):
        self.parameters = parameters
     
        self._reset_children_distribution()
    
    def _reset_children_distribution(self):
        self.children_desired_velocities = []
        self.children_relaxation_times =[]
        self.children_interaction_strengths = []
        self.children_interaction_ranges =[]
             
    def _generate_children_distribution(self,num,children_velocity_mean = 0.0,
                                                 children_relaxation_mean = 0.0,
                                                 children_interaction_strength_mean = 0.0,
                                                 children_interaction_range_mean = 0.0):
        
        if num ==0:
            return
        self._reset_children_distribution()
                 
        if self.parameters['children_group_velocity_deviation']> 0.0:
            while len(self.children_desired_velocities) < num:
                samples = numpy.random.normal(children_velocity_mean, self.parameters['children_group_velocity_deviation'], num)
                self.children_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.children_desired_velocities)))
        else:
                self.children_desired_velocities = [children_velocity_mean] * num
            
        if self.parameters['children_group_relaxation_deviation'] > 0.0:
            while len(self.children_relaxation_times) < num:   
                samples = numpy.random.normal(children_relaxation_mean, self.parameters['children_group_relaxation_deviation'], num)
                self.children_relaxation_times.extend(constants._filter_samples_by_mean(samples, num-len(self.children_relaxation_times)))
        else:
                self.children_relaxation_times = [children_relaxation_mean] * num
            
        if self.parameters['children_group_force_deviation'] > 0.0: 
            while len(self.children_interaction_strengths) < num:      
                samples =  numpy.random.normal(children_interaction_strength_mean, self.parameters['children_group_force_deviation'], num)
                self.children_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.children_interaction_strengths)))
        else:
                self.children_interaction_strengths = [children_interaction_strength_mean] * num
            
        if self.parameters['children_group_range_deviation'] > 0.0:
            while len(self.children_interaction_ranges)< num:        
                samples = numpy.random.normal(children_interaction_range_mean, self.parameters['children_group_range_deviation'], num)
                self.children_interaction_ranges.extend(constants._filter_samples_by_mean(samples, num-len(self.children_interaction_ranges)))
        else:
                self.children_interaction_ranges = [children_interaction_range_mean] * num
    
    def _set_children_desired_velocities_distribution(self,children_desired_velocities):
        self.children_desired_velocities=children_desired_velocities
    
    def _set_children_relaxation_times_distribution(self,children_relaxation_times):
        self.children_relaxation_times=children_relaxation_times
    
    def _set_children_interaction_strengths_distribution(self,children_interaction_strengths):
        self.children_interaction_strengths = children_interaction_strengths
    
    def _set_children_interaction_ranges_distribution(self,children_interaction_ranges):
        self.children_interaction_ranges=children_interaction_ranges
                
    def _get_children_desired_velocities_distribution(self):
        return self.children_desired_velocities
    
    def _get_children_relaxation_times_distribution(self):
        return self.children_relaxation_times
    
    def _get_children_interaction_strengths_distribution(self):
        return self.children_interaction_strengths
    
    def _get_children_interaction_ranges_distribution(self):
        return self.children_interaction_ranges
    
    def _to_JSON(self):
        return  json.dumps(self, cls=ChildrenLog_Encoder)
    
class ChildrenLog_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Children):
            return super(ChildrenLog_Encoder, self).default(obj)

        return obj.__dict__

class ChildrenLog_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(ChildrenLog_Decoder,self).decode(json_string)
        
        children_desired_velocities = []
        for velocity in default_obj['children_desired_velocities']:
            children_desired_velocities.append(velocity)
        
        children_relaxation_times = []
        for relaxation_time in default_obj['children_relaxation_times']:
            children_relaxation_times.append(relaxation_time)
        
        children_interaction_strengths = []
        for interaction_strength in default_obj['children_interaction_strengths']:
            children_interaction_strengths.append(interaction_strength)
        
        children_interaction_ranges = []
        for interaction_range in default_obj['children_interaction_ranges']:
            children_interaction_ranges.append(interaction_range)
        
        children_dist = Children()
        children_dist._set_children_desired_velocities_distribution(children_desired_velocities)  
        children_dist._set_children_relaxation_times_distribution(children_relaxation_times) 
        children_dist._set_children_interaction_strengths_distribution(children_interaction_strengths)
        children_dist._set_children_interaction_ranges_distribution(children_interaction_ranges)
        
        return children_dist