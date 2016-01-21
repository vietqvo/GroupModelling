'''
Created on 9 Mar 2015

@author: quangv
'''
import matplotlib.pyplot as plt
import numpy as np

class DistributionPlot:

    def __init__(self,parameters = {}):
        self.parameters = parameters
     
        
    def _create_pedestrian_type_parameter_distribution_plot(self, plotting_name, bin_num,                                                
                                                  ### for differential prototype          
                                                  young_mean, young_std, young_elements, 
                                                  adult_mean, adult_std, adults_elements,
                                                  elder_mean, elder_std, elderly_elements,                                                                                                
                                                  ### for average prototype
                                                  average_mean, average_std, average_elements,
                                                  plotting_time
                                                  ):
         
               
            
        fig, (ax1, ax2) = plt.subplots(2,figsize=(10,10),sharex=True, sharey=True) 
                                                           
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
                  
        self._annotate_plot(ax1, ax2,
                            young_elements,adults_elements,elderly_elements,
                            average_elements                      
                            )
            
        if len(young_elements)>0:
            weights = np.ones_like(young_elements)/len(young_elements)
            ax1.hist(young_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="green",alpha=0.8, label='$Children\/members(\mu = %.2f,\/\sigma= %.3f)$'%(young_mean,young_std))      
                
        if len(adults_elements) >0:
            weights = np.ones_like(adults_elements)/len(adults_elements)
            ax1.hist(adults_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="red", alpha=0.9, label='$Adult\/members(\mu = %.2f,\/\sigma= %.3f)$'%(adult_mean,adult_std))
                    
        if len(elderly_elements) >0:
            weights = np.ones_like(elderly_elements)/len(elderly_elements)
            ax1.hist(elderly_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="blue",alpha=0.9, label='$Elder\/members(\mu = %.2f,\/\sigma= %.3f)$'%(elder_mean,elder_std))
        
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=3, fancybox=True, shadow=True,prop={'size':11})
        ax1.set_title("%s" % plotting_name)
        ax1.set_ylabel('Probability')
                   
        if len(average_elements) >0:
            weights = np.ones_like(average_elements)/len(average_elements)
            ax2.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='Out-group\/pedestrians $(\mu = %.3f,\/\sigma= %.3f)$'%(average_mean,average_std))
            ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=1, fancybox=True, shadow=True,prop={'size':11})
            ax2.set_ylabel('Probability')
                
        self._save_figure(plotting_time,plotting_name)
        
    def _annotate_plot(self,
                       ax1, ax2,
                       young_elements,adults_elements,elderly_elements, 
                       average_elements
                       ):

        ax1_param_text = []
        ax2_param_text = []
      
        
        ax1_param_text.append("$group\/members \t \t$")
        ax2_param_text.append("$out-group\/pedestrians \t \t$")
      
                          
        if len(young_elements)>0:
            ax1_param_text.append("$\mu_{children}=%.4f, \sigma_{children}=%.3f$" % (np.mean(young_elements),np.std(young_elements)))
            ax1_param_text.append("$min_{children}=%.3f, max_{children}=%.3f$" % (min(young_elements),max(young_elements)))
            
        if len(adults_elements)>0:
            ax1_param_text.append("$\mu_{adult}=%.4f, \sigma_{adult}=%.3f$" % (np.mean(adults_elements),np.std(adults_elements)))
            ax1_param_text.append("$min_{adult}=%.3f, max_{adult}=%.3f$" % (min(adults_elements),max(adults_elements)))
             
        if len(elderly_elements)>0:
            ax1_param_text.append("$\mu_{elder}=%.4f, \sigma_{elder}=%.3f$" % (np.mean(elderly_elements),np.std(elderly_elements)))
            ax1_param_text.append("$min_{elder}=%.3f, max_{elder}=%.3f$" % (min(elderly_elements),max(elderly_elements)))
            
        if len(average_elements)>0:
            ax2_param_text.append("$\mu_{average}=%.4f, \sigma_{average}=%.3f$" % (np.mean(average_elements),np.std(average_elements)))           
            ax2_param_text.append("$min_{average}=%.3f, max_{average}=%.3f$" % (min(average_elements),max(average_elements)))
        
        ax1.text(0.98, 0.95, "\n".join(ax1_param_text),
                transform=ax1.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
        
        ax2.text(0.98, 0.95, "\n".join(ax2_param_text),
                transform=ax2.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
      
            
    def _save_figure(self, plotting_time, prefix_name):
        prefix = self.parameters['quantification_plot_prefix']
        figure = plt.gcf()
        figure.savefig("%s-%s-%s.pdf" % (prefix, plotting_time, prefix_name))        
        plt.clf()
        plt.close('all')
    
    