'''
Created on 1 Feb 2016

@author: quangv
'''

import numpy as np
from src import constants

class ObservationPlots:

    def __init__(self, parameters, total_group_num):
        self.parameters = parameters
        self.observered_duration = constants.total_monitoring_duration_uni_direction
        self.total_group_num = total_group_num
        
        self.t_values = []
        self.group_cohesion_degree = []
        self.escaped_number = []
        i=0
        while i < self.total_group_num:
            self.group_cohesion_degree.append([]) 
            self.escaped_number.append([])
            i+=1

    def _add_sample(self,  t, current_group_cohesion_degree, current_escaped_number): 
      
        self.t_values.append(t)
        
        for i in range(len(current_group_cohesion_degree)):
            self.group_cohesion_degree[i].append(current_group_cohesion_degree[i])
            self.escaped_number[i].append(current_escaped_number[i])

    
    def _proceed_cut_off(self):            
        #cut off by the first n-second, last m-second and compute the average through normalization
        i = 0
        while i < constants.cut_off_first_period:
            if len(self.t_values) > 1: #always keep the last data point
                del self.t_values[0] 
                
                for i in range(len(self.group_cohesion_degree)):
                    if len(self.group_cohesion_degree[i]) > 1: #always keep the last data point
                        del self.group_cohesion_degree[i][0] 
            
                for i in range(len(self.escaped_number)):
                    if len(self.escaped_number[i]) > 1: #always keep the last data point
                        del self.escaped_number[i][0] 
            
            i+=1
                
    def reset_sample(self):
       
        self.t_values = []
        self.group_cohesion_degree = []
        self.escaped_number = []
        i=0
        while i < self.total_group_num:
            self.group_cohesion_degree.append([]) 
            self.escaped_number.append([])
            i+=1

    def _get_cohesion_degree(self):

        #remove zero value in the list
        for i in range(len(self.group_cohesion_degree)):
            j = 0
            while j < len (self.group_cohesion_degree[i]):
                if self.group_cohesion_degree[i][j] == 0.0 or np.isnan(self.group_cohesion_degree[i][j]):
                    del self.group_cohesion_degree[i][j]
                else:
                    j+=1
                    
        cohesion_degree = []
        for i in range(len(self.group_cohesion_degree)):
            if len(self.group_cohesion_degree[i]) == 0:
                cohesion_degree.append(0)
            
            else:
                cohesion_degree.append(np.mean(self.group_cohesion_degree[i]))

        return cohesion_degree
    
    def _get_flow_rate(self):
        
        #remove the last same number row
        for i in range(len(self.escaped_number)):
            j = 0
            while j< len(self.escaped_number[i]) and len(self.escaped_number[i])>0:
                if self.escaped_number[i][-1] == self.escaped_number[i][len(self.escaped_number[i])-2]:
                    del self.escaped_number[i][len(self.escaped_number[i])-1]
                else:
                    j+=1
        
        flowrate = []
        
        for i in range(len(self.escaped_number)):
            if len(self.escaped_number[i]) >0 and self.t_values[len(self.escaped_number[i])-1] > 0:
                group_flowrate =  self.escaped_number[i][-1]/self.t_values[len(self.escaped_number[i])-1]
                flowrate.append(group_flowrate)
            else:
                flowrate.append(0.0)
        return flowrate
        