import numpy as np
import matplotlib.pyplot as plt

r1= 0.3
r2 = 0.3

A_rep = 1.0
B_rep = 1.5
A_att = 2.0
B_att = 2.0

d = np.arange(0.00,5,0.05) 
y1 = np.exp((r1+r2-d)/B_rep)
y2 = np.exp((r1+r2-d)/B_att)

plt.plot(d,y1,'r',d,y2,'b')
plt.suptitle(r'Force magnitude', fontsize = 25)
#plt.axis([0,5,0,0.4])
plt.ylabel(r'$Force\/magnitude$', fontsize = 15)
plt.xlabel(r'Distance', fontsize = 15)
ax1 = plt.gca()
ax1.set_xlim([0, 5])
ax1.set_autoscale_on(False)
plt.axvline(x=(r1+r2), ymin=0.0, ymax = 2, linewidth=2, color='k')

#plt.annotate('Repulsive force', xy=(1, 0.35), xytext=(1.6, 0.35),arrowprops = dict(facecolor = 'red', shrink=0.1))
#plt.annotate('Attraction force', xy=(2, 0.15), xytext=(2.4, 0.25),arrowprops = dict(facecolor = 'blue', shrink=0.1))
plt.grid()
plt.show()