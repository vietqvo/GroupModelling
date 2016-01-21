'''
Created on 27 Apr 2015

@author: quangv
'''

import matplotlib.pyplot as plt
from src import constants

class Pedestrian_Track:

    def __init__(self, pedestrian_id=0, initial_desired_velocity=0.0, max_velocity=0.0, relax_time=0.0):
        import matplotlib as mpl
        #Use true LaTeX and bigger font
        mpl.rc('text', usetex=True)
        # Include packages `amssymb` and `amsmath` in LaTeX preamble
        # as they include extended math support (symbols, envisonments etc.)
        mpl.rcParams['text.latex.preamble']=[r"\usepackage{amssymb}",r"\usepackage{amsmath}"]
                                             
                                             
        self.pedestrian_id = pedestrian_id
      
        self.t_values = list()
        
        """ desired-force component"""
        self.initial_desired_velocity = initial_desired_velocity
        self.max_velocity = max_velocity
        self.relax_time = relax_time
        
        self.velocities = list()
        self.panic_levels = list()
        self.desired_velocities = list()
        self.desired_force_values = list()
        
        """ interaction-force component"""
        self.interaction_force_values = list()
        
        """ obstacle-force component"""
        self.obstacle_force_values = list()
        
    
    def _add_sample(self, t, current_velocity, panic_level, desired_velocity, desired_force, interaction_force, obstacle_force):          
        self.t_values.append(t)
        
        self.velocities.append(current_velocity)
        self.panic_levels.append(panic_level)     
        self.desired_velocities.append(desired_velocity)
        self.desired_force_values.append(desired_force)
        
        self.interaction_force_values.append(interaction_force)
        
        self.obstacle_force_values.append(obstacle_force)
         
    def _save(self, prefix,simulation_id):
        
        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex=True, figsize=(18,20)) 
    
        fig.suptitle(r"$Force\,components\,of\,pedestrian\,Id=%s,\,initial\,desired\, velocity=%.3f,\,max\,velocity=%.3f,\,acceleration\,time=%.3f$" % (str(int(self.pedestrian_id)),self.initial_desired_velocity,self.max_velocity,self.relax_time), fontsize=18)
       
        ax1.set_title(r"$Velocity=|\vec{v_{p}}(t)|$",fontsize=18)
        ax2.set_title(r"$Panic\,Level=1-\frac{\bar{v_{p}(t)}}{V{p}^{Id}} $",fontsize=18)
        ax3.set_title(r"$Desired\,Velocity\,on\,Desired\,Direction = v_{p}^{d}(t)\vec{e_{p}^{d}}(t)$",fontsize=18)
        ax4.set_title(r"$Desired\,Acceleration\,on\,Desired\,Direction=\frac{1}{\tau_{p}}\left(v_{p}^{d}(t)\vec{e_{p}^{d}}(t)-\vec{v_{p}}(t)\right)$",fontsize=18)

        ax5.set_title(r"$Interaction\,Force=\sum_{q(\neq p)}\vec{f_{pq}}(t)$",fontsize=18)
        
        ax6.set_title(r"$Obstacle\,Force=\sum_{\gamma}\vec{f_{p\gamma}}(t)$",fontsize=18)
                   
        ax1.plot(self.t_values,self.velocities,'k.-')
        ax2.plot(self.t_values,self.panic_levels,'k.-')
        ax3.plot(self.t_values,self.desired_velocities,'k.-')
        ax4.plot(self.t_values,self.desired_force_values,'k.-') 
    
        ax5.plot(self.t_values,self.interaction_force_values,'k.-') 

        ax6.plot(self.t_values,self.obstacle_force_values,'k.-') 


        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        #plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
     
        #plt.xticks([x*10 for x in range(0,int((constants.total_monitoring_duration_uni_direction/10)+1))])
    
        ax1.set_ylabel(r'magnitude')
        ax2.set_ylabel('')
        ax3.set_ylabel(r'm/s')
        ax4.set_ylabel(r'magnitude')
        ax5.set_ylabel(r'magnitude')
        ax6.set_ylabel(r'magnitude')
        
        ax6.set_xlabel('time (second)')
            
        #fig.savefig("%s-%s-%s.pdf" % (prefix, simulation_id,str(self.pedestrian_id)),bbox_inches='tight')  
        fig.savefig("%s-%s-%s.pdf" % (prefix, simulation_id,str(self.pedestrian_id)))  
        plt.clf()
        plt.close('all')
        