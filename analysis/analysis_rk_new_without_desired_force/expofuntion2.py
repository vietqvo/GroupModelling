import numpy as np
import matplotlib.pyplot as plt

#this func compute the attractive force affect on pedestrian ped1
def _attractive_force(ped1, ped2,distance): 
	rep = ped1.get("A_att")*(np.exp((ped1.get("radius")+ped2.get("radius")-distance)/ped1.get("B_att"))) 
	return rep
	

#this func compute the repulsive force affect on pedestrian ped1
def _repulsive_force(ped1, ped2,distance): 
	rep = ped1.get("A_rep")*(np.exp((ped1.get("radius")+ped2.get("radius")-distance)/ped1.get("B_rep"))) 
	return rep
		
ped_p = dict(radius = 0.3, A_rep = 3.0, B_rep = 0.2, A_att = 3.0, B_att = 1.0) 
ped_q = dict(radius = 0.3, A_rep = 3.0, B_rep = 0.2, A_att = 3.0, B_att = 1.0) 
ped_k = dict(radius = 0.3, A_rep = 3.0, B_rep = 0.2, A_att = 3.0, B_att = 1.0) 

d = np.arange(0.00,3,0.05) 
total_rep =[]
total_att = []

for distance in d:
	force = _repulsive_force(ped_p,ped_q,distance) + _repulsive_force(ped_p,ped_k,distance + 1.2)
	total_rep.append(force)
	force = _attractive_force(ped_p,ped_q,distance) + _attractive_force(ped_p,ped_k,distance + 1.2)
	total_att.append(force) 

plt.title('$Repulsive\/and\/Attractive\/forces\/of\/pedestrian\/p$')
plt.plot(d,total_rep,'r',label='$Repulsive\/force$')
plt.plot(d,total_att,'b',label='$Attractive\/force$')

plt.ylabel(r'$Force\/magnitude$', fontsize = 15)
plt.xlabel(r'$Distance\/ d$', fontsize = 15)

ax1 = plt.gca()
ax1.set_xlim([0, 3])
ax1.set_autoscale_on(False)


plt.axvline(x=(0.6), ymin=0.0, ymax = 2, linewidth=2, color='k')
plt.annotate(r'$r_{1}+r_{2}=d$', xy=(0.61,15), verticalalignment='top')
legend = ax1.legend(loc='upper right', shadow=True)

				
plt.grid()
plt.show()