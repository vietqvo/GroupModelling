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
     
        self.group_cohesion_degree.clear()

        
        if len(self.parameters['start_areas']) ==1:
            self.observered_duration = constants.total_monitoring_duration_uni_direction
        else:
            self.observered_duration = constants.total_monitoring_duration_bi_direction
           
    def _add_sample(self,  t, group_cohesion_degree): 
      

        self.t_values.append(t)
        self.group_cohesion_degree.append(group_cohesion_degree) 
   
                      
    def _observation_plot(self,simulation_id):

        #fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, figsize=(30,20)) 
        fig, (ax1) = plt.subplots(1, figsize=(30,20)) 
        #fig, (ax1, ax2) = plt.subplots(2, figsize=(30,20)) 
        fig.suptitle(r"Simulation Id:=%s" % simulation_id, fontsize=18)
        
        ax1.set_title(r"$Group\/cohesion\/degree$",fontsize=18)
        ax1.set_xlabel('time (second)')
        
        ax1.plot(self.t_values, self.group_cohesion_degree,'k.-')
        ax1.grid(True)
        
        
        ax1.set_xticks([x*10 for x in range(0,int((self.observered_duration/10)+1))])
       
        return fig
      
    def _save(self, prefix, simulation_id,rep):
         
        escape_number_fig = self._observation_plot(simulation_id)
        if self.observation_mode == 0:
            if rep==False:
                escape_number_fig.savefig("%s-%s.pdf" % (prefix, simulation_id), dpi=900)  
            else:
                escape_number_fig.savefig("%s-%s-rep.pdf" % (prefix, simulation_id), dpi=900)  
        else:
            if rep==False:
                escape_number_fig.savefig(r"%s-%s.pdf" % (prefix, simulation_id), dpi=900)
            else:
                escape_number_fig.savefig(r"%s-%s-rep.pdf" % (prefix, simulation_id), dpi=900)  
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
            
            i+=1
                
    def reset_sample(self):
       
        self.t_values.clear()
        self.group_cohesion_degree.clear()

    def _get_cohesion_degree(self):
        return np.mean(self.group_cohesion_degree) 
       
    def _get_cohesion_degree_str(self):
        str_cohesion_degree = '[' + ','. join(str(x) for x in self.group_cohesion_degree)
        str_cohesion_degree += ']'
        return str_cohesion_degree
    