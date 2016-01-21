'''
Created on 1 Mar 2015

@author: quangv
'''

import matplotlib.pyplot as plt
import numpy as np
from src import constants

class ObservationPlots:

    def __init__(self, parameters, observation_mode=0): #0:new simulation mode #1: replay mode
        self.parameters = parameters
        self.observation_mode =  observation_mode

        self.t_values = list()
        
        self.group_cohesion_degree = list() 
        self.group_average_speed = list() 
        self.group_average_direction = list() 
        self.escaped_number = list()
        
        self.group_cohesion_degree.clear()
        self.group_average_speed.clear()
        self.group_average_direction.clear()
        self.escaped_number.clear()
        
        if len(self.parameters['start_areas']) ==1:
            self.observered_duration = constants.total_monitoring_duration_uni_direction
        else:
            self.observered_duration = constants.total_monitoring_duration_bi_direction
           
    def _add_sample(self,  t, group_cohesion_degree, group_average_speed, group_average_direction, escaped_number): 
      

        self.t_values.append(t)
        self.group_cohesion_degree.append(group_cohesion_degree)
        self.group_average_speed.append(group_average_speed)
        self.group_average_direction.append(group_average_direction)
        self.escaped_number .append(escaped_number)         
   
                      
    def _observation_plot(self,simulation_id):

        #fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, figsize=(30,20)) 
        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(30,20)) 
        #fig, (ax1, ax2) = plt.subplots(2, figsize=(30,20)) 
        fig.suptitle(r"Simulation Id:=%s" % simulation_id, fontsize=18)
        
        ax1.set_title(r"$Group\/cohesion\/degree$",fontsize=18)
        ax2.set_title(r"$Group\/average\/speed$",fontsize=18)
        ax3.set_title(r"$Group\/average\/direction$",fontsize=18)
        ax3.set_xlabel('time (second)')
        
        ax1.plot(self.t_values, self.group_cohesion_degree,'k.-')
        #ax1.legend(loc='upper left', bbox_to_anchor=(0., 1.02), ncol=1, fancybox=True, shadow=True,prop={'size':11})
        ax1.grid(True)
        
        ax2.plot(self.t_values, self.group_average_speed,'k.-')
        #ax2.legend(loc='upper left', bbox_to_anchor=(0., 1.02), ncol=1, fancybox=True, shadow=True,prop={'size':11})
        ax2.grid(True)
        
        ax3.plot(self.t_values, self.group_average_direction,'k.-')
        #ax3.legend(loc='upper left', bbox_to_anchor=(0., 1.02), ncol=1, fancybox=True, shadow=True,prop={'size':11})
        ax3.grid(True)
        
        ax1.set_xticks([x*10 for x in range(0,int((self.observered_duration/10)+1))])
        ax2.set_xticks([x*10 for x in range(0,int((self.observered_duration/10)+1))])
        ax3.set_xticks([x*10 for x in range(0,int((self.observered_duration/10)+1))])
        
        return fig
      
    def _save(self, prefix, simulation_id):
         
        escape_number_fig = self._observation_plot(simulation_id)
        if self.observation_mode == 0:
            escape_number_fig.savefig("%s-%s.pdf" % (prefix, simulation_id), dpi=900)  
        else:
            escape_number_fig.savefig(r"%s-%s.pdf" % (prefix, simulation_id), dpi=900)  
        plt.clf()
        plt.close('all')
        #self.reset_sample()
    
    def _proceed_cut_off(self):            
        #cut off by the first n-second, last m-second and compute the average through normalization
        i = 0
        while i < constants.cut_off_first_period:
            if len(self.t_values) > 1: #always keep the last data point
                del self.t_values[0] 
                
            if len(self.group_cohesion_degree) > 1: #always keep the last data point
                del self.group_cohesion_degree[0] 
            
            if len(self.group_average_speed) > 1: #always keep the last data point
                del self.group_average_speed[0]
            
            if len(self.group_average_direction) > 1: #always keep the last data point
                del self.group_average_direction[0]
            
            i+=1
         
        #cut off the last m-second  
        """"i = 0  
        while i < constants.cut_off_last_period:
            if len(self.t_values) > 1: #always keep the last data point
                del self.t_values[-1] 
                
            if len(self.group_cohesion_degree) > 1:
                del self.group_cohesion_degree[-1]  
            
            if len(self.group_average_speed) > 1: #always keep the last data point
                del self.group_average_speed[-1]
            
            if len(self.group_average_direction) > 1: #always keep the last data point
                del self.group_average_direction[-1]
            
            i+=1"""
                
    def reset_sample(self):
       
        self.t_values.clear()
        self.group_cohesion_degree.clear()
        self.group_average_speed.clear()
        self.group_average_direction.clear()
        self.escaped_number.clear()
        #self.group_escape_rate = 0.0
     
    def _get_cohesion_degree(self):

        #normalize to get average scalar value
        """max_degree = max (self.group_cohesion_degree)  
        min_degree = min (self.group_cohesion_degree) 
        difference = max_degree  - min_degree
        if difference>0:       
            norm = [(i- min_degree)/(difference) for i in self.group_cohesion_degree]
            group_cohesion_degree_scalar_value = sum(norm)/len(norm)
            return group_cohesion_degree_scalar_value
        else:
            return 1.0"""
        return np.mean(self.group_cohesion_degree) 
       
    def _get_cohesion_degree_str(self):
        str_cohesion_degree = '[' + ','. join(str(x) for x in self.group_cohesion_degree)
        str_cohesion_degree += ']'
        return str_cohesion_degree
    
    def _get_average_speed(self):

        #normalize to get average scalar value
        """max_degree = max (self.group_average_speed)  
        min_degree = min (self.group_average_speed) 
        difference = max_degree  - min_degree
        if difference>0:
            norm = [(i- min_degree)/(difference) for i in self.group_average_speed]
            group_average_speed_scalar_value = sum(norm)/len(norm)
            return group_average_speed_scalar_value
        
        else:
            return 1.0"""
        return np.mean(self.group_average_speed)     
    
    def _get_average_speed_str(self):
        str_average_speed = '[' + ','. join(str(x) for x in self.group_average_speed)
        str_average_speed += ']'
        return str_average_speed
            
    def _get_average_direction(self):
     
        #normalize to get average scalar value
        """max_degree = max (self.group_average_direction)  
        min_degree = min (self.group_average_direction) 
        difference = max_degree  - min_degree
        if difference>0:      
            norm = [(i- min_degree)/(difference) for i in self.group_average_direction]
            group_average_direction_scalar_value = sum(norm)/len(norm)
            return group_average_direction_scalar_value
        else:
            return 1"""
        return np.mean(self.group_average_direction)    
        
    def _get_average_direction_str(self):
        str_average_direction = '[' + ','. join(str(x) for x in self.group_average_direction)
        str_average_direction += ']'
        return str_average_direction
                