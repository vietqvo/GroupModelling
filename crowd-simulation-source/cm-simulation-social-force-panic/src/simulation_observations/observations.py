'''
Created on 1 Mar 2015

@author: quangv
'''

import matplotlib.pyplot as plt
from src import constants

class ObservationPlots:

    def __init__(self, parameters, observation_mode=0): #0:new simulation mode #1: replay mode
        self.parameters = parameters
        self.observation_mode =  observation_mode
        
        """ this list is for differential distribution prototype """
        self.t_values_different_distribution_prototype = list()
        self.escape_number_different_distribution_prototype = list() 
        self.escape_rates_different_distribution_protype = 0.0
        self.last_escape_time_different_distribution_protype = 0
        self.panic_level_different_distribution_prototype = list()
        self.interaction_force_different_distribution_prototype = list()
        
        ########################################################################### 
        """this list is for average normal distribution prototype """ 
        self.t_values_average_prototype = list()
        self.escape_number_average_prototype = list()
        self.escape_rates_average_prototype = 0.0
        self.last_escape_time_average_prototype = 0
        self.panic_level_average_prototype = list()
        self.interaction_force_average_prototype = list()
        
        ########################################################################### 
        """this list is for average cutoff_lv3 normal distribution prototype """ 
        self.t_values_a_cutoff_lv3_prototype = list() 
        self.escape_number_a_cutoff_lv3_prototype = list()
        self.escape_rates_a_cutoff_lv3_prototype = 0.0
        self.last_escape_time_a_cutoff_lv3_prototype = 0
        self.panic_level_a_cutoff_lv3_prototype = list()
        self.interaction_force_a_cutoff_lv3_prototype = list()
        
        ########################################################################### 
        """this list is for average cutoff_lv1 normal distribution prototype """ 
        self.t_values_a_cutoff_lv1_prototype = list() 
        self.escape_number_a_cutoff_lv1_prototype = list()
        self.escape_rates_a_cutoff_lv1_prototype = 0.0
        self.last_escape_time_a_cutoff_lv1_prototype = 0
        self.panic_level_a_cutoff_lv1_prototype = list()
        self.interaction_force_a_cutoff_lv1_prototype = list()
        
          
        ########################################################################### 
        """this list is for uniform cutoff_lv3 distribution prototype """ 
        self.t_values_u_cutoff_lv3_prototype = list() 
        self.escape_number_u_cutoff_lv3_prototype = list()
        self.escape_rates_u_cutoff_lv3_prototype = 0.0
        self.last_escape_time_u_cutoff_lv3_prototype = 0
        self.panic_level_u_cutoff_lv3_prototype = list()
        self.interaction_force_u_cutoff_lv3_prototype = list()
        
        ########################################################################### 
        """this list is for uniform cutoff_lv1 distribution prototype """ 
        self.t_values_u_cutoff_lv1_prototype = list() 
        self.escape_number_u_cutoff_lv1_prototype = list()
        self.escape_rates_u_cutoff_lv1_prototype = 0.0
        self.last_escape_time_u_cutoff_lv1_prototype = 0
        self.panic_level_u_cutoff_lv1_prototype = list()
        self.interaction_force_u_cutoff_lv1_prototype = list()
        
        
        if len(self.parameters['start_areas']) ==1:
            self.observered_duration = constants.total_monitoring_duration_uni_direction
        else:
            self.observered_duration = constants.total_monitoring_duration_bi_direction
           
    def _add_sample(self, prototype_type, t, total_escaped_number,panic_level, interaction_force):     
        # type =1: differential distribution prototype
        # type =2: average distribution prototype
        # type =3: a_cutoff_lv3 distribution prototype
        # type =4: a_cutoff_lv1 distribution prototype 
        # type =5: u_cutoff_lv3 distribution prototype
        # type =6: u_cutoff_lv1 distribution prototype
                 
        if prototype_type ==1:            
            #update escape rate
            if len(self.escape_number_different_distribution_prototype) > 0:
                previous_escape_count = self.escape_number_different_distribution_prototype[-1] #get last element
                if total_escaped_number >  previous_escape_count:
                    self.escape_rates_different_distribution_protype = total_escaped_number/t
                    self.last_escape_time_different_distribution_protype = t
          
            #update time and total escaped number
            self.t_values_different_distribution_prototype.append(t)
            self.escape_number_different_distribution_prototype.append(total_escaped_number)
            self.panic_level_different_distribution_prototype.append(panic_level)
            self.interaction_force_different_distribution_prototype.append(interaction_force)
                  
        elif prototype_type ==2:
            #update escape rate
            if len(self.escape_number_average_prototype) >0:
                previous_escape_count = self.escape_number_average_prototype[-1] #get last element
                if total_escaped_number >  previous_escape_count:
                    self.escape_rates_average_prototype = total_escaped_number/t
                    self.last_escape_time_average_prototype=t
         
            #update time and total escaped number
            self.t_values_average_prototype.append(t)
            self.escape_number_average_prototype.append(total_escaped_number)
            self.panic_level_average_prototype.append(panic_level)
            self.interaction_force_average_prototype.append(interaction_force)
            
        elif prototype_type ==3:
            #update escape rate
            if len(self.escape_number_a_cutoff_lv3_prototype) >0:
                previous_escape_count = self.escape_number_a_cutoff_lv3_prototype[-1] #get last element
                if total_escaped_number >  previous_escape_count:
                    self.escape_rates_a_cutoff_lv3_prototype = total_escaped_number/t
                    self.last_escape_time_a_cutoff_lv3_prototype=t
         
            #update time and total escaped number
            self.t_values_a_cutoff_lv3_prototype.append(t)
            self.escape_number_a_cutoff_lv3_prototype.append(total_escaped_number)
            self.panic_level_a_cutoff_lv3_prototype.append(panic_level)
            self.interaction_force_a_cutoff_lv3_prototype.append(interaction_force)    
            
        elif prototype_type ==4:
            #update escape rate     
            if len(self.escape_number_a_cutoff_lv1_prototype) >0:
                previous_escape_count = self.escape_number_a_cutoff_lv1_prototype[-1] #get last element
                if total_escaped_number >  previous_escape_count:
                    self.escape_rates_a_cutoff_lv1_prototype = total_escaped_number/t
                    self.last_escape_time_a_cutoff_lv1_prototype=t
         
            #update time and total escaped number
            self.t_values_a_cutoff_lv1_prototype.append(t)
            self.escape_number_a_cutoff_lv1_prototype.append(total_escaped_number)
            self.panic_level_a_cutoff_lv1_prototype.append(panic_level)
            self.interaction_force_a_cutoff_lv1_prototype.append(interaction_force) 
            
        elif prototype_type ==5:
            #update escape rate       
            if len(self.escape_number_u_cutoff_lv3_prototype) >0:
                previous_escape_count = self.escape_number_u_cutoff_lv3_prototype[-1] #get last element
                if total_escaped_number >  previous_escape_count:
                    self.escape_rates_u_cutoff_lv3_prototype = total_escaped_number/t
                    self.last_escape_time_u_cutoff_lv3_prototype=t
         
            #update time and total escaped number
            self.t_values_u_cutoff_lv3_prototype.append(t)
            self.escape_number_u_cutoff_lv3_prototype.append(total_escaped_number)
            self.panic_level_u_cutoff_lv3_prototype.append(panic_level)
            self.interaction_force_u_cutoff_lv3_prototype.append(interaction_force)         
            
        elif prototype_type ==6:
            #update escape rate        
            if len(self.escape_number_u_cutoff_lv1_prototype) >0:
                previous_escape_count = self.escape_number_u_cutoff_lv1_prototype[-1] #get last element
                if total_escaped_number >  previous_escape_count:
                    self.escape_rates_u_cutoff_lv1_prototype = total_escaped_number/t
                    self.last_escape_time_u_cutoff_lv1_prototype=t
         
            #update time and total escaped number
            self.t_values_u_cutoff_lv1_prototype.append(t)
            self.escape_number_u_cutoff_lv1_prototype.append(total_escaped_number)
            self.panic_level_u_cutoff_lv1_prototype.append(panic_level)
            self.interaction_force_u_cutoff_lv1_prototype.append(interaction_force)         
                
                      
    def _escape_number_plot(self,simulation_id):

        fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(30,20)) 
        fig.suptitle(r"Simulation Id:=%s" % simulation_id, fontsize=18)
        ax1.set_title(r"$Escape\/number$",fontsize=18)
        ax1.set_ylabel(r'pedestrians')
        ax2.set_title(r"$Interaction\/force\/in\/tracking\/area$",fontsize=18)
        ax2.set_xlabel('time (second)')
        
        ax1.plot(self.t_values_different_distribution_prototype, self.escape_number_different_distribution_prototype,'k.-', label="P$_{differential}\/escape\/rate=%.3f$" %(self.escape_rates_different_distribution_protype))
        ax1.plot(self.t_values_average_prototype, self.escape_number_average_prototype,'r.-', label="P$_{average}\/escape\/rate=%.3f$"%(self.escape_rates_average_prototype))
        ax1.plot(self.t_values_a_cutoff_lv3_prototype, self.escape_number_a_cutoff_lv3_prototype,'b.-', label="P$_{average\/lv3}\/escape\/rate=%.3f$"%(self.escape_rates_a_cutoff_lv3_prototype))
        ax1.plot(self.t_values_a_cutoff_lv1_prototype, self.escape_number_a_cutoff_lv1_prototype,'y.-', label="P$_{average\/lv1}\/escape\/rate=%.3f$"%(self.escape_rates_a_cutoff_lv1_prototype))
        ax1.plot(self.t_values_u_cutoff_lv3_prototype, self.escape_number_u_cutoff_lv3_prototype,'m.-', label="P$_{uniform\/lv3}\/escape\/rate=%.3f$"%(self.escape_rates_u_cutoff_lv3_prototype))
        ax1.plot(self.t_values_u_cutoff_lv1_prototype, self.escape_number_u_cutoff_lv1_prototype,'g.-', label="P$_{uniform\/lv1}\/escape\/rate=%.3f$"%(self.escape_rates_u_cutoff_lv1_prototype))
        ax1.legend(loc='upper left', bbox_to_anchor=(0., 1.02), ncol=1, fancybox=True, shadow=True,prop={'size':11})
        ax1.grid(True)
        
        ax2.plot(self.t_values_different_distribution_prototype, self.interaction_force_different_distribution_prototype,'k.-', label="P$_{differential}$")
        ax2.plot(self.t_values_average_prototype, self.interaction_force_average_prototype,'r.-', label="P$_{average}$")
        ax2.plot(self.t_values_a_cutoff_lv3_prototype, self.interaction_force_a_cutoff_lv3_prototype,'b.-', label="P$_{average\/lv3}$")
        ax2.plot(self.t_values_a_cutoff_lv1_prototype, self.interaction_force_a_cutoff_lv1_prototype,'y.-', label="P$_{average\/lv1}$")
        ax2.plot(self.t_values_u_cutoff_lv3_prototype, self.interaction_force_u_cutoff_lv3_prototype,'m.-', label="P$_{uniform\/lv3}$")
        ax2.plot(self.t_values_u_cutoff_lv1_prototype, self.interaction_force_u_cutoff_lv1_prototype,'g.-', label="P$_{uniform\/lv1}$")
        ax2.legend(loc='upper left', bbox_to_anchor=(0., 1.02), ncol=1, fancybox=True, shadow=True,prop={'size':11})
        ax2.grid(True)
        
        #ax2.set_ylim([0,100])
        
        ax2.set_xticks([x*10 for x in range(0,int((self.observered_duration/10)+1))])
        
        return fig
      
    def _save(self, prefix, simulation_id):
               
        escape_number_fig = self._escape_number_plot(simulation_id)
        if self.observation_mode == 0:
            escape_number_fig.savefig("%s-%s.pdf" % (prefix, simulation_id), dpi=900)  
        else:
            escape_number_fig.savefig(r"%s-%s.pdf" % (prefix, simulation_id), dpi=900)  
        plt.clf()
        plt.close('all')
        
        #self.reset_sample()
    
    """ for differential prototype """
    def _get_escaped_num_different_distribution_prototype(self):
        return self.escape_number_different_distribution_prototype[-1]
                 
    def _get_last_escape_time_different_distribution_protype(self):     
        return self.last_escape_time_different_distribution_protype
    
    """ for average prototype """
    def _get_escaped_num_average_prototype(self):
        return self.escape_number_average_prototype[-1]
    
    def _get_last_escape_time_average_prototype(self):
        return self.last_escape_time_average_prototype 
    
    """ for average cutoff level 3 prototype """
    def _get_escaped_num_a_cutoff_lv3_prototype(self):
        return self.escape_number_a_cutoff_lv3_prototype[-1]
    
    def _get_last_escape_time_a_cutoff_lv3_prototype(self):
        return self.last_escape_time_a_cutoff_lv3_prototype 
    
    """ for average cutoff level 1 prototype """
    def _get_escaped_num_a_cutoff_lv1_prototype(self):
        return self.escape_number_a_cutoff_lv1_prototype[-1]
    
    def _get_last_escape_time_a_cutoff_lv1_prototype(self):
        return self.last_escape_time_a_cutoff_lv1_prototype 
    
    """ for uniform cutoff level 3 prototype """
    def _get_escaped_num_u_cutoff_lv3_prototype(self):
        return self.escape_number_u_cutoff_lv3_prototype[-1]
    
    def _get_last_escape_time_u_cutoff_lv3_prototype(self):
        return self.last_escape_time_u_cutoff_lv3_prototype 
    
    """ for uniform cutoff level 1 prototype """
    def _get_escaped_num_u_cutoff_lv1_prototype(self):
        return self.escape_number_u_cutoff_lv1_prototype[-1]
    
    def _get_last_escape_time_u_cutoff_lv1_prototype(self):
        return self.last_escape_time_u_cutoff_lv1_prototype 
    
    def reset_sample(self):
        
        """this list is for differential prototype """ 
        self.t_values_different_distribution_prototype.clear()
        self.escape_number_different_distribution_prototype.clear()
        self.escape_rates_different_distribution_protype = 0.0
        self.last_escape_time_different_distribution_protype = 0
        self.panic_level_different_distribution_prototype.clear()
        self.interaction_force_different_distribution_prototype.clear()
        
        """this list is for average prototype """ 
        self.t_values_average_prototype.clear()
        self.escape_number_average_prototype.clear()
        self.escape_rates_average_prototype = 0.0
        self.last_escape_time_average_prototype = 0
        self.panic_level_average_prototype.clear()
        self.interaction_force_average_prototype.clear()
        
        """this list is for average cutoff level 3 prototype """ 
        self.t_values_a_cutoff_lv3_prototype.clear()
        self.escape_number_a_cutoff_lv3_prototype.clear()
        self.escape_rates_a_cutoff_lv3_prototype = 0.0
        self.last_escape_time_a_cutoff_lv3_prototype = 0
        self.panic_level_a_cutoff_lv3_prototype.clear()
        self.interaction_force_a_cutoff_lv3_prototype.clear()
                
        """this list is for average cutoff level 1 prototype """ 
        self.t_values_a_cutoff_lv1_prototype.clear()
        self.escape_number_a_cutoff_lv1_prototype.clear()
        self.escape_rates_a_cutoff_lv1_prototype = 0.0
        self.last_escape_time_a_cutoff_lv1_prototype = 0
        self.panic_level_a_cutoff_lv1_prototype.clear()
        self.interaction_force_a_cutoff_lv1_prototype.clear()

        """this list is for uniform cutoff level 3 prototype """ 
        self.t_values_u_cutoff_lv3_prototype.clear()
        self.escape_number_u_cutoff_lv3_prototype.clear()
        self.escape_rates_u_cutoff_lv3_prototype = 0.0
        self.last_escape_time_u_cutoff_lv3_prototype = 0
        self.panic_level_u_cutoff_lv3_prototype.clear()
        self.interaction_force_u_cutoff_lv3_prototype.clear()

        """this list is for uniform cutoff level 1 prototype """ 
        self.t_values_u_cutoff_lv1_prototype.clear()
        self.escape_number_u_cutoff_lv1_prototype.clear()
        self.escape_rates_u_cutoff_lv1_prototype = 0.0
        self.last_escape_time_u_cutoff_lv1_prototype = 0
        self.panic_level_u_cutoff_lv1_prototype.clear()
        self.interaction_force_u_cutoff_lv1_prototype.clear()
