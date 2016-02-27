import numpy as np
import matplotlib.pyplot as plt
import math as m

r1 = 0.3
r2 = 0.3

R = 2.0
r = 0.3
A = 1.5
a = 0.5

repulsion = list()
attraction = list()

d = np.arange(0.6,3,0.05) 
for i in range(len(d)):
	rep = R*(np.exp(- m.fabs(d[i]-0.6)/r))
	att = A*(np.exp(- m.fabs(d[i]-0.6)/a))
	repulsion.append(rep)
	attraction.append(att)
	

plt.plot(d,repulsion,'r',label='$Repulsive\/force$', linestyle = '-')
plt.plot(d,attraction,'b',label='$Attractive\/force$')

plt.ylabel(r'$Force$', fontsize = 15)
plt.xlabel(r'$Distance\/ x$', fontsize = 15)

ax1 = plt.gca()
ax1.set_xlim([0.6, 3])
ax1.set_autoscale_on(False)

plt.grid()
plt.show()