import numpy as np
import matplotlib.pyplot as plt

r1= 0.3
r2 = 0.3

A_rep = 2.5
B_rep = 0.2
A_att = 2.5#2.5
B_att = 1.0#1.0

d = np.arange(0.00,5,0.05) 
y1 = A_rep*(np.exp((r1+r2-d)/B_rep))
y2 = A_att*(np.exp((r1+r2-d)/B_att))

plt.plot(d,y1,'r',label='$Repulsive\/force$')
plt.plot(d,y2,'b',label='$Attractive\/force$')

plt.ylabel(r'$Force\/magnitude$', fontsize = 15)
plt.xlabel(r'$Distance\/ d$', fontsize = 15)

ax1 = plt.gca()
ax1.set_xlim([0, 5])
ax1.set_autoscale_on(False)


ax1_param_text = []
ax1_param_text.append("$A_{rep}= 2.5$")
ax1_param_text.append("$B_{rep}= 0.2$")
ax1_param_text.append("$A_{att}= 2.5$")
ax1_param_text.append("$B_{att}= 1.0$")

plt.axvline(x=(r1+r2), ymin=0.0, ymax = 2, linewidth=2, color='k')
plt.annotate(r'$r_{1}+r_{2}=d$', xy=(0.61,15), verticalalignment='top')
legend = ax1.legend(loc='upper right', shadow=True)

ax1.text(0.98, 0.80, "\n".join(ax1_param_text),
                transform=ax1.transAxes,
                verticalalignment='top',
                horizontalalignment='right',
                fontdict={'family': 'serif', 'size'   : 15},
                bbox = {'facecolor': 'w', 'edgecolor': 'w', 'alpha': 0.5},
                )
				
plt.grid()
plt.show()