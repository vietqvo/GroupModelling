import numpy as np
import random as rd
N = 100
B_rep = 0.3
ratio = np.random.exponential(scale=.2, size=10)
ratio= sorted(ratio,reverse = False)
i=0
while i  < len(ratio):
    if ratio[i] > 0.9 or ratio[i] < 0.2:
        del ratio[i]
    else:
        i+=1    
    
B_att = [B_rep/i for i in ratio]
print(B_att)

