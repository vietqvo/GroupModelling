'''
Created on 26 Mar 2015

@author: quangv
'''
import matplotlib.pyplot as plt
import numpy as np
import datetime


now = datetime.datetime.now()
figure_index= now.hour + now.minute + now.second
fig = plt.figure(figure_index)
run_trials = [time for time in range(1,31)]

""" in unique directional flow """
""" average escape rate of different-distribution prototype"""
escape_rates_different_distribution_protype_uni = [1, 0.986, 0.933, 1.014, 0.986, 0.986, 1.061, 1.045, 0.897, 0.886, 
                                               1.014, 1.014, 0.946, 0.972, 0.673, 0.673, 0.986, 0.986, 0.921, 0.909, 
                                               0.886, 0.921, 1, 0.946, 1.045, 0.972, 0.972, 0.673, 1.045, 1.029]


escape_rates_average_distribution_protype_uni = [0.833, 0.564, 0.624, 0.769, 0.554, 0.795, 0.663, 0.683, 0.854, 0.604,
                                             0.673, 0.663, 0.475, 0.843, 0.673, 0.683, 0.574, 0.644, 0.653, 1.029,
                                             0.614, 0.554, 0.663, 0.634, 0.663, 0.683, 0.663, 0.653, 0.673, 0.673]

fig = plt.figure(1)
fig.set_size_inches(12,6)
plt.title("Escape rate over trails in uni-direction scenario")
plt.xlabel("Trial")
plt.xlim([0,31])
plt.ylim([0,1.5])
plt.ylabel("Ped/s")

plt.plot(run_trials, escape_rates_different_distribution_protype_uni,'r^',  label="P$_{different}$ = %.3f" % np.average(escape_rates_different_distribution_protype_uni))
plt.plot(run_trials, escape_rates_average_distribution_protype_uni,'bs', label="P$_{average}$ = %.3f" % np.average(escape_rates_average_distribution_protype_uni))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=2, fancybox=True, shadow=True, prop={'size':10})
plt.grid(True)
 
fig.savefig("%s.pdf" % ("uni-direction"))        
plt.clf()
plt.close('all')

###########################################################################################################################
""" in bio directional flow """

escape_rates_different_distribution_protype_bio = [0.741, 0.706, 0.741, 0.75, 0.759, 0.75, 0.759, 0.779, 0.845, 0.723, 
                                               0.706, 0.8, 0.619, 0.723, 0.769, 0.732, 0.8, 0.779, 0.779, 0.759,
                                               0.714, 0.822, 0.822, 0.833, 0.811, 0.811, 0.779, 0.833, 0.833, 0.741]


escape_rates_average_distribution_protype_bio = [0.594, 0.333, 0.292, 0.292, 0.287, 0.48, 0.441, 0.403, 0.292, 0.292,
                                             0.292, 0.612, 0.326, 0.292, 0.292, 0.287, 0.292, 0.292, 0.625, 0.287,
                                             0.387, 0.292, 0.382, 0.292, 0.292, 0.292, 0.292, 0.292,0.504,0.368]

fig = plt.figure(2)
fig.set_size_inches(12,6)
plt.title("Escape rate over trails in bi-direction scenario")
plt.xlabel("Trial")
plt.xlim([0,31])
plt.ylim([0,1.5])
plt.ylabel("Ped/s")

plt.plot(run_trials, escape_rates_different_distribution_protype_bio,'r^',  label="P$_{different}$ = %.3f" % np.average(escape_rates_different_distribution_protype_bio))
plt.plot(run_trials, escape_rates_average_distribution_protype_bio,'bs', label="P$_{average}$ = %.3f" % np.average(escape_rates_average_distribution_protype_bio))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), ncol=2, fancybox=True, shadow=True, prop={'size':10})
plt.grid(True)
 
fig.savefig("%s.pdf" % ("bi-direction"))        
plt.clf()
plt.close('all')
        