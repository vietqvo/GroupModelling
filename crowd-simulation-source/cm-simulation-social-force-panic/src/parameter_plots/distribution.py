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
                                                  
                                                  ### for average cutoff_level 3_normal prototype
                                                  average_cutoff_3_mean, average_cutoff_3_std,
                                                  average_cutoff_3_low_value, average_cutoff_3_high_value, average_cutoff_3_elements,
                                                  
                                                  ### for average cutoff_level 3_normal prototype
                                                  average_cutoff_1_mean, average_cutoff_1_std,
                                                  average_cutoff_1_low_value, average_cutoff_1_high_value, average_cutoff_1_elements,
                                                
                                                  ### for uniform cutoff_level 3
                                                  uni_cutoff_3_low_value, uni_cutoff_3_high_value, uniform_cutoff_3_elements,
                                                  
                                                  ### for uniform cutoff_level 1
                                                  uni_cutoff_1_low_value, uni_cutoff_1_high_value, uniform_cutoff_1_elements,
                                                  
                                                  plotting_time
                                                  ):
         
               
            
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6,figsize=(18,20),sharex=True, sharey=True) 
                                                           
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
            
        if len(average_cutoff_3_elements)>0:
            min_value = min(min_value,min(average_cutoff_3_elements))      
            max_value = max(max_value,max(average_cutoff_3_elements))
        
        if len(average_cutoff_1_elements)>0:
            min_value = min(min_value,min(average_cutoff_1_elements))      
            max_value = max(max_value,max(average_cutoff_1_elements))
             
        if len(uniform_cutoff_3_elements)>0:
            min_value = min(min_value,min(uniform_cutoff_3_elements))      
            max_value = max(max_value,max(uniform_cutoff_3_elements))
        
        if len(uniform_cutoff_1_elements)>0:
            min_value = min(min_value,min(uniform_cutoff_1_elements))      
            max_value = max(max_value,max(uniform_cutoff_1_elements))
               
        #find mean and max of above three arrays with bin number
        bins = np.linspace(min_value, max_value, bin_num)
                  
        self._annotate_plot(ax1, ax2, ax3, ax4, ax5, ax6,
                            young_elements,adults_elements,elderly_elements,
                            average_elements,
                            average_cutoff_3_elements,
                            average_cutoff_1_elements,
                            uniform_cutoff_3_elements,
                            uniform_cutoff_1_elements
                            )
            
        if len(young_elements)>0:
            weights = np.ones_like(young_elements)/len(young_elements)
            ax1.hist(young_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="green",alpha=0.8, label='Children $(\mu = %.2f,\/\sigma= %.3f)$'%(young_mean,young_std))      
                
        if len(adults_elements) >0:
            weights = np.ones_like(adults_elements)/len(adults_elements)
            ax1.hist(adults_elements, bins, histtype='bar', normed=False,weights=weights, facecolor="red", alpha=0.9, label='Adult $(\mu = %.2f,\/\sigma= %.3f)$'%(adult_mean,adult_std))
                    
        if len(elderly_elements) >0:
            weights = np.ones_like(elderly_elements)/len(elderly_elements)
            ax1.hist(elderly_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="blue",alpha=0.9, label='Elder $(\mu = %.2f,\/\sigma= %.3f)$'%(elder_mean,elder_std))
        
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=3, fancybox=True, shadow=True,prop={'size':12})
        ax1.set_title("%s" % plotting_name)
        ax1.set_ylabel('Probability')
                   
        if len(average_elements) >0:
            weights = np.ones_like(average_elements)/len(average_elements)
            ax2.hist(average_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="black", alpha=0.9, label='Average $(\mu = %.3f,\/\sigma= %.3f)$'%(average_mean,average_std))
            ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=1, fancybox=True, shadow=True,prop={'size':12})
            ax2.set_ylabel('Probability')
                
        if len(average_cutoff_3_elements) >0:
            weights = np.ones_like(average_cutoff_3_elements)/len(average_cutoff_3_elements)
            ax3.hist(average_cutoff_3_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="blue", alpha=0.9, label='Average $(\mu = %.3f,\/\sigma= %.3f),[r_{1} = %.3f,\/r_{2}= %.3f]$'%(average_cutoff_3_mean,average_cutoff_3_std,average_cutoff_3_low_value,average_cutoff_3_high_value))
            ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=1, fancybox=True, shadow=True,prop={'size':12})
            ax3.set_ylabel('Probability')
        
        if len(average_cutoff_1_elements) >0:
            weights = np.ones_like(average_cutoff_1_elements)/len(average_cutoff_1_elements)
            ax4.hist(average_cutoff_1_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="green", alpha=0.9, label='Average $(\mu = %.3f,\/\sigma= %.3f),[r_{1} = %.3f,\/r_{2}= %.3f]$'%(average_cutoff_1_mean,average_cutoff_1_std,average_cutoff_1_low_value,average_cutoff_1_high_value))
            ax4.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=1, fancybox=True, shadow=True,prop={'size':12})
            ax4.set_ylabel('Probability')            
        
        if len(uniform_cutoff_3_elements) >0:
            weights = np.ones_like(uniform_cutoff_3_elements)/len(uniform_cutoff_3_elements)
            ax5.hist(uniform_cutoff_3_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="yellow", alpha=0.9, label='Uniform $[r_{1} = %.3f,\/r_{2}= %.3f]$'%(uni_cutoff_3_low_value,uni_cutoff_3_high_value))
            ax5.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=1, fancybox=True, shadow=True,prop={'size':12})
            ax5.set_ylabel('Probability')            
        
        if len(uniform_cutoff_1_elements) >0:
            weights = np.ones_like(uniform_cutoff_1_elements)/len(uniform_cutoff_1_elements)
            ax6.hist(uniform_cutoff_1_elements, bins, histtype='bar', normed=False,weights=weights,facecolor="red", alpha=0.9, label='Uniform $[r_{1} = %.3f,\/r_{2}= %.3f]$'%(uni_cutoff_1_low_value,uni_cutoff_1_high_value))
            ax6.legend(loc='upper center', bbox_to_anchor=(0.5, 1.06), ncol=1, fancybox=True, shadow=True,prop={'size':12})
            ax6.set_ylabel('Probability')            
         
        
        self._save_figure(plotting_time,plotting_name)
        
    def _annotate_plot(self,
                       ax1, ax2, ax3, ax4, ax5, ax6,
                       young_elements,adults_elements,elderly_elements, 
                       average_elements,
                       average_cutoff_3_elements,
                       average_cutoff_1_elements,
                       uniform_cutoff_3_elements,
                       uniform_cutoff_1_elements
                       ):

        ax1_param_text = []
        ax2_param_text = []
        ax3_param_text = []
        ax4_param_text = []
        ax5_param_text = []
        ax6_param_text = []
        
        ax1_param_text.append("$P_{differential} \t \t$")
        ax2_param_text.append("$P_{average} \t \t$")
        ax3_param_text.append("$P_{average\/lv3} \t \t$")
        ax4_param_text.append("$P_{average\/lv1} \t \t$")
        ax5_param_text.append("$P_{uniform\/lv3} \t \t$")
        ax6_param_text.append("$P_{uniform\/lv1} \t \t$")
                          
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
        
        if len(average_cutoff_3_elements)>0:
            ax3_param_text.append("$\mu_{average\/lv3}=%.4f, \sigma_{average\/lv3}=%.3f$" % (np.mean(average_cutoff_3_elements),np.std(average_cutoff_3_elements)))           
            ax3_param_text.append("$min_{average\/lv3}=%.3f, max_{average\/lv3}=%.3f$" % (min(average_cutoff_3_elements),max(average_cutoff_3_elements)))
            
            
        if len(average_cutoff_1_elements)>0:
            ax4_param_text.append("$\mu_{average\/lv1}=%.4f, \sigma_{average\/lv1}=%.3f$" % (np.mean(average_cutoff_1_elements),np.std(average_cutoff_1_elements)))           
            ax4_param_text.append("$min_{average\/lv1}=%.3f, max_{average\/lv1}=%.3f$" % (min(average_cutoff_1_elements),max(average_cutoff_1_elements)))
           
        if len(uniform_cutoff_3_elements)>0:
            ax5_param_text.append("$\mu_{uniform\/lv3}=%.4f, \sigma_{uniform\/lv3}=%.3f$" % (np.mean(uniform_cutoff_3_elements),np.std(uniform_cutoff_3_elements)))           
            ax5_param_text.append("$min_{uniform\/lv3}=%.3f, max_{uniform\/lv3}=%.3f$" % (min(uniform_cutoff_3_elements),max(uniform_cutoff_3_elements)))
        
        if len(uniform_cutoff_1_elements)>0:
            ax6_param_text.append("$\mu_{uniform\/lv1}=%.4f, \sigma_{uniform\/lv1}=%.3f$" % (np.mean(uniform_cutoff_1_elements),np.std(uniform_cutoff_1_elements)))           
            ax6_param_text.append("$min_{uniform\/lv1}=%.3f, max_{uniform\/lv1}=%.3f$" % (min(uniform_cutoff_1_elements),max(uniform_cutoff_1_elements)))
       
         
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
        
        ax3.text(0.98, 0.95, "\n".join(ax3_param_text),
                transform=ax3.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
         
        ax4.text(0.98, 0.95, "\n".join(ax4_param_text),
                transform=ax4.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
        
        ax5.text(0.98, 0.95, "\n".join(ax5_param_text),
                transform=ax5.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
          
        ax6.text(0.98, 0.95, "\n".join(ax6_param_text),
                transform=ax6.transAxes,
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
    
    