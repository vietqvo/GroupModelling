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
        
    def _create_pedestrian_type_parameter_distribution_plot(self, plotting_name, bin_num,
                                                  young_mean, young_std, young_elements, 
                                                  elder_mean, elder_std, elderly_elements,
                                                  average_mean, average_std, average_elements,  average_uniform_notation= False):
         
        min_value = 0.0
        max_value = 0.0
        
        if len(young_elements)>0:
            min_value = min(young_elements)
            max_value = max (young_elements)
         
        if len(elderly_elements) >0:
            min_value = min(min_value,min(elderly_elements))      
            max_value = max(max_value,max(elderly_elements))
        
        if len(average_elements)>0:
            min_value = min(min_value,min(average_elements))      
            max_value = max(max_value,max(average_elements))
            
        #find mean and max of above three arrays with bin number
        bins = np.linspace(min_value, max_value, bin_num)
        
        if self.index == 0:    
            self._annotate_plot(self.ax1, young_elements,elderly_elements,average_elements)
            
            if len(young_elements)>0:
                weights = np.ones_like(young_elements)/len(young_elements)
                self.ax1.hist(young_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="green",alpha=0.8, label='Children $(\mu = %.2f,\/\sigma= %.3f)$'%(young_mean,young_std))      
                
            if len(elderly_elements) >0:
                weights = np.ones_like(elderly_elements)/len(elderly_elements)
                self.ax1.hist(elderly_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="blue",alpha=0.9, label='Elder $(\mu = %.2f,\/\sigma= %.3f)$'%(elder_mean,elder_std))
            
            if len(average_elements) >0:
                weights = np.ones_like(average_elements)/len(average_elements)
                if average_uniform_notation ==False:
                    self.ax1.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='Average $(\mu = %.3f,\/\sigma= %.3f)$'%(average_mean,average_std))
                else:
                    self.ax1.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='Average $[r_{1} = %.3f,\/r_{2}= %.3f]$'%(average_mean,average_std))
             
                self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.04), ncol=4, fancybox=True, shadow=True,prop={'size':12})
                self.ax1.set_title("%s" % plotting_name)
                
                self.ax1.set_ylabel('Probability')
            
            self.index +=1
        
        elif self.index == 1:    
            self._annotate_plot(self.ax2, young_elements,elderly_elements,average_elements)
            
            if len(young_elements)>0:
                weights = np.ones_like(young_elements)/len(young_elements)
                self.ax2.hist(young_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="green",alpha=0.8, label='Children $(\mu = %.2f,\/\sigma= %.3f)$'%(young_mean,young_std))      
       
            if len(elderly_elements) >0:
                weights = np.ones_like(elderly_elements)/len(elderly_elements)
                self.ax2.hist(elderly_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="blue",alpha=0.9, label='Elder $(\mu = %.2f,\/\sigma= %.3f)$'%(elder_mean,elder_std))
            
            if len(average_elements) >0:
                weights = np.ones_like(average_elements)/len(average_elements)
                if average_uniform_notation ==False:
                    self.ax2.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='Average $(\mu = %.3f,\/\sigma= %.3f)$'%(average_mean,average_std))
                else:
                    self.ax2.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='Average $[r_{1} = %.3f,\/r_{2}= %.3f]$'%(average_mean,average_std))
             
                self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.04), ncol=4, fancybox=True, shadow=True,prop={'size':12})
                self.ax2.set_title("%s" % plotting_name)
                
                self.ax2.set_ylabel('Probability')
            
            self.index +=1
 
    def _annotate_plot(self,ax, young_elements,elderly_elements,average_elements):

        param_text = []

        param_text.append("$P_{different} \t \t$")
                          
        if len(young_elements)>0:
            param_text.append("$\mu_{children}=%.4f, \sigma_{children}=%.3f$" % (np.mean(young_elements),np.std(young_elements)))
            param_text.append("$min_{children}=%.3f, max_{children}=%.3f$" % (min(young_elements),max(young_elements)))
            
        if len(elderly_elements)>0:
            param_text.append("$\mu_{elder}=%.4f, \sigma_{elder}=%.3f$" % (np.mean(elderly_elements),np.std(elderly_elements)))
            param_text.append("$min_{elder}=%.3f, max_{elder}=%.3f$" % (min(elderly_elements),max(elderly_elements)))
            
        if len(average_elements)>0:
            param_text.append("$P_{average} \t \t$")
            param_text.append("$\mu_{average}=%.4f, \sigma_{average}=%.3f$" % (np.mean(average_elements),np.std(average_elements)))           
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
    