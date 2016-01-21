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
        self.children_interaction_strengths = []
             
    def _generate_children_distribution(self,num):
        
        if num ==0:
            return
        self._reset_children_distribution()
        
        if self.parameters['young_velocity_deviation'] > 0.0:
            while len(self.children_desired_velocities) < num:
                samples = numpy.random.normal(self.parameters['young_velocity_mean'], self.parameters['young_velocity_deviation'], num)
                self.children_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.children_desired_velocities)))
        else:
                self.children_desired_velocities = [self.parameters['young_velocity_mean']] * num
            
        if self.parameters['young_force_deviation'] > 0.0: 
            while len(self.children_interaction_strengths) < num:      
                samples =  numpy.random.normal(self.parameters['young_force_unit'], self.parameters['young_force_deviation'], num)
                self.children_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.children_interaction_strengths)))
        else:
                self.children_interaction_strengths = [self.parameters['young_force_unit']] * num
   
    
    def _set_children_desired_velocities_distribution(self,children_desired_velocities):
        self.children_desired_velocities=children_desired_velocities
    
    def _set_children_interaction_strengths_distribution(self,children_interaction_strengths):
        self.children_interaction_strengths = children_interaction_strengths
    
    def _get_children_desired_velocities_distribution(self):
        return self.children_desired_velocities
    
    def _get_children_interaction_strengths_distribution(self):
        return self.children_interaction_strengths
    
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
        
         
        children_interaction_strengths = []
        for interaction_strength in default_obj['children_interaction_strengths']:
            children_interaction_strengths.append(interaction_strength)
        
        children_dist = Children()
        children_dist._set_children_desired_velocities_distribution(children_desired_velocities)  
        children_dist._set_children_interaction_strengths_distribution(children_interaction_strengths)
        
        return children_dist