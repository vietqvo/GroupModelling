'''
Created on 9 Mar 2015

@author: quangv
'''
import matplotlib.pyplot as plt
import numpy as np
import constants

class QuantitativePlots:

#http://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
# for observation legend plotting techniques

    def __init__(self,parameters = {}, young_pedestrians =[], adult_pedestrians =[], elderly_pedestrians =[],average_pedestrians =[], total_pedestrians =[]):
        self.parameters = parameters
        
        self.young_pedestrians = young_pedestrians
        self.adult_pedestrians = adult_pedestrians
        self.elderly_pedestrians =  elderly_pedestrians
        self.average_pedestrians = average_pedestrians
        self.total_pedestrians = total_pedestrians
        self.figure_index=0
        
    def _create_pedestrian_type_distribution_plot(self, parameter_name, plotting_name,bin_num,plotting_time):
         
        # extract information based on parameter name
        young_elements = [(young[parameter_name]) for young in self.young_pedestrians]
        adult_elements = [adult[parameter_name] for adult in self.adult_pedestrians]
        elderly_elements = [elder[parameter_name] for elder in self.elderly_pedestrians]
        average_elements = [average[parameter_name] for average in self.average_pedestrians]
        
        min_value = 0.0
        max_value = 0.0
        
        if len(self.young_pedestrians)>0:
            min_value = min(young_elements)
            max_value = max (young_elements)
        if len(self.adult_pedestrians) >0:
            min_value = min(min_value,min(adult_elements))   
            max_value = max(max_value,max(adult_elements))
        if len(self.elderly_pedestrians) >0:
            min_value = min(min_value,min(elderly_elements))      
            max_value = max(max_value,max(elderly_elements))
        
        if len(self.average_pedestrians)>0:
            min_value = min(min_value,min(average_elements))      
            max_value = max(max_value,max(average_elements))
            
        #find mean and max of above three arrays with bin number
        bins = np.linspace(min_value, max_value, bin_num)
        
        self.figure_index+=1
        
        fig = plt.figure(self.figure_index)
        self._annotate_plot(fig, parameter_name, young_elements,adult_elements,elderly_elements,average_elements)
        
      
        if len(self.young_pedestrians)>0:
            weights = np.ones_like(young_elements)/len(young_elements)
            plt.hist(young_elements, bins, histtype='stepfilled', normed=False,weights=weights, facecolor="green",label='Children')      
            
        if len(self.adult_pedestrians) >0:
            weights = np.ones_like(adult_elements)/len(adult_elements)
            plt.hist(adult_elements, bins, histtype='stepfilled', normed=False,weights=weights,facecolor="red", alpha=0.9,label='Adult')
                
        if len(self.elderly_pedestrians) >0:
            weights = np.ones_like(elderly_elements)/len(elderly_elements)
            plt.hist(elderly_elements, bins, histtype='stepfilled', normed=False,weights=weights,facecolor="blue", alpha=0.7,label='Elder')
        
        if len(self.average_pedestrians) >0:
            weights = np.ones_like(average_elements)/len(average_elements)
            plt.hist(average_elements, bins, histtype='stepfilled', normed=False,weights=weights,facecolor="black", alpha=0.7,label='Average')
        
        #plt.title()
        #plt.text(0.5, 1.05, "%s%s" % (plotting_name," Distribution over Pedestrian Type"), horizontalalignment='center', fontsize=8)
        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':8})
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=4, fancybox=True, shadow=True,prop={'size':8})
        plt.xlabel("%s%s" % (plotting_name," Value"))
        plt.ylabel('Probability')
        
        self._save_figure(plt.gcf(),plotting_time,parameter_name) 
    
    def _create_bell_curve_distribution_plot(self, parameter_name, plotting_name,bin_num,plotting_time):
         
        # extract information based on parameter name
        young_elements = [(young[parameter_name]) for young in self.young_pedestrians]
        adult_elements = [adult[parameter_name] for adult in self.adult_pedestrians]
        elderly_elements = [elder[parameter_name] for elder in self.elderly_pedestrians]
        average_elements = [average[parameter_name] for average in self.total_pedestrians]
        
        min_value = 0.0
        max_value = 0.0
        
        if len(self.young_pedestrians)>0:
            min_value = min(young_elements)
            max_value = max (young_elements)
        if len(self.adult_pedestrians) >0:
            min_value = min(min_value,min(adult_elements))   
            max_value = max(max_value,max(adult_elements))
        if len(self.elderly_pedestrians) >0:
            min_value = min(min_value,min(elderly_elements))      
            max_value = max(max_value,max(elderly_elements))
        
        if len(self.average_pedestrians)>0:
            min_value = min(min_value,min(average_elements))      
            max_value = max(max_value,max(average_elements))
            
        #find mean and max of above three arrays with bin number
        bins = np.linspace(min_value, max_value, bin_num)
        
        self.figure_index+=1
        
        fig = plt.figure(self.figure_index)
        self._annotate_plot(fig, parameter_name, young_elements,adult_elements,elderly_elements,average_elements)
        
      
        if len(self.young_pedestrians)>0:
            mu = np.mean(young_elements)
            sigma = round(np.std(young_elements),4)   
            if sigma != 0.0: 
                plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *  np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='green',label='Children')  
            
                
        if len(self.adult_pedestrians) >0:
            mu = np.mean(adult_elements)
            sigma = round(np.std(adult_elements),4)
            if sigma != 0.0:     
                plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *  np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='red',label='Adult')  
                
        if len(self.elderly_pedestrians) >0:
            mu = np.mean(elderly_elements)
            sigma = round(np.std(elderly_elements),4)
            if sigma != 0.0:     
                plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *  np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='blue',label='Elder')  
             
        if len(self.average_pedestrians) >0:
            mu = np.mean(average_elements)
            sigma = round(np.std(average_elements),4)    
            if sigma != 0.0: 
                plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *  np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=2, color='black',label='Average')  
            
        #plt.title("%s%s" % (plotting_name," Distribution over Pedestrian Type"))
        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':8})
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=4, fancybox=True, shadow=True,prop={'size':8})
        #plt.xlabel('Value')
        plt.xlabel("%s%s" % (plotting_name," Value"))
        self._save_figure(plt.gcf(),plotting_time,("%s%s" %(parameter_name,"_bellcurve"))) 
     
            
    def _annotate_plot(self,fig, parameter_name, young_elements,adult_elements,elderly_elements,average_elements):
        fig.set_size_inches(10,5)
        ax = fig.gca()
        param_text = []

        if len(self.young_pedestrians)>0:
            param_text.append("${P1}:\t \mu_{children}=%.4f, \sigma_{children}=%.2f$" % (np.mean(young_elements),np.std(young_elements)))
            #param_text.append(self._generate_anotate_mean_sigma(0,parameter_name))              
        if len(self.adult_pedestrians)>0:
            param_text.append("$\mu_{adult}=%.4f, \sigma_{adult}=%.2f$" % (np.mean(adult_elements),np.std(adult_elements)))
            #param_text.append(self._generate_anotate_mean_sigma(1,parameter_name))      
       
        if len(self.elderly_pedestrians)>0:
            param_text.append("$\mu_{elder}=%.4f, \sigma_{elder}=%.2f$" % (np.mean(elderly_elements),np.std(elderly_elements)))
            #param_text.append(self._generate_anotate_mean_sigma(2,parameter_name))     
                   
        if len(self.average_pedestrians)>0:
            #param_text.append("$\mu_{average}=%.3f, \sigma_{average}=%.2f$" % (np.mean(average_elements),np.std(average_elements)))
            
            param_text.append("%s%s" % ("${P2}:\t", self._generate_probability_distribution_anotate_mean_sigma(3,parameter_name)))     
      
        ax.text(0.98, 0.85, "\n".join(param_text),
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif'},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
   
    def _save_figure(self,figure, strTime,figure_name):
        prefix = self.parameters['quantification_plot_prefix']
        figure.savefig("%s-%s-%s.pdf" % (prefix, strTime,figure_name))
     
    def _show_plot(self):
        plt.show()        
    
    def _generate_probability_distribution_anotate_mean_sigma(self, pedestrian_type, parameter_name):
        
        if pedestrian_type ==0:
            if parameter_name =="initial_desired_velocity":
                return "$\mu_{children}=%.4f, \sigma_{children}=%.2f$" % (self.parameters['young_velocity_mean'],self.parameters['young_velocity_deviation'])
            
            if parameter_name =="relax_time":
                return "$\mu_{children}=%.4f, \sigma_{children}=%.2f$" % (self.parameters['young_relaxation_mean'],self.parameters['young_relaxation_deviation'])
            
            if parameter_name == "interaction_constant":
                return "$\mu_{children}=%.4f, \sigma_{children}=%.2f$" % (self.parameters['young_force_unit'],self.parameters['young_force_deviation'])
            
            if parameter_name == "interaction_distance":
                return "$\mu_{children}=%.4f, \sigma_{children}=%.2f$" % (self.parameters['young_force_range'],self.parameters['young_range_deviation'])
      
        if pedestrian_type == 1:
            if parameter_name =="initial_desired_velocity":
                return "$\mu_{adult}=%.4f, \sigma_{adult}=%.2f$" % (self.parameters['adult_velocity_mean'],self.parameters['adult_velocity_deviation'])
            
            if parameter_name =="relax_time":
                return "$\mu_{adult}=%.4f, \sigma_{adult}=%.2f$" % (self.parameters['adult_relaxation_mean'],self.parameters['adult_relaxation_deviation'])
            
            if parameter_name == "interaction_constant":
                return "$\mu_{adult}=%.4f, \sigma_{adult}=%.2f$" % (self.parameters['adult_force_unit'],self.parameters['adult_force_deviation'])
            
            if parameter_name == "interaction_distance":
                return "$\mu_{adult}=%.4f, \sigma_{adult}=%.2f$" % (self.parameters['adult_force_range'],self.parameters['adult_range_deviation'])
                
        if pedestrian_type ==2:
            if parameter_name =="initial_desired_velocity":
                return "$\mu_{elder}=%.4f, \sigma_{elder}=%.2f$" % (self.parameters['elderly_velocity_mean'],self.parameters['elderly_velocity_deviation'])
            
            if parameter_name =="relax_time":
                return "$\mu_{elder}=%.4f, \sigma_{elder}=%.2f$" % (self.parameters['elderly_relaxation_mean'],self.parameters['elderly_relaxation_deviation'])
            
            if parameter_name == "interaction_constant":
                return "$\mu_{elder}=%.4f, \sigma_{elder}=%.2f$" % (self.parameters['elderly_force_unit'],self.parameters['elderly_force_deviation'])
            
            if parameter_name == "interaction_distance":
                return "$\mu_{elder}=%.4f, \sigma_{elder}=%.2f$" % (self.parameters['elderly_force_range'],self.parameters['elderly_force_range'])
        
        if pedestrian_type ==3:
            if parameter_name =="initial_desired_velocity":
                pedestrians_velocities = [(pedestrian['initial_desired_velocity']) for pedestrian in self.total_pedestrians]
                return " \mu_{average}=%.4f, \sigma_{average}=%.2f$" % (np.mean(pedestrians_velocities),np.std(pedestrians_velocities))
            
            if parameter_name =="relax_time":
                pedestrians_acceleration_time = [(pedestrian['relax_time']) for pedestrian in self.total_pedestrians]
                return " \mu_{average}=%.4f, \sigma_{average}=%.2f$" % (np.mean(pedestrians_acceleration_time),np.std(pedestrians_acceleration_time))
            
            if parameter_name == "interaction_constant":
                pedestrians_interaction_strength = [(pedestrian['interaction_constant']) for pedestrian in self.total_pedestrians]
                return " \mu_{average}=%.4f, \sigma_{average}=%.2f$" % (np.mean(pedestrians_interaction_strength),np.std(pedestrians_interaction_strength))
            
            if parameter_name == "interaction_distance":
                pedestrians_interaction_distance = [(pedestrian['interaction_distance']) for pedestrian in self.total_pedestrians]
                return " \mu_{average}=%.4f, \sigma_{average}=%.2f$" % (np.mean(pedestrians_interaction_distance),np.std(pedestrians_interaction_distance))
  
        return ""           