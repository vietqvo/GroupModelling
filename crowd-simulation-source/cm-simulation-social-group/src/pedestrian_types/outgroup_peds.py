'''
Created on 15 Sep 2015

@author: quangv
'''
from src import constants
import numpy
import json

class Outgroup_peds(object):
    def __init__(self, parameters= {}):
        self.parameters = parameters
     
        self._reset_outgroup_distribution()
    
    def _reset_outgroup_distribution(self):
        
        """ for the out-group normal distribution prototype """
        self.outgroup_desired_velocities = []
        self.outgroup_relaxation_times =[]
        self.outgroup_interaction_strengths = []
        self.outgroup_interaction_ranges =[]
             
      
    def _generate_outgroup_ped_normal_distribution(self, num):      
        if num ==0:
            return
        self._reset_outgroup_distribution()
        
        if self.parameters['outgroup_velocity_deviation'] > 0.0:
            while len(self.outgroup_desired_velocities) < num:
                samples = numpy.random.normal(self.parameters['outgroup_velocity_mean'], self.parameters['outgroup_velocity_deviation'], num)
                self.outgroup_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.outgroup_desired_velocities)))          
        else:
            self.outgroup_desired_velocities = [self.parameters['outgroup_velocity_mean']] * num
            
        if self.parameters['outgroup_relaxation_deviation'] > 0.0:    
            while len(self.outgroup_relaxation_times) < num:
                samples = numpy.random.normal(self.parameters['outgroup_relaxation_mean'], self.parameters['outgroup_relaxation_deviation'], num)
                self.outgroup_relaxation_times.extend(constants._filter_samples_by_mean(samples, num-len(self.outgroup_relaxation_times)))          
        else:
            self.outgroup_relaxation_times = [self.parameters['outgroup_relaxation_mean']] * num
               
        if self.parameters['outgroup_force_deviation'] > 0.0:    
            while len(self.outgroup_interaction_strengths) < num :
                samples = numpy.random.normal(self.parameters['outgroup_force_unit'], self.parameters['outgroup_force_deviation'], num)
                self.outgroup_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.outgroup_interaction_strengths)))          
        else:
            self.outgroup_interaction_strengths = [self.parameters['outgroup_force_unit']] * num
            
        if self.parameters['outgroup_range_deviation'] > 0.0:       
            while len(self.outgroup_interaction_ranges) < num:
                samples = numpy.random.normal(self.parameters['outgroup_force_range'], self.parameters['outgroup_range_deviation'], num)
                self.outgroup_interaction_ranges.extend(constants._filter_samples_by_mean(samples, num-len(self.outgroup_interaction_ranges)))          
        else:
            self.outgroup_interaction_ranges = [self.parameters['outgroup_force_range']] * num
            
    def _to_JSON(self):
        return  json.dumps(self, cls=OutGroup_Peds_Log_Encoder)

    def get_parameters(self):
        return self.parameters

    def get_outgroup_desired_velocities(self):
        return self.outgroup_desired_velocities


    def get_outgroup_relaxation_times(self):
        return self.outgroup_relaxation_times

    def get_outgroup_interaction_strengths(self):
        return self.outgroup_interaction_strengths


    def get_outgroup_interaction_ranges(self):
        return self.outgroup_interaction_ranges


    def set_parameters(self, value):
        self.parameters = value


    def set_outgroup_desired_velocities(self, value):
        self.outgroup_desired_velocities = value


    def set_outgroup_relaxation_times(self, value):
        self.outgroup_relaxation_times = value


    def set_outgroup_interaction_strengths(self, value):
        self.outgroup_interaction_strengths = value


    def set_outgroup_interaction_ranges(self, value):
        self.outgroup_interaction_ranges = value

    
class OutGroup_Peds_Log_Encoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Outgroup_peds):
            return super(OutGroup_Peds_Log_Encoder, self).default(obj)

        return obj.__dict__


class OutGroup_Peds_Log_Decoder(json.JSONDecoder):
    def decode(self,json_string):
     
        default_obj = super(OutGroup_Peds_Log_Decoder,self).decode(json_string)
        
        outgroup_desired_velocities = []
        for velocity in default_obj['outgroup_desired_velocities']:
            outgroup_desired_velocities.append(velocity)
        
        outgroup_relaxation_times = []
        for relaxation_time in default_obj['outgroup_relaxation_times']:
            outgroup_relaxation_times.append(relaxation_time)
        
        outgroup_interaction_strengths = []
        for interaction_strength in default_obj['outgroup_interaction_strengths']:
            outgroup_interaction_strengths.append(interaction_strength)
        
        outgroup_interaction_ranges = []
        for interaction_range in default_obj['outgroup_interaction_ranges']:
            outgroup_interaction_ranges.append(interaction_range)
   
        """ sharing parameters extraction"""
        parameter_data = default_obj['parameters']
  
        outgroup_peds_dist = Outgroup_peds()
        
        outgroup_peds_dist.set_parameters(parameter_data)
        
        outgroup_peds_dist.set_outgroup_desired_velocities(outgroup_desired_velocities)
        outgroup_peds_dist.set_outgroup_relaxation_times(outgroup_relaxation_times)
        outgroup_peds_dist.set_outgroup_interaction_strengths(outgroup_interaction_strengths)
        outgroup_peds_dist.set_outgroup_interaction_ranges(outgroup_interaction_ranges)
        
        return outgroup_peds_dist