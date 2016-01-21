'''
Created on 9 Mar 2015

@author: quangv
'''
import matplotlib.pyplot as plt
import numpy as np
import datetime

class DistributionPlot:

    def __init__(self,parameters = {}):
        self.parameters = parameters
        
        now = datetime.datetime.now()
        self.figure_index= now.hour + now.minute + now.second
        
    def _create_pedestrian_type_parameter_distribution_plot(self, parameter_name, plotting_name, bin_num,
                                                  young_mean, young_std, young_elements, 
                                                  adult_mean, adult_std, adults_elements,
                                                  elder_mean, elder_std, elderly_elements,
                                                  average_mean, average_std, average_elements,
                                                  plotting_time):
         
        min_value = 0.0
        max_value = 0.0
        
        if len(young_elements)>0:
            min_value = min(young_elements)
            max_value = max (young_elements)
        
        if len(adults_elements)>0:
            min_value = min(min_value,min(adults_elements))   
            max_value = max(max_value,max(adults_elements))
        
        if len(elderly_elements) >0:
            min_value = min(min_value,min(elderly_elements))      
            max_value = max(max_value,max(elderly_elements))
        
        if len(average_elements)>0:
            min_value = min(min_value,min(average_elements))      
            max_value = max(max_value,max(average_elements))
            
        #find mean and max of above three arrays with bin number
        bins = np.linspace(min_value, max_value, bin_num)
        
        self.figure_index+=1       
        fig = plt.figure(self.figure_index)
        
        self._annotate_plot(fig, young_elements,adults_elements,elderly_elements,average_elements)
        
       
        if len(young_elements)>0:
            weights = np.ones_like(young_elements)/len(young_elements)
            plt.hist(young_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="green",alpha=0.8, label='Children $(\mu = %.2f,\sigma= %.3f)$'%(young_mean,young_std))      
            
        if len(adults_elements) >0:
            weights = np.ones_like(adults_elements)/len(adults_elements)
            plt.hist(adults_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="red", alpha=0.9,label='Adult $(\mu = %.2f,\sigma= %.3f)$'%(adult_mean,adult_std))
                
        if len(elderly_elements) >0:
            weights = np.ones_like(elderly_elements)/len(elderly_elements)
            plt.hist(elderly_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="blue",alpha=0.9, label='Elder $(\mu = %.2f,\sigma= %.3f)$'%(elder_mean,elder_std))
        
        if len(average_elements) >0:
            weights = np.ones_like(average_elements)/len(average_elements)
            plt.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9,label='Average $(\mu = %.2f,\sigma= %.3f)$'%(average_mean,average_std))
        
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=4, fancybox=True, shadow=True,prop={'size':8})
        plt.xlabel("%s%s" % (plotting_name," Value"))
        plt.ylabel('Probability')
        
        self._save_figure(plt.gcf(),plotting_time,parameter_name) 
    
   
    def _annotate_plot(self,fig, young_elements,adults_elements,elderly_elements,average_elements):
        fig.set_size_inches(10,6)
        ax = fig.gca()
        param_text = []

        param_text.append("$P_{different} \t \t$")
                          
        if len(young_elements)>0:
            param_text.append("$\mu_{children}=%.4f, \sigma_{children}=%.3f$" % (np.mean(young_elements),np.std(young_elements)))
   
        if len(adults_elements)>0:
            param_text.append("$\mu_{adult}=%.4f, \sigma_{adult}=%.3f$" % (np.mean(adults_elements),np.std(adults_elements)))
     
        if len(elderly_elements)>0:
            param_text.append("$\mu_{elder}=%.4f, \sigma_{elder}=%.3f$" % (np.mean(elderly_elements),np.std(elderly_elements)))
        
        if len(average_elements)>0:
            param_text.append("$P_{average} \t \t$")
            param_text.append("$\mu_{average}=%.3f, \sigma_{average}=%.3f$" % (np.mean(average_elements),np.std(average_elements)))           
      
        ax.text(0.98, 0.85, "\n".join(param_text),
                transform=ax.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif'},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
   
    def _save_figure(self,figure, plotting_time,parameter_name):
        prefix = self.parameters['quantification_plot_prefix']
        figure.savefig("%s-%s-%s.pdf" % (prefix, plotting_time,parameter_name))        
        plt.clf()
        plt.close('all')
        
    def _show_plot(self):
        plt.show()        
    