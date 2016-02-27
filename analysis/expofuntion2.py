import numpy as np
import matplotlib.pyplot as plt
import math as m

#this func compute the attractive force affect on pedestrian ped1
def _attractive_force(ped1, ped2,distance): 
	att = ped1.get("A_att")*(np.exp(- m.fabs(distance - 0.6)/ped1.get("B_att"))) 
	return att
	

#this func compute the repulsive force affect on pedestrian ped1
def _repulsive_force(ped1, ped2,distance): 
	rep = ped1.get("A_rep")*(np.exp(- m.fabs(distance - 0.6)/ped1.get("B_rep"))) 
	return rep
		
ped_p = dict(radius = 0.3, A_rep = 2.0, B_rep = 0.3, A_att = 1.8, B_att = 0.5) 
ped_q = dict(radius = 0.3, A_rep = 2.0, B_rep = 0.3, A_att = 1.8, B_att = 0.5) 
ped_k = dict(radius = 0.3, A_rep = 2.0, B_rep = 0.3, A_att = 1.8, B_att = 0.5) 
ped_j = dict(radius = 0.3, A_rep = 2.0, B_rep = 0.3, A_att = 1.8, B_att = 0.5) 

d = np.arange(0.00,3,0.05) 
total_rep =[]
total_att = []

for distance in d:
	force = _repulsive_force(ped_p,ped_q,distance) + _repulsive_force(ped_p,ped_k,distance + 0.3+ 0.2 + 0.3) + _repulsive_force(ped_p,ped_j,distance + 1.6)
	total_rep.append(force)
	force = _attractive_force(ped_p,ped_q,distance) + _attractive_force(ped_p,ped_k,distance + 0.3+ 0.2 + 0.3) + _attractive_force(ped_p,ped_j,distance + 1.6)
	total_att.append(force) 

plt.title('$Repulsive\/and\/Attractive\/forces\/of\/pedestrian\/p$')
plt.plot(d,total_rep,'r',label='$Repulsive\/force$')
plt.plot(d,total_att,'b',label='$Attractive\/force$')

plt.ylabel(r'$Force\/magnitude$', fontsize = 15)
plt.xlabel(r'$Distance\/ d$', fontsize = 15)

ax1 = plt.gca()
ax1.set_xlim([0.6, 3])
ax1.set_autoscale_on(False)


plt.axvline(x=(0.6), ymin=0.0, ymax = 2, linewidth=5, color='k')
plt.annotate(r'$r_{1}+r_{2}=d$', xy=(0.61,0.5), verticalalignment='top')
legend = ax1.legend(loc='upper right', shadow=True)

ax1_param_text = []
ax1_param_text.append("$R= 2.0$")
ax1_param_text.append("$r= 0.3$")
ax1_param_text.append("$A= 1.8$")
ax1_param_text.append("$a= 0.5$")

ax1.text(0.98, 0.76, "\n".join(ax1_param_text),
                transform=ax1.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
				
plt.grid()
plt.show()