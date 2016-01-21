'''
Created on 31 Mar 2015

@author: quangv
'''

import json

class Average(object):
    def __init__(self, total_num, desire_velocity_array, force_array,parameters= {}):
        self.parameters = parameters
     
        self._reset_average_distribution()
        
        self.average_desired_velocities = desire_velocity_array #self.parameters['average_velocity_mean']
        self.average_interaction_strengths = force_array#self.parameters['average_force_unit']

    def _reset_average_distribution(self):
        self.average_desired_velocities = []
        self.average_interaction_strengths = []
             
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
  
        average_dist = Average(len(average_desired_velocities),parameter_data)
        average_dist._set_average_desired_velocities_distribution(average_desired_velocities)  
        average_dist._set_average_interaction_strengths_distribution(average_interaction_strengths)
        average_dist._set_parameters(parameter_data)
        
        return average_dist