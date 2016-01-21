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
        self.elderly_interaction_strengths = []
             
    def _generate_elderly_distribution(self,num):
        
        if num ==0:
            return
        self._reset_elderly_distribution()
        
        if self.parameters['elderly_velocity_deviation'] > 0.0:
            while len(self.elderly_desired_velocities) < num:
                samples = numpy.random.normal(self.parameters['elderly_velocity_mean'], self.parameters['elderly_velocity_deviation'], num)
                self.elderly_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.elderly_desired_velocities)))
        else:
            self.elderly_desired_velocities = [self.parameters['elderly_velocity_mean']] * num
                
        if self.parameters['elderly_force_deviation'] > 0.0:
            while len(self.elderly_interaction_strengths) < num:    
                samples =  numpy.random.normal(self.parameters['elderly_force_unit'], self.parameters['elderly_force_deviation'], num)
                self.elderly_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.elderly_interaction_strengths)))
        else:
            self.elderly_interaction_strengths = [self.parameters['elderly_force_unit']] * num
        
    def _set_elderly_desired_velocities_distribution(self,elderly_desired_velocities):
        self.elderly_desired_velocities=elderly_desired_velocities
    
    def _set_elderly_interaction_strengths_distribution(self,elderly_interaction_strengths):
        self.elderly_interaction_strengths=elderly_interaction_strengths
    
    def _get_elderly_desired_velocities_distribution(self):
        return self.elderly_desired_velocities
    
    def _get_elderly_interaction_strengths_distribution(self):
        return self.elderly_interaction_strengths
    
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
        
        elderly_interaction_strengths = []
        for interaction_strength in default_obj['elderly_interaction_strengths']:
            elderly_interaction_strengths.append(interaction_strength)
        
        elderly_dist = Elderly()
        elderly_dist._set_elderly_desired_velocities_distribution(elderly_desired_velocities)  
        elderly_dist._set_elderly_interaction_strengths_distribution(elderly_interaction_strengths)

        return elderly_dist       
