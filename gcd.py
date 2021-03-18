import numpy as np

def get_gcd(vec):
	vec = np.sort(vec)
	maxi = np.max(vec)
	while len(vec) > 1 and vec[-1]>0:
		maxi = vec[-1]
		vec = vec - vec[0] 
		vec = vec[1:]
	return maxi
ex = np.array([0.46093127, 0.34767182, 0.46093127, 0.46093127, 0.34767182, 0.34767182])


