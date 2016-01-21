'''
Created on 9 Mar 2015

@author: quangv
'''
import matplotlib.pyplot as plt
import numpy as np

class DistributionPlot:

    def __init__(self,parameters = {}):
        self.parameters = parameters
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(2,figsize=(18,20)) 
        self.index = 0
        
    def _create_pedestrian_type_parameter_distribution_plot(self, plotting_name, bin_num, average_elements):
         
        min_value = 0.0
        max_value = 0.0
      
        if len(average_elements)>0:
            min_value = min(min_value,min(average_elements))      
            max_value = max(max_value,max(average_elements))
            
            #find mean and max of above three arrays with bin number
            bins = np.linspace(min_value, max_value, bin_num)
        
            if self.index == 0:    
                self._annotate_plot(self.ax1, average_elements)
            
                weights = np.ones_like(average_elements)/len(average_elements)
                self.ax1.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='$Average$')
             
                self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.04), ncol=1, fancybox=True, shadow=True,prop={'size':12})
                self.ax1.set_title("%s" % plotting_name)
                
                self.ax1.set_ylabel('Probability')
            
                self.index +=1
        
            elif self.index == 1:    
                self._annotate_plot(self.ax2,average_elements)
            
                weights = np.ones_like(average_elements)/len(average_elements)
                self.ax2.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='$Average$')
             
                self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.04), ncol=1, fancybox=True, shadow=True,prop={'size':12})
                self.ax2.set_title("%s" % plotting_name)
                
                self.ax2.set_ylabel('Probability')
        
                self.index +=1
 
    def _annotate_plot(self,ax, average_elements):

        param_text = []

        param_text.append("$P_{average} \t \t$")     
        param_text.append("$min_{average}=%.3f, max_{average}=%.3f$" % (min(average_elements),max(average_elements)))
            
        ax.text(0.98, 0.95, "\n".join(param_text),
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
   
    def _save_figure(self, plotting_time):
        prefix = self.parameters['quantification_plot_prefix']
        figure = plt.gcf()
        figure.savefig("%s-%s.pdf" % (prefix, plotting_time))        
        plt.clf()
        plt.close('all')
        
    def _show_plot(self):
        plt.show()        
    