import numpy as np
import random as rd

B_rep = 0.35

def call(lower,upper):
	N = 1000	
	ratio = np.random.exponential(scale=0.1, size=N )
	ratio= sorted(ratio,reverse = False)   
	B_att = [B_rep/i for i in ratio]
	i=0
	while i  < len(B_att):
		if B_att[i] > upper or B_att[i] < lower:
			del B_att[i]
		else:
			i+=1   
	B_att= sorted(B_att) 	
	return B_att


B_att = list()
while len(B_att) <10:
	B_att = call(0.6,0.8)
B_att= B_att[0:10]
print(B_att)