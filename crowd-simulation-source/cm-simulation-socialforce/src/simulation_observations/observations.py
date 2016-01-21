'''
Created on 1 Mar 2015

@author: quangv
'''

import matplotlib.pyplot as plt
from src import constants

class ObservationPlots:

    def __init__(self, parameters, observation_mode=0): #0:new simulation mode #1: replay mode):
        self.parameters = parameters
        self.observation_mode =  observation_mode
        
        """ this list is for different distribution prototype """
        self.t_values_different_distribution_prototype = list()
        self.escape_number_different_distribution_prototype = list() 
        self.escape_rates_different_distribution_protype = 0.0
        self.last_escape_time_different_distribution_protype = 0
        ########################################################################### 
        """this list is for average prototype """ 
        self.t_values_average_prototype = list()
        self.escape_number_average_prototype = list()
        self.escape_rates_average_prototype = 0.0
        self.last_escape_time_average_prototype = 0
        
        
        if len(self.parameters['start_areas']) ==1:
            self.observered_duration = constants.total_monitoring_duration_uni_direction
        else:
            self.observered_duration = constants.total_monitoring_duration_bi_direction
           
    def _add_sample(self, prototype_type, t, total_escaped_number):     
        # type =1: different distribution prototype
        # type =2: average distribution prototype
              
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
         
            
    def _create_plot(self, title, xlabel, ylabel,width, height):
        fig = plt.figure()
        fig.set_size_inches(width,height)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        return fig
            
    def _escape_number_plot(self,simulation_id):
        fig = self._create_plot("Simulation Id:=%s" % simulation_id, 
                "time (s)", "pedestrians", 30,5)
        plt.plot(self.t_values_different_distribution_prototype, self.escape_number_different_distribution_prototype,'k.-', label="P$_{different}\/escape\/rate=%.3f$" %(self.escape_rates_different_distribution_protype))
        plt.plot(self.t_values_average_prototype, self.escape_number_average_prototype,'r.-', label="P$_{average}\/escape\/rate=%.3f$"%(self.escape_rates_average_prototype))
        plt.xticks([x*10 for x in range(0,int((self.observered_duration/10)+1))])
        plt.legend(loc='upper left', bbox_to_anchor=(0., 1.02), ncol=1, fancybox=True, shadow=True,prop={'size':11})
        plt.grid(True)
        return fig
      
    def _save(self, prefix, simulation_id):
               
        escape_number_fig = self._escape_number_plot(simulation_id)
        if self.observation_mode == 0:
            escape_number_fig.savefig("%s-%s.pdf" % (prefix, simulation_id), dpi=900)  
        else:
            escape_number_fig.savefig(r"%s-%s.pdf" % (prefix, simulation_id), dpi=900)  
        plt.clf()
        plt.close('all')
    
    def _get_escaped_num_different_distribution_prototype(self):
        return self.escape_number_different_distribution_prototype[-1]
                 
    def _get_last_escape_time_different_distribution_protype(self):     
        return self.last_escape_time_different_distribution_protype
    
    def _get_escape_rate_different_distribution_protype(self):    
        return self.escape_rates_different_distribution_protype
 
    def _get_escaped_num_average_prototype(self):
        return self.escape_number_average_prototype[-1]
    
    def _get_last_escape_time_average_prototype(self):
        return self.last_escape_time_average_prototype
           
    def _get_escape_rate_average_prototype(self):
        return self.escape_rates_average_prototype
    
    def _show(self):
        plt.show()    