'''
Created on 8 Jan 2016

@author: quangv
'''
import matplotlib.pyplot as plt


class   PedTrack:

    def __init__(self):         
        self.t_values = list()
        
        self.velocities = list() 
     
        self.distances = list()

        self.previous_velocity = list()
        self.velocity_rk1 = list()
        self.velocity_rk2 = list()
        self.velocity_rk3 = list()
        self.velocity_rk4 = list()
        
        self.previous_position = list()
        self.position_rk1 = list()
        self.position_rk2 = list()
        self.position_rk3 = list()
        self.position_rk4 = list()
           
    def _reset(self):
        self.t_values.clear()
        
        self.velocities.clear()
        
        self.distances.clear()
        
        self.previous_velocity.clear()
        self.velocity_rk1.clear()
        self.velocity_rk2.clear()
        self.velocity_rk3.clear()
        self.velocity_rk4.clear()
        
        self.previous_position.clear()
        self.position_rk1.clear()
        self.position_rk2.clear()
        self.position_rk3.clear()
        self.position_rk4.clear()
            
    def _add_sample(self,  t, velocity, distance,
                    v0,v_rk1,v_rk2,v_rk3,v_rk4,
                    x0,x_rk1,x_rk2,x_rk3,x_rk4 ): 
      
        self.t_values.append(t)
        self.velocities.append(velocity) 
        self.distances.append(distance)
        
        self.previous_velocity.append(v0)
        self.velocity_rk1.append(v_rk1)
        self.velocity_rk2.append(v_rk2)
        self.velocity_rk3.append(v_rk3)
        self.velocity_rk4.append(v_rk4)
        
        self.previous_position.append(x0)
        self.position_rk1.append(x_rk1)
        self.position_rk2.append(x_rk2)
        self.position_rk3.append(x_rk3)
        self.position_rk4.append(x_rk4)       
        
    def _track_plot(self,prefix, simulation_id):

        fig, (ax1,ax2, ax3,ax4,ax5,ax6,ax7) = plt.subplots(7, sharex=True,figsize=(20,30)) #
        #fig, (ax1,ax2) = plt.subplots(2, sharex=True) 
        fig.suptitle(r"Simulation Id:=%s" % simulation_id, fontsize=18)
        
        ax1.set_title("$Velocity\/time$",fontsize=20)
        ax1.set_xlabel('$time\/(second)$', fontsize=20)
        ax1.set_ylabel(r"$\vec{v}$", fontsize=20)


        ax1.plot(self.t_values, self.velocities,'k.-')
        ax1.grid(True)
        
        ax2.plot(self.t_values, self.distances,'b.-')
        ax2.grid(True)
        ax2.set_title("$Distance\/time$",fontsize=20)
        ax2.set_xlabel('$time\/(second)$', fontsize=20)
        ax2.set_ylabel("$distance$",fontsize=20)
        
        ax3.plot(self.t_values, self.previous_velocity,'b.-')
        ax3.grid(True)
        ax3.set_title("$v_{t-1}\/time$",fontsize=20)
        ax3.set_xlabel('$time\/(second)$', fontsize=20)
        ax3.set_ylabel("$v_{t-1}$",fontsize=20)
        
        ax4.plot(self.t_values, self.velocity_rk1,'b.-')
        ax4.grid(True)
        ax4.set_title("$v_{rk1}\/time$",fontsize=20)
        ax4.set_xlabel('$time\/(second)$', fontsize=20)
        ax4.set_ylabel("$v_{rk1}$",fontsize=20)
        
        ax5.plot(self.t_values, self.velocity_rk2,'b.-')
        ax5.grid(True)
        ax5.set_title("$v_{rk2}\/time$",fontsize=20)
        ax5.set_xlabel('$time\/(second)$', fontsize=20)
        ax5.set_ylabel("$v_{rk2}$",fontsize=20)
        
        ax6.plot(self.t_values, self.velocity_rk3,'b.-')
        ax6.grid(True)
        ax6.set_title("$v_{rk3}\/time$",fontsize=20)
        ax6.set_xlabel('$time\/(second)$', fontsize=20)
        ax6.set_ylabel("$v_{rk3}$",fontsize=20)
        
        ax7.plot(self.t_values, self.velocity_rk4,'b.-')
        ax7.grid(True)
        ax7.set_title("$v_{rk4}\/time$",fontsize=20)
        ax7.set_xlabel('$time\/(second)$', fontsize=20)
        ax7.set_ylabel("$v_{rk4}$",fontsize=20)
        
        ax2.axhline(y=0.6, linewidth=4, color='r') #draw the line where distance = sum of two radii

        #find the closet points between two particles
        indexes = [i for i,x in enumerate(self.distances) if abs(x - 0.6) <= 0.0001]

        for i in range(0,len(indexes)):
            # draw vline
            ax1.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax2.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax3.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax4.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax5.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax6.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax7.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            
            
        ax1.set_xticks([x for x in range(0,20)])
       
        
        fig.savefig("%s-%s.pdf" % (prefix, simulation_id+"1"), dpi=900)  
        plt.clf()
        plt.close('all')
        
        #######################################################################################################
        fig, (ax1,ax2, ax3,ax4,ax5,ax6,ax7) = plt.subplots(7, sharex=True,figsize=(20,30)) #
        #fig, (ax1,ax2) = plt.subplots(2, sharex=True) 
        fig.suptitle(r"Simulation Id:=%s" % simulation_id, fontsize=18)
        
        ax1.set_title("$Velocity\/time$",fontsize=20)
        ax1.set_xlabel('$time\/(second)$', fontsize=20)
        ax1.set_ylabel(r"$\vec{v}$", fontsize=20)


        ax1.plot(self.t_values, self.velocities,'k.-')
        ax1.grid(True)
        
        ax2.plot(self.t_values, self.distances,'b.-')
        ax2.grid(True)
        ax2.set_title("$Distance\/time$",fontsize=20)
        ax2.set_xlabel('$time\/(second)$', fontsize=20)
        ax2.set_ylabel("$distance$",fontsize=20)
        
        ax3.plot(self.t_values, self.previous_position,'b.-')
        ax3.grid(True)
        ax3.set_title("$x_{t-1}\/time$",fontsize=20)
        ax3.set_xlabel('$time\/(second)$', fontsize=20)
        ax3.set_ylabel("$x_{t-1}$",fontsize=20)
        
        ax4.plot(self.t_values, self.position_rk1,'b.-')
        ax4.grid(True)
        ax4.set_title("$x_{rk1}\/time$",fontsize=20)
        ax4.set_xlabel('$time\/(second)$', fontsize=20)
        ax4.set_ylabel("$x_{rk1}$",fontsize=20)
        
        ax5.plot(self.t_values, self.position_rk2,'b.-')
        ax5.grid(True)
        ax5.set_title("$x_{rk2}\/time$",fontsize=20)
        ax5.set_xlabel('$time\/(second)$', fontsize=20)
        ax5.set_ylabel("$x_{rk2}$",fontsize=20)
        
        ax6.plot(self.t_values, self.position_rk3,'b.-')
        ax6.grid(True)
        ax6.set_title("$x_{rk3}\/time$",fontsize=20)
        ax6.set_xlabel('$time\/(second)$', fontsize=20)
        ax6.set_ylabel("$x_{rk3}$",fontsize=20)
        
        ax7.plot(self.t_values, self.position_rk4,'b.-')
        ax7.grid(True)
        ax7.set_title("$x_{rk4}\/time$",fontsize=20)
        ax7.set_xlabel('$time\/(second)$', fontsize=20)
        ax7.set_ylabel("$x_{rk4}$",fontsize=20)
        
        ax2.axhline(y=0.6, linewidth=4, color='r') #draw the line where distance = sum of two radii

        #find the closet points between two particles
        indexes = [i for i,x in enumerate(self.distances) if abs(x - 0.6) <= 0.0001]

        for i in range(0,len(indexes)):
            # draw vline
            ax1.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax2.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax3.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax4.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax5.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax6.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            ax7.axvline(x=self.t_values[indexes[i]], linewidth=1, color='m')
            
            
        ax1.set_xticks([x for x in range(0,20)])
        fig.savefig("%s-%s.pdf" % (prefix, simulation_id+"2"), dpi=900)
        plt.clf()
        plt.close('all')        
      
    def _save(self, prefix, simulation_id):
         
        self._track_plot(prefix, simulation_id)
        self._reset()