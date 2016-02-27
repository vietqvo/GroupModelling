'''
Created on 1 Feb 2016

@author: quangv
'''
import matplotlib.pyplot as plt
from src import constants
import math as m
import numpy as np

class ObservationPlots:

    def __init__(self, parameters, total_group_num):
        self.parameters = parameters
        self.observered_duration = constants.total_monitoring_duration_uni_direction
        self.total_group_num = total_group_num
        
        self.t_values = []
        self.cd_within_group = []
        self.cd_between_groups = []
        
        #below values are calculated at equilibrium state
        self.equilibrium_time = 0.0
        self.equilibrium_cd_within_group = 0.0
        self.equilibrium_cd_between_group = 0.0
        
    def _add_sample(self,  t, comfortable_distances_within_group, comfortable_distances_betweens_groups): 
      
        self.t_values.append(t)
        
        if len(comfortable_distances_within_group)==0:
            self.cd_within_group.append(0.0)
        else:    
            self.cd_within_group.append(np.mean(comfortable_distances_within_group))
           
        if m.fabs(self.equilibrium_cd_between_group- comfortable_distances_betweens_groups) > 0.01 or m.fabs(np.mean(comfortable_distances_within_group) - self.equilibrium_cd_within_group) > 0.01:
                
            self.equilibrium_time = t 
            self.equilibrium_cd_within_group = np.mean(comfortable_distances_within_group)
            self.equilibrium_cd_between_group = comfortable_distances_betweens_groups
                
                
        self.cd_between_groups.append(comfortable_distances_betweens_groups)
        
                  
    def reset_sample(self):
       
        self.t_values = []
        self.cd_within_group = []
        self.cd_between_groups = []
        
        #below values are calculated at equilibrium state
        self.equilibrium_time = 0.0
        self.equilibrium_cd_within_group = 0.0
        self.equilibrium_cd_between_group = 0.0
        
    
    def _plot_cd(self, simulation_id):

        fig, (ax1) = plt.subplots(1, sharex=True) 
        ax1.set_title(r"$Distances\/of \/intragroup\/and\/intergroup$",fontsize=18)
        ax1.set_xlabel('time (second)')
                
        ax1.plot(self.t_values, self.cd_within_group,'r.-', label=r"$distance_{intragroup}$")
        ax1.plot(self.t_values, self.cd_between_groups,'b.-', label=r"$distance_{intergroup}$", linestyle = '-')
        ax1.legend(loc='upper right', bbox_to_anchor=(1.0, 0.96), ncol=1, fancybox=False, shadow=False,prop={'size':14})
        ax1.grid(True)
        ax1.set_xticks([x*10 for x in range(0,int((len(self.t_values)/10)+1))])
                        
        return fig
    
    def _save(self, prefix, simulation_id):
               
        cd_fig = self._plot_cd(simulation_id)
        cd_fig.savefig("%s-%s.pdf" % (prefix, simulation_id))  

        plt.clf()
        plt.close('all')
        
        #self.reset_sample()
           
    def get_equilibrium_cd_between_groups(self):           
        return self.equilibrium_cd_between_group
    
    def get_equilibrium_cd_within_groups(self):
        return self.equilibrium_cd_within_group
    
    def get_equilibrium_time(self):
        return self.equilibrium_time