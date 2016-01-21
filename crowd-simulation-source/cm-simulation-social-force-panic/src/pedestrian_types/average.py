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
        
        """ for the average normal distribution prototype """
        self.average_desired_velocities = []
        self.average_relaxation_times =[]
        self.average_interaction_strengths = []
        self.average_interaction_ranges =[]
             
        """ for the average cutoff level 3 normal distribution prototype """
        self.average_cutoff_lv3_desired_velocities = []
        self.average_cutoff_lv3_desired_velocities_low_value = 0.0
        self.average_cutoff_lv3_desired_velocities_high_value = 0.0
        
        self.average_cutoff_lv3_relaxation_times =[]
        self.average_cutoff_lv3_relaxation_times_low_value = 0.0
        self.average_cutoff_lv3_relaxation_times_high_value = 0.0
        
        self.average_cutoff_lv3_interaction_strengths = []
        self.average_cutoff_lv3_interaction_strengths_low_value = 0.0
        self.average_cutoff_lv3_interaction_strengths_high_value = 0.0
        
        self.average_cutoff_lv3_interaction_ranges =[]
        self.average_cutoff_lv3_interaction_ranges_low_value = 0.0
        self.average_cutoff_lv3_interaction_ranges_high_value = 0.0
             
        """ for the average cutoff level 1 normal distribution prototype """
        self.average_cutoff_lv1_desired_velocities = []
        self.average_cutoff_lv1_desired_velocities_low_value = 0.0
        self.average_cutoff_lv1_desired_velocities_high_value = 0.0
      
        self.average_cutoff_lv1_relaxation_times =[]
        self.average_cutoff_lv1_relaxation_times_low_value = 0.0
        self.average_cutoff_lv1_relaxation_times_high_value = 0.0
        
        self.average_cutoff_lv1_interaction_strengths = []
        self.average_cutoff_lv1_interaction_strengths_low_value = 0.0
        self.average_cutoff_lv1_interaction_strengths_high_value = 0.0
        
        self.average_cutoff_lv1_interaction_ranges =[]
        self.average_cutoff_lv1_interaction_ranges_low_value = 0.0
        self.average_cutoff_lv1_interaction_ranges_high_value = 0.0
        
        
        """ for the uniform cutoff level 3 distribution prototype """
        self.uniform_cutoff_lv3_desired_velocities = []
        self.uniform_cutoff_lv3_desired_velocities_low_value = 0.0
        self.uniform_cutoff_lv3_desired_velocities_high_value = 0.0
      
        self.uniform_cutoff_lv3_relaxation_times =[]
        self.uniform_cutoff_lv3_relaxation_times_low_value = 0.0
        self.uniform_cutoff_lv3_relaxation_times_high_value = 0.0
        
        self.uniform_cutoff_lv3_interaction_strengths = []
        self.uniform_cutoff_lv3_interaction_strengths_low_value = 0.0
        self.uniform_cutoff_lv3_interaction_strengths_high_value = 0.0
        
        self.uniform_cutoff_lv3_interaction_ranges =[]
        self.uniform_cutoff_lv3_interaction_ranges_low_value = 0.0
        self.uniform_cutoff_lv3_interaction_ranges_high_value = 0.0
         
        """ for the uniform cutoff level 1 distribution prototype """
        self.uniform_cutoff_lv1_desired_velocities = []
        self.uniform_cutoff_lv1_desired_velocities_low_value = 0.0
        self.uniform_cutoff_lv1_desired_velocities_high_value = 0.0
      
        self.uniform_cutoff_lv1_relaxation_times =[]
        self.uniform_cutoff_lv1_relaxation_times_low_value = 0.0
        self.uniform_cutoff_lv1_relaxation_times_high_value = 0.0
        
        self.uniform_cutoff_lv1_interaction_strengths = []
        self.uniform_cutoff_lv1_interaction_strengths_low_value = 0.0
        self.uniform_cutoff_lv1_interaction_strengths_high_value = 0.0
        
        self.uniform_cutoff_lv1_interaction_ranges =[]
        self.uniform_cutoff_lv1_interaction_ranges_low_value = 0.0
        self.uniform_cutoff_lv1_interaction_ranges_high_value = 0.0
                  
    def _generate_average_normal_distribution(self, mean_desired_velocity, std_desired_velocity,
                                       mean_relaxation_time, std_relaxation_time,
                                       mean_interaction_strength, std_interaction_strength,
                                       mean_interaction_range, std_interaction_range,
                                       num):      
        if num ==0:
            return
        self._reset_average_distribution()
        
        while len(self.average_desired_velocities) < num:
            samples = numpy.random.normal(mean_desired_velocity, std_desired_velocity, num)
            self.average_desired_velocities.extend(constants._filter_samples_by_mean(samples, num-len(self.average_desired_velocities)))          
            
        while len(self.average_relaxation_times) < num:
            samples = numpy.random.normal(mean_relaxation_time, std_relaxation_time, num)
            self.average_relaxation_times.extend(constants._filter_samples_by_mean(samples, num-len(self.average_relaxation_times)))          
            
        while len(self.average_interaction_strengths) < num :
            samples = numpy.random.normal(mean_interaction_strength, std_interaction_strength, num)
            self.average_interaction_strengths.extend(constants._filter_samples_by_mean(samples, num-len(self.average_interaction_strengths)))          
            
        while len(self.average_interaction_ranges) < num:
            samples = numpy.random.normal(mean_interaction_range, std_interaction_range, num)
            self.average_interaction_ranges.extend(constants._filter_samples_by_mean(samples, num-len(self.average_interaction_ranges)))          
    
    
    def _generate_average_cutoff_level_normal_distribution(self, 
                                    mean_desired_velocity, std_desired_velocity,                       
                                    min_desired_velocity_value,max_desired_velocity_value,
                                    
                                    mean_relaxation_time, std_relaxation_time,
                                    min_relaxation_time_value,max_relaxation_time_value,                                                                            
                                    
                                    mean_interaction_strength, std_interaction_strength,
                                    min_interaction_strength_value, max_interaction_strength_value,                                                       
                                    
                                    mean_interaction_range, std_interaction_range,
                                    min_interaction_range_value,max_interaction_range_value,
                                    
                                    num, level):    
                                                                                     
        if num ==0 or len(self.average_desired_velocities) == 0:
            return
        
        """ for desired velocity parameter"""
        cut_off_low_value_desired_velocity = min_desired_velocity_value - level* self.parameters['young_velocity_deviation'] 
        cut_off_high_value_desired_velocity = max_desired_velocity_value + level* self.parameters['young_velocity_deviation']
        
        cut_off_desired_velocities = [item for item in self.average_desired_velocities if (item>= cut_off_low_value_desired_velocity and item <= cut_off_high_value_desired_velocity)]  
        while len(cut_off_desired_velocities) < num:
            samples = numpy.random.normal(mean_desired_velocity, std_desired_velocity, num-(len(cut_off_desired_velocities)))
            refined_samples = [item for item in samples if (item>= cut_off_low_value_desired_velocity and item <= cut_off_high_value_desired_velocity)]  
            cut_off_desired_velocities.extend(refined_samples)          
         
        if level ==3:       
            self.average_cutoff_lv3_desired_velocities = cut_off_desired_velocities
            self.average_cutoff_lv3_desired_velocities_low_value = cut_off_low_value_desired_velocity
            self.average_cutoff_lv3_desired_velocities_high_value = cut_off_high_value_desired_velocity
        
        elif level ==1:
            self.average_cutoff_lv1_desired_velocities = cut_off_desired_velocities
            self.average_cutoff_lv1_desired_velocities_low_value = cut_off_low_value_desired_velocity
            self.average_cutoff_lv1_desired_velocities_high_value = cut_off_high_value_desired_velocity
      
        #print("compute min desired velocity %s level- %s" % (level,min(cut_off_desired_velocities)))
        #print("compute max desired velocity %s level- %s" % (level, max(cut_off_desired_velocities)))
        
        """ for relaxation time parameter"""
        cut_off_low_value_relaxation_time = min_relaxation_time_value - level* self.parameters['young_relaxation_deviation'] 
        cut_off_high_value_relaxation_time = max_relaxation_time_value + level* self.parameters['young_relaxation_deviation']
        
        cut_off_relaxation_times = [item for item in self.average_relaxation_times if (item>= cut_off_low_value_relaxation_time and item <= cut_off_high_value_relaxation_time)]  
        while len(cut_off_relaxation_times) < num:
            samples = numpy.random.normal(mean_relaxation_time, std_relaxation_time, num-(len(cut_off_relaxation_times)))
            refined_samples = [item for item in samples if (item>= cut_off_low_value_relaxation_time and item <= cut_off_high_value_relaxation_time)]  
            cut_off_relaxation_times.extend(refined_samples)          
         
        if level ==3:       
            self.average_cutoff_lv3_relaxation_times = cut_off_relaxation_times
            self.average_cutoff_lv3_relaxation_times_low_value = cut_off_low_value_relaxation_time
            self.average_cutoff_lv3_relaxation_times_high_value = cut_off_high_value_relaxation_time
        
        elif level ==1:
            self.average_cutoff_lv1_relaxation_times = cut_off_relaxation_times
            self.average_cutoff_lv1_relaxation_times_low_value = cut_off_low_value_relaxation_time
            self.average_cutoff_lv1_relaxation_times_high_value = cut_off_high_value_relaxation_time
      
        """ for interaction strength parameter"""
        cut_off_low_value_interaction_strength = min_interaction_strength_value - level* self.parameters['young_force_deviation'] 
        cut_off_high_value_interaction_strength = max_interaction_strength_value + level* self.parameters['young_force_deviation']
        
        cut_off_interaction_strengths = [item for item in self.average_interaction_strengths if (item>= cut_off_low_value_interaction_strength and item <= cut_off_high_value_interaction_strength)]  
        while len(cut_off_interaction_strengths) < num:
            samples = numpy.random.normal(mean_interaction_strength, std_interaction_strength, num-(len(cut_off_interaction_strengths)))
            refined_samples = [item for item in samples if (item>= cut_off_low_value_interaction_strength and item <= cut_off_high_value_interaction_strength)]  
            cut_off_interaction_strengths.extend(refined_samples)          
         
        if level ==3:       
            self.average_cutoff_lv3_interaction_strengths = cut_off_interaction_strengths
            self.average_cutoff_lv3_interaction_strengths_low_value = cut_off_low_value_interaction_strength
            self.average_cutoff_lv3_interaction_strengths_high_value = cut_off_high_value_interaction_strength
        
        elif level ==1:
            self.average_cutoff_lv1_interaction_strengths = cut_off_interaction_strengths
            self.average_cutoff_lv1_interaction_strengths_low_value = cut_off_low_value_interaction_strength
            self.average_cutoff_lv1_interaction_strengths_high_value = cut_off_high_value_interaction_strength
        
        """ for interaction range parameter"""
        cut_off_low_value_interaction_range = min_interaction_range_value - level* self.parameters['young_range_deviation'] 
        cut_off_high_value_interaction_range = max_interaction_range_value + level* self.parameters['young_range_deviation']
        
        cut_off_interaction_ranges = [item for item in self.average_interaction_ranges if (item>= cut_off_low_value_interaction_range and item <= cut_off_high_value_interaction_range)]  
        while len(cut_off_interaction_ranges) < num:
            samples = numpy.random.normal(mean_interaction_range, std_interaction_range, num-(len(cut_off_interaction_ranges)))
            refined_samples = [item for item in samples if (item>= cut_off_low_value_interaction_range and item <= cut_off_high_value_interaction_range)]  
            cut_off_interaction_ranges.extend(refined_samples)          
         
        if level ==3:       
            self.average_cutoff_lv3_interaction_ranges = cut_off_interaction_ranges
            self.average_cutoff_lv3_interaction_ranges_low_value = cut_off_low_value_interaction_range
            self.average_cutoff_lv3_interaction_ranges_high_value = cut_off_high_value_interaction_range
        
        elif level ==1:
            self.average_cutoff_lv1_interaction_ranges = cut_off_interaction_ranges
            self.average_cutoff_lv1_interaction_ranges_low_value = cut_off_low_value_interaction_range
            self.average_cutoff_lv1_interaction_ranges_high_value = cut_off_high_value_interaction_range
        
      
    def _generate_uniform_cutoff_level_distribution(self, 
                                                min_desired_velocity_value, max_desired_velocity_value,
                                                min_relaxation_time_value, max_relaxation_time_value,
                                                min_interaction_strength_value, max_interaction_strength_value,
                                                min_interaction_range_value, max_interaction_range_value,                                            
                                                num, level):      
        if num ==0:
            return

        """ for desired velocity parameter"""
        cut_off_low_value_desired_velocity = min_desired_velocity_value - level* self.parameters['young_velocity_deviation'] 
        cut_off_high_value_desired_velocity = max_desired_velocity_value + level* self.parameters['young_velocity_deviation']
        
        cut_off_desired_velocities = []  
        while len(cut_off_desired_velocities) < num:
            samples = numpy.random.uniform(cut_off_low_value_desired_velocity, cut_off_high_value_desired_velocity, num)
            cut_off_desired_velocities.extend(samples)          
         
        if level ==3:       
            self.uniform_cutoff_lv3_desired_velocities = cut_off_desired_velocities
            self.uniform_cutoff_lv3_desired_velocities_low_value = cut_off_low_value_desired_velocity
            self.uniform_cutoff_lv3_desired_velocities_high_value = cut_off_high_value_desired_velocity
        
        elif level ==1:
            self.uniform_cutoff_lv1_desired_velocities = cut_off_desired_velocities
            self.uniform_cutoff_lv1_desired_velocities_low_value = cut_off_low_value_desired_velocity
            self.uniform_cutoff_lv1_desired_velocities_high_value = cut_off_high_value_desired_velocity
      
      
        """ for relaxation time parameter"""
        cut_off_low_value_relaxation_time = min_relaxation_time_value - level* self.parameters['young_relaxation_deviation'] 
        cut_off_high_value_relaxation_time = max_relaxation_time_value + level* self.parameters['young_relaxation_deviation']
        
        cut_off_relaxation_times = []  
        while len(cut_off_relaxation_times) < num:
            samples = numpy.random.uniform(cut_off_low_value_relaxation_time, cut_off_high_value_relaxation_time, num)
            cut_off_relaxation_times.extend(samples)          
         
        if level ==3:       
            self.uniform_cutoff_lv3_relaxation_times = cut_off_relaxation_times
            self.uniform_cutoff_lv3_relaxation_times_low_value = cut_off_low_value_relaxation_time
            self.uniform_cutoff_lv3_relaxation_times_high_value = cut_off_high_value_relaxation_time
        
        elif level ==1:
            self.uniform_cutoff_lv1_relaxation_times = cut_off_relaxation_times
            self.uniform_cutoff_lv1_relaxation_times_low_value = cut_off_low_value_relaxation_time
            self.uniform_cutoff_lv1_relaxation_times_high_value = cut_off_high_value_relaxation_time
         
        """ for interaction strength parameter"""
        cut_off_low_value_interaction_strength = min_interaction_strength_value - level* self.parameters['young_force_deviation'] 
        cut_off_high_value_interaction_strength = max_interaction_strength_value + level* self.parameters['young_force_deviation']
        
        cut_off_interaction_strengths = []  
        while len(cut_off_interaction_strengths) < num:
            samples = numpy.random.uniform(cut_off_low_value_interaction_strength, cut_off_high_value_interaction_strength, num)
            cut_off_interaction_strengths.extend(samples)          
         
        if level ==3:       
            self.uniform_cutoff_lv3_interaction_strengths = cut_off_interaction_strengths
            self.uniform_cutoff_lv3_interaction_strengths_low_value = cut_off_low_value_interaction_strength
            self.uniform_cutoff_lv3_interaction_strengths_high_value = cut_off_high_value_interaction_strength

        elif level ==1:
            self.uniform_cutoff_lv1_interaction_strengths = cut_off_interaction_strengths
            self.uniform_cutoff_lv1_interaction_strengths_low_value = cut_off_low_value_interaction_strength
            self.uniform_cutoff_lv1_interaction_strengths_high_value = cut_off_high_value_interaction_strength   
        
        """ for interaction range parameter """    
        cut_off_low_value_interaction_range = min_interaction_range_value - level* self.parameters['young_range_deviation'] 
        cut_off_high_value_interaction_range = max_interaction_range_value + level* self.parameters['young_range_deviation']
      
        cut_off_interaction_ranges = []  
        while len(cut_off_interaction_ranges) < num:
            samples = numpy.random.uniform(cut_off_low_value_interaction_range, cut_off_high_value_interaction_range, num)
            cut_off_interaction_ranges.extend(samples)          
         
        if level ==3:     
            self.uniform_cutoff_lv3_interaction_ranges = cut_off_interaction_ranges
            self.uniform_cutoff_lv3_interaction_ranges_low_value = cut_off_low_value_interaction_range
            self.uniform_cutoff_lv3_interaction_ranges_high_value = cut_off_high_value_interaction_range
         
        elif level ==1:
            self.uniform_cutoff_lv1_interaction_ranges = cut_off_interaction_ranges
            self.uniform_cutoff_lv1_interaction_ranges_low_value = cut_off_low_value_interaction_range
            self.uniform_cutoff_lv1_interaction_ranges_high_value = cut_off_high_value_interaction_range
        
    def _to_JSON(self):
        return  json.dumps(self, cls=AverageLog_Encoder)

    def get_parameters(self):
        return self.parameters

    def get_average_desired_velocities(self):
        return self.average_desired_velocities


    def get_average_relaxation_times(self):
        return self.average_relaxation_times


    def get_average_interaction_strengths(self):
        return self.average_interaction_strengths


    def get_average_interaction_ranges(self):
        return self.average_interaction_ranges


    def get_average_cutoff_lv_3_desired_velocities(self):
        return self.average_cutoff_lv3_desired_velocities


    def get_average_cutoff_lv_3_desired_velocities_low_value(self):
        return self.average_cutoff_lv3_desired_velocities_low_value


    def get_average_cutoff_lv_3_desired_velocities_high_value(self):
        return self.average_cutoff_lv3_desired_velocities_high_value


    def get_average_cutoff_lv_3_relaxation_times(self):
        return self.average_cutoff_lv3_relaxation_times


    def get_average_cutoff_lv_3_relaxation_times_low_value(self):
        return self.average_cutoff_lv3_relaxation_times_low_value


    def get_average_cutoff_lv_3_relaxation_times_high_value(self):
        return self.average_cutoff_lv3_relaxation_times_high_value


    def get_average_cutoff_lv_3_interaction_strengths(self):
        return self.average_cutoff_lv3_interaction_strengths


    def get_average_cutoff_lv_3_interaction_strengths_low_value(self):
        return self.average_cutoff_lv3_interaction_strengths_low_value


    def get_average_cutoff_lv_3_interaction_strengths_high_value(self):
        return self.average_cutoff_lv3_interaction_strengths_high_value


    def get_average_cutoff_lv_3_interaction_ranges(self):
        return self.average_cutoff_lv3_interaction_ranges


    def get_average_cutoff_lv_3_interaction_ranges_low_value(self):
        return self.average_cutoff_lv3_interaction_ranges_low_value


    def get_average_cutoff_lv_3_interaction_ranges_high_value(self):
        return self.average_cutoff_lv3_interaction_ranges_high_value


    def get_average_cutoff_lv_1_desired_velocities(self):
        return self.average_cutoff_lv1_desired_velocities


    def get_average_cutoff_lv_1_desired_velocities_low_value(self):
        return self.average_cutoff_lv1_desired_velocities_low_value


    def get_average_cutoff_lv_1_desired_velocities_high_value(self):
        return self.average_cutoff_lv1_desired_velocities_high_value


    def get_average_cutoff_lv_1_relaxation_times(self):
        return self.average_cutoff_lv1_relaxation_times


    def get_average_cutoff_lv_1_relaxation_times_low_value(self):
        return self.average_cutoff_lv1_relaxation_times_low_value


    def get_average_cutoff_lv_1_relaxation_times_high_value(self):
        return self.average_cutoff_lv1_relaxation_times_high_value


    def get_average_cutoff_lv_1_interaction_strengths(self):
        return self.average_cutoff_lv1_interaction_strengths


    def get_average_cutoff_lv_1_interaction_strengths_low_value(self):
        return self.average_cutoff_lv1_interaction_strengths_low_value


    def get_average_cutoff_lv_1_interaction_strengths_high_value(self):
        return self.average_cutoff_lv1_interaction_strengths_high_value


    def get_average_cutoff_lv_1_interaction_ranges(self):
        return self.average_cutoff_lv1_interaction_ranges


    def get_average_cutoff_lv_1_interaction_ranges_low_value(self):
        return self.average_cutoff_lv1_interaction_ranges_low_value


    def get_average_cutoff_lv_1_interaction_ranges_high_value(self):
        return self.average_cutoff_lv1_interaction_ranges_high_value


    def get_uniform_cutoff_lv_3_desired_velocities(self):
        return self.uniform_cutoff_lv3_desired_velocities


    def get_uniform_cutoff_lv_3_desired_velocities_low_value(self):
        return self.uniform_cutoff_lv3_desired_velocities_low_value


    def get_uniform_cutoff_lv_3_desired_velocities_high_value(self):
        return self.uniform_cutoff_lv3_desired_velocities_high_value


    def get_uniform_cutoff_lv_3_relaxation_times(self):
        return self.uniform_cutoff_lv3_relaxation_times


    def get_uniform_cutoff_lv_3_relaxation_times_low_value(self):
        return self.uniform_cutoff_lv3_relaxation_times_low_value


    def get_uniform_cutoff_lv_3_relaxation_times_high_value(self):
        return self.uniform_cutoff_lv3_relaxation_times_high_value


    def get_uniform_cutoff_lv_3_interaction_strengths(self):
        return self.uniform_cutoff_lv3_interaction_strengths


    def get_uniform_cutoff_lv_3_interaction_strengths_low_value(self):
        return self.uniform_cutoff_lv3_interaction_strengths_low_value


    def get_uniform_cutoff_lv_3_interaction_strengths_high_value(self):
        return self.uniform_cutoff_lv3_interaction_strengths_high_value


    def get_uniform_cutoff_lv_3_interaction_ranges(self):
        return self.uniform_cutoff_lv3_interaction_ranges


    def get_uniform_cutoff_lv_3_interaction_ranges_low_value(self):
        return self.uniform_cutoff_lv3_interaction_ranges_low_value


    def get_uniform_cutoff_lv_3_interaction_ranges_high_value(self):
        return self.uniform_cutoff_lv3_interaction_ranges_high_value


    def get_uniform_cutoff_lv_1_desired_velocities(self):
        return self.uniform_cutoff_lv1_desired_velocities


    def get_uniform_cutoff_lv_1_desired_velocities_low_value(self):
        return self.uniform_cutoff_lv1_desired_velocities_low_value


    def get_uniform_cutoff_lv_1_desired_velocities_high_value(self):
        return self.uniform_cutoff_lv1_desired_velocities_high_value


    def get_uniform_cutoff_lv_1_relaxation_times(self):
        return self.uniform_cutoff_lv1_relaxation_times


    def get_uniform_cutoff_lv_1_relaxation_times_low_value(self):
        return self.uniform_cutoff_lv1_relaxation_times_low_value


    def get_uniform_cutoff_lv_1_relaxation_times_high_value(self):
        return self.uniform_cutoff_lv1_relaxation_times_high_value


    def get_uniform_cutoff_lv_1_interaction_strengths(self):
        return self.uniform_cutoff_lv1_interaction_strengths


    def get_uniform_cutoff_lv_1_interaction_strengths_low_value(self):
        return self.uniform_cutoff_lv1_interaction_strengths_low_value


    def get_uniform_cutoff_lv_1_interaction_strengths_high_value(self):
        return self.uniform_cutoff_lv1_interaction_strengths_high_value


    def get_uniform_cutoff_lv_1_interaction_ranges(self):
        return self.uniform_cutoff_lv1_interaction_ranges


    def get_uniform_cutoff_lv_1_interaction_ranges_low_value(self):
        return self.uniform_cutoff_lv1_interaction_ranges_low_value


    def get_uniform_cutoff_lv_1_interaction_ranges_high_value(self):
        return self.uniform_cutoff_lv1_interaction_ranges_high_value


    def set_parameters(self, value):
        self.parameters = value


    def set_average_desired_velocities(self, value):
        self.average_desired_velocities = value


    def set_average_relaxation_times(self, value):
        self.average_relaxation_times = value


    def set_average_interaction_strengths(self, value):
        self.average_interaction_strengths = value


    def set_average_interaction_ranges(self, value):
        self.average_interaction_ranges = value


    def set_average_cutoff_lv_3_desired_velocities(self, value):
        self.average_cutoff_lv3_desired_velocities = value


    def set_average_cutoff_lv_3_desired_velocities_low_value(self, value):
        self.average_cutoff_lv3_desired_velocities_low_value = value


    def set_average_cutoff_lv_3_desired_velocities_high_value(self, value):
        self.average_cutoff_lv3_desired_velocities_high_value = value


    def set_average_cutoff_lv_3_relaxation_times(self, value):
        self.average_cutoff_lv3_relaxation_times = value


    def set_average_cutoff_lv_3_relaxation_times_low_value(self, value):
        self.average_cutoff_lv3_relaxation_times_low_value = value


    def set_average_cutoff_lv_3_relaxation_times_high_value(self, value):
        self.average_cutoff_lv3_relaxation_times_high_value = value


    def set_average_cutoff_lv_3_interaction_strengths(self, value):
        self.average_cutoff_lv3_interaction_strengths = value


    def set_average_cutoff_lv_3_interaction_strengths_low_value(self, value):
        self.average_cutoff_lv3_interaction_strengths_low_value = value


    def set_average_cutoff_lv_3_interaction_strengths_high_value(self, value):
        self.average_cutoff_lv3_interaction_strengths_high_value = value


    def set_average_cutoff_lv_3_interaction_ranges(self, value):
        self.average_cutoff_lv3_interaction_ranges = value


    def set_average_cutoff_lv_3_interaction_ranges_low_value(self, value):
        self.average_cutoff_lv3_interaction_ranges_low_value = value


    def set_average_cutoff_lv_3_interaction_ranges_high_value(self, value):
        self.average_cutoff_lv3_interaction_ranges_high_value = value


    def set_average_cutoff_lv_1_desired_velocities(self, value):
        self.average_cutoff_lv1_desired_velocities = value


    def set_average_cutoff_lv_1_desired_velocities_low_value(self, value):
        self.average_cutoff_lv1_desired_velocities_low_value = value


    def set_average_cutoff_lv_1_desired_velocities_high_value(self, value):
        self.average_cutoff_lv1_desired_velocities_high_value = value


    def set_average_cutoff_lv_1_relaxation_times(self, value):
        self.average_cutoff_lv1_relaxation_times = value


    def set_average_cutoff_lv_1_relaxation_times_low_value(self, value):
        self.average_cutoff_lv1_relaxation_times_low_value = value


    def set_average_cutoff_lv_1_relaxation_times_high_value(self, value):
        self.average_cutoff_lv1_relaxation_times_high_value = value


    def set_average_cutoff_lv_1_interaction_strengths(self, value):
        self.average_cutoff_lv1_interaction_strengths = value


    def set_average_cutoff_lv_1_interaction_strengths_low_value(self, value):
        self.average_cutoff_lv1_interaction_strengths_low_value = value


    def set_average_cutoff_lv_1_interaction_strengths_high_value(self, value):
        self.average_cutoff_lv1_interaction_strengths_high_value = value


    def set_average_cutoff_lv_1_interaction_ranges(self, value):
        self.average_cutoff_lv1_interaction_ranges = value


    def set_average_cutoff_lv_1_interaction_ranges_low_value(self, value):
        self.average_cutoff_lv1_interaction_ranges_low_value = value


    def set_average_cutoff_lv_1_interaction_ranges_high_value(self, value):
        self.average_cutoff_lv1_interaction_ranges_high_value = value


    def set_uniform_cutoff_lv_3_desired_velocities(self, value):
        self.uniform_cutoff_lv3_desired_velocities = value


    def set_uniform_cutoff_lv_3_desired_velocities_low_value(self, value):
        self.uniform_cutoff_lv3_desired_velocities_low_value = value


    def set_uniform_cutoff_lv_3_desired_velocities_high_value(self, value):
        self.uniform_cutoff_lv3_desired_velocities_high_value = value


    def set_uniform_cutoff_lv_3_relaxation_times(self, value):
        self.uniform_cutoff_lv3_relaxation_times = value


    def set_uniform_cutoff_lv_3_relaxation_times_low_value(self, value):
        self.uniform_cutoff_lv3_relaxation_times_low_value = value


    def set_uniform_cutoff_lv_3_relaxation_times_high_value(self, value):
        self.uniform_cutoff_lv3_relaxation_times_high_value = value


    def set_uniform_cutoff_lv_3_interaction_strengths(self, value):
        self.uniform_cutoff_lv3_interaction_strengths = value


    def set_uniform_cutoff_lv_3_interaction_strengths_low_value(self, value):
        self.uniform_cutoff_lv3_interaction_strengths_low_value = value


    def set_uniform_cutoff_lv_3_interaction_strengths_high_value(self, value):
        self.uniform_cutoff_lv3_interaction_strengths_high_value = value


    def set_uniform_cutoff_lv_3_interaction_ranges(self, value):
        self.uniform_cutoff_lv3_interaction_ranges = value


    def set_uniform_cutoff_lv_3_interaction_ranges_low_value(self, value):
        self.uniform_cutoff_lv3_interaction_ranges_low_value = value


    def set_uniform_cutoff_lv_3_interaction_ranges_high_value(self, value):
        self.uniform_cutoff_lv3_interaction_ranges_high_value = value


    def set_uniform_cutoff_lv_1_desired_velocities(self, value):
        self.uniform_cutoff_lv1_desired_velocities = value


    def set_uniform_cutoff_lv_1_desired_velocities_low_value(self, value):
        self.uniform_cutoff_lv1_desired_velocities_low_value = value


    def set_uniform_cutoff_lv_1_desired_velocities_high_value(self, value):
        self.uniform_cutoff_lv1_desired_velocities_high_value = value


    def set_uniform_cutoff_lv_1_relaxation_times(self, value):
        self.uniform_cutoff_lv1_relaxation_times = value


    def set_uniform_cutoff_lv_1_relaxation_times_low_value(self, value):
        self.uniform_cutoff_lv1_relaxation_times_low_value = value


    def set_uniform_cutoff_lv_1_relaxation_times_high_value(self, value):
        self.uniform_cutoff_lv1_relaxation_times_high_value = value


    def set_uniform_cutoff_lv_1_interaction_strengths(self, value):
        self.uniform_cutoff_lv1_interaction_strengths = value


    def set_uniform_cutoff_lv_1_interaction_strengths_low_value(self, value):
        self.uniform_cutoff_lv1_interaction_strengths_low_value = value


    def set_uniform_cutoff_lv_1_interaction_strengths_high_value(self, value):
        self.uniform_cutoff_lv1_interaction_strengths_high_value = value


    def set_uniform_cutoff_lv_1_interaction_ranges(self, value):
        self.uniform_cutoff_lv1_interaction_ranges = value


    def set_uniform_cutoff_lv_1_interaction_ranges_low_value(self, value):
        self.uniform_cutoff_lv1_interaction_ranges_low_value = value


    def set_uniform_cutoff_lv_1_interaction_ranges_high_value(self, value):
        self.uniform_cutoff_lv1_interaction_ranges_high_value = value

    
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
   
             
        """ for the average cutoff level 3 normal distribution prototype """
        average_cutoff_lv3_desired_velocities = []
        for velocity in default_obj['average_cutoff_lv3_desired_velocities']:
            average_cutoff_lv3_desired_velocities.append(velocity)
        
        average_cutoff_lv3_desired_velocities_low_value = default_obj['average_cutoff_lv3_desired_velocities_low_value']
        average_cutoff_lv3_desired_velocities_high_value = default_obj['average_cutoff_lv3_desired_velocities_high_value']
        
        average_cutoff_lv3_relaxation_times =[]
        for velocity in default_obj['average_cutoff_lv3_relaxation_times']:
            average_cutoff_lv3_relaxation_times.append(velocity)
       
        average_cutoff_lv3_relaxation_times_low_value = default_obj['average_cutoff_lv3_relaxation_times_low_value']
        average_cutoff_lv3_relaxation_times_high_value = default_obj['average_cutoff_lv3_relaxation_times_high_value']
        
        average_cutoff_lv3_interaction_strengths = []
        for velocity in default_obj['average_cutoff_lv3_interaction_strengths']:
            average_cutoff_lv3_interaction_strengths.append(velocity)
       
        average_cutoff_lv3_interaction_strengths_low_value = default_obj['average_cutoff_lv3_interaction_strengths_low_value']
        average_cutoff_lv3_interaction_strengths_high_value = default_obj['average_cutoff_lv3_interaction_strengths_high_value']
        
        average_cutoff_lv3_interaction_ranges =[]
        for velocity in default_obj['average_cutoff_lv3_interaction_ranges']:
            average_cutoff_lv3_interaction_ranges.append(velocity)
      
        average_cutoff_lv3_interaction_ranges_low_value = default_obj['average_cutoff_lv3_interaction_ranges_low_value']
        average_cutoff_lv3_interaction_ranges_high_value = default_obj['average_cutoff_lv3_interaction_ranges_high_value']
             
        """ for the average cutoff level 1 normal distribution prototype """
        average_cutoff_lv1_desired_velocities = []
        for velocity in default_obj['average_cutoff_lv1_desired_velocities']:
            average_cutoff_lv1_desired_velocities.append(velocity)
      
        average_cutoff_lv1_desired_velocities_low_value = default_obj['average_cutoff_lv1_desired_velocities_low_value']
        average_cutoff_lv1_desired_velocities_high_value = default_obj['average_cutoff_lv1_desired_velocities_high_value']
      
        average_cutoff_lv1_relaxation_times =[]
        for velocity in default_obj['average_cutoff_lv1_relaxation_times']:
            average_cutoff_lv1_relaxation_times.append(velocity)
      
        average_cutoff_lv1_relaxation_times_low_value = default_obj['average_cutoff_lv1_relaxation_times_low_value']
        average_cutoff_lv1_relaxation_times_high_value = default_obj['average_cutoff_lv1_relaxation_times_high_value']
        
        average_cutoff_lv1_interaction_strengths = []
        for velocity in default_obj['average_cutoff_lv1_interaction_strengths']:
            average_cutoff_lv1_interaction_strengths.append(velocity)
            
        average_cutoff_lv1_interaction_strengths_low_value = default_obj['average_cutoff_lv1_interaction_strengths_low_value']
        average_cutoff_lv1_interaction_strengths_high_value = default_obj['average_cutoff_lv1_interaction_strengths_high_value']
        
        average_cutoff_lv1_interaction_ranges =[]
        for velocity in default_obj['average_cutoff_lv1_interaction_ranges']:
            average_cutoff_lv1_interaction_ranges.append(velocity)
       
        average_cutoff_lv1_interaction_ranges_low_value = default_obj['average_cutoff_lv1_interaction_ranges_low_value']
        average_cutoff_lv1_interaction_ranges_high_value = default_obj['average_cutoff_lv1_interaction_ranges_high_value']
        
        
        """ for the uniform cutoff level 3 distribution prototype """
        uniform_cutoff_lv3_desired_velocities = []
        for velocity in default_obj['uniform_cutoff_lv3_desired_velocities']:
            uniform_cutoff_lv3_desired_velocities.append(velocity)
       
        uniform_cutoff_lv3_desired_velocities_low_value = default_obj['uniform_cutoff_lv3_desired_velocities_low_value']
        uniform_cutoff_lv3_desired_velocities_high_value = default_obj['uniform_cutoff_lv3_desired_velocities_high_value']
      
        uniform_cutoff_lv3_relaxation_times =[]
        for velocity in default_obj['uniform_cutoff_lv3_relaxation_times']:
            uniform_cutoff_lv3_relaxation_times.append(velocity)
       
        uniform_cutoff_lv3_relaxation_times_low_value = default_obj['uniform_cutoff_lv3_relaxation_times_low_value']
        uniform_cutoff_lv3_relaxation_times_high_value = default_obj['uniform_cutoff_lv3_relaxation_times_high_value']
        
        uniform_cutoff_lv3_interaction_strengths = []
        for velocity in default_obj['uniform_cutoff_lv3_interaction_strengths']:
            uniform_cutoff_lv3_interaction_strengths.append(velocity)
       
        uniform_cutoff_lv3_interaction_strengths_low_value = default_obj['uniform_cutoff_lv3_interaction_strengths_low_value']
        uniform_cutoff_lv3_interaction_strengths_high_value = default_obj['uniform_cutoff_lv3_interaction_strengths_high_value']
        
        uniform_cutoff_lv3_interaction_ranges =[]
        for velocity in default_obj['uniform_cutoff_lv3_interaction_ranges']:
            uniform_cutoff_lv3_interaction_ranges.append(velocity)
       
        uniform_cutoff_lv3_interaction_ranges_low_value = default_obj['uniform_cutoff_lv3_interaction_ranges_low_value']
        uniform_cutoff_lv3_interaction_ranges_high_value = default_obj['uniform_cutoff_lv3_interaction_ranges_high_value']
         
        """ for the uniform cutoff level 1 distribution prototype """
        uniform_cutoff_lv1_desired_velocities = []
        for velocity in default_obj['uniform_cutoff_lv1_desired_velocities']:
            uniform_cutoff_lv1_desired_velocities.append(velocity)
       
        uniform_cutoff_lv1_desired_velocities_low_value = default_obj['uniform_cutoff_lv1_desired_velocities_low_value']
        uniform_cutoff_lv1_desired_velocities_high_value = default_obj['uniform_cutoff_lv1_desired_velocities_high_value']
      
        uniform_cutoff_lv1_relaxation_times =[]
        for velocity in default_obj['uniform_cutoff_lv1_relaxation_times']:
            uniform_cutoff_lv1_relaxation_times.append(velocity)
       
        uniform_cutoff_lv1_relaxation_times_low_value = default_obj['uniform_cutoff_lv1_relaxation_times_low_value']
        uniform_cutoff_lv1_relaxation_times_high_value = default_obj['uniform_cutoff_lv1_relaxation_times_high_value']
        
        uniform_cutoff_lv1_interaction_strengths = []
        for velocity in default_obj['uniform_cutoff_lv1_interaction_strengths']:
            uniform_cutoff_lv1_interaction_strengths.append(velocity)
      
        uniform_cutoff_lv1_interaction_strengths_low_value = default_obj['uniform_cutoff_lv1_interaction_strengths_low_value']
        uniform_cutoff_lv1_interaction_strengths_high_value = default_obj['uniform_cutoff_lv1_interaction_strengths_high_value']
        
        uniform_cutoff_lv1_interaction_ranges =[]
        for velocity in default_obj['uniform_cutoff_lv1_interaction_ranges']:
            uniform_cutoff_lv1_interaction_ranges.append(velocity)
      
        uniform_cutoff_lv1_interaction_ranges_low_value = default_obj['uniform_cutoff_lv1_interaction_ranges_low_value']
        uniform_cutoff_lv1_interaction_ranges_high_value = default_obj['uniform_cutoff_lv1_interaction_ranges_high_value']
        
        """ sharing parameters extraction"""
        parameter_data = default_obj['parameters']
  
        average_dist = Average()
        
        average_dist.set_parameters(parameter_data)
        
        average_dist.set_average_desired_velocities(average_desired_velocities)
        average_dist.set_average_relaxation_times(average_relaxation_times)
        average_dist.set_average_interaction_strengths(average_interaction_strengths)
        average_dist.set_average_interaction_ranges(average_interaction_ranges)
        
        average_dist.set_average_cutoff_lv_3_desired_velocities(average_cutoff_lv3_desired_velocities)
        average_dist.set_average_cutoff_lv_3_desired_velocities_low_value(average_cutoff_lv3_desired_velocities_low_value)
        average_dist.set_average_cutoff_lv_3_desired_velocities_high_value(average_cutoff_lv3_desired_velocities_high_value)
        
        average_dist.set_average_cutoff_lv_3_relaxation_times(average_cutoff_lv3_relaxation_times)
        average_dist.set_average_cutoff_lv_3_relaxation_times_low_value(average_cutoff_lv3_relaxation_times_low_value)
        average_dist.set_average_cutoff_lv_3_relaxation_times_high_value(average_cutoff_lv3_relaxation_times_high_value)
        
        average_dist.set_average_cutoff_lv_3_interaction_strengths(average_cutoff_lv3_interaction_strengths)
        average_dist.set_average_cutoff_lv_3_interaction_strengths_low_value(average_cutoff_lv3_interaction_strengths_low_value)
        average_dist.set_average_cutoff_lv_3_interaction_strengths_high_value(average_cutoff_lv3_interaction_strengths_high_value)
        
        average_dist.set_average_cutoff_lv_3_interaction_ranges(average_cutoff_lv3_interaction_ranges)
        average_dist.set_average_cutoff_lv_3_interaction_ranges_low_value(average_cutoff_lv3_interaction_ranges_low_value)
        average_dist.set_average_cutoff_lv_3_interaction_ranges_high_value(average_cutoff_lv3_interaction_ranges_high_value)
        
        average_dist.set_average_cutoff_lv_1_desired_velocities(average_cutoff_lv1_desired_velocities)
        average_dist.set_average_cutoff_lv_1_desired_velocities_low_value(average_cutoff_lv1_desired_velocities_low_value)
        average_dist.set_average_cutoff_lv_1_desired_velocities_high_value(average_cutoff_lv1_desired_velocities_high_value)
        
        average_dist.set_average_cutoff_lv_1_relaxation_times(average_cutoff_lv1_relaxation_times)
        average_dist.set_average_cutoff_lv_1_relaxation_times_low_value(average_cutoff_lv1_relaxation_times_low_value)
        average_dist.set_average_cutoff_lv_1_relaxation_times_high_value(average_cutoff_lv1_relaxation_times_high_value)
        
        average_dist.set_average_cutoff_lv_1_interaction_strengths(average_cutoff_lv1_interaction_strengths)
        average_dist.set_average_cutoff_lv_1_interaction_strengths_low_value(average_cutoff_lv1_interaction_strengths_low_value)
        average_dist.set_average_cutoff_lv_1_interaction_strengths_high_value(average_cutoff_lv1_interaction_strengths_high_value)
        
        average_dist.set_average_cutoff_lv_1_interaction_ranges(average_cutoff_lv1_interaction_ranges)
        average_dist.set_average_cutoff_lv_1_interaction_ranges_low_value(average_cutoff_lv1_interaction_ranges_low_value)
        average_dist.set_average_cutoff_lv_1_interaction_ranges_high_value(average_cutoff_lv1_interaction_ranges_high_value)
       
        average_dist.set_uniform_cutoff_lv_3_desired_velocities(uniform_cutoff_lv3_desired_velocities)
        average_dist.set_uniform_cutoff_lv_3_desired_velocities_low_value(uniform_cutoff_lv3_desired_velocities_low_value)
        average_dist.set_uniform_cutoff_lv_3_desired_velocities_high_value(uniform_cutoff_lv3_desired_velocities_high_value)
        
        average_dist.set_uniform_cutoff_lv_3_relaxation_times(uniform_cutoff_lv3_relaxation_times)
        average_dist.set_uniform_cutoff_lv_3_relaxation_times_low_value(uniform_cutoff_lv3_relaxation_times_low_value)
        average_dist.set_uniform_cutoff_lv_3_relaxation_times_high_value(uniform_cutoff_lv3_relaxation_times_high_value)
        
        average_dist.set_uniform_cutoff_lv_3_interaction_strengths(uniform_cutoff_lv3_interaction_strengths)
        average_dist.set_uniform_cutoff_lv_3_interaction_strengths_low_value(uniform_cutoff_lv3_interaction_strengths_low_value)
        average_dist.set_uniform_cutoff_lv_3_interaction_strengths_high_value(uniform_cutoff_lv3_interaction_strengths_high_value)
        
        average_dist.set_uniform_cutoff_lv_3_interaction_ranges(uniform_cutoff_lv3_interaction_ranges)
        average_dist.set_uniform_cutoff_lv_3_interaction_ranges_low_value(uniform_cutoff_lv3_interaction_ranges_low_value)
        average_dist.set_uniform_cutoff_lv_3_interaction_ranges_high_value(uniform_cutoff_lv3_interaction_ranges_high_value)
        
        average_dist.set_uniform_cutoff_lv_1_desired_velocities(uniform_cutoff_lv1_desired_velocities)
        average_dist.set_uniform_cutoff_lv_1_desired_velocities_low_value(uniform_cutoff_lv1_desired_velocities_low_value)
        average_dist.set_uniform_cutoff_lv_1_desired_velocities_high_value(uniform_cutoff_lv1_desired_velocities_high_value)    
        
        average_dist.set_uniform_cutoff_lv_1_relaxation_times(uniform_cutoff_lv1_relaxation_times)
        average_dist.set_uniform_cutoff_lv_1_relaxation_times_low_value(uniform_cutoff_lv1_relaxation_times_low_value)
        average_dist.set_uniform_cutoff_lv_1_relaxation_times_high_value(uniform_cutoff_lv1_relaxation_times_high_value)
        
        average_dist.set_uniform_cutoff_lv_1_interaction_strengths(uniform_cutoff_lv1_interaction_strengths)
        average_dist.set_uniform_cutoff_lv_1_interaction_strengths_low_value(uniform_cutoff_lv1_interaction_strengths_low_value)
        average_dist.set_uniform_cutoff_lv_1_interaction_strengths_high_value(uniform_cutoff_lv1_interaction_strengths_high_value)
        
        average_dist.set_uniform_cutoff_lv_1_interaction_ranges(uniform_cutoff_lv1_interaction_ranges)
        average_dist.set_uniform_cutoff_lv_1_interaction_ranges_low_value(uniform_cutoff_lv1_interaction_ranges_low_value)
        average_dist.set_uniform_cutoff_lv_1_interaction_ranges_high_value(uniform_cutoff_lv1_interaction_ranges_high_value)
    
        return average_dist