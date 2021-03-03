import os
import sys
import re
import numpy as np
import pandas as pd
from scipy.linalg import null_space
# take in chem eqn, solve

print("DO NOT ACCIDENTALLY TYPE '0' (zero) FOR OXYGEN INSTEAD OF 'O' (oh), which should be used! Also note that a current limitation is that polyatomic 'sub-compounds' such as 'Ca3(PO4)2' will not be properly parsed, so you should instead write it as 'Ca3P2O8'\n")


def tokenToDict(s, start = {}):
	a =  re.compile('[A-Z][a-z]?(\d|)*') # match a single element-number pair
	pairs = []
	while s != '':
		match = a.match(s)
		start, end = match.start(), match.end()
		pairs.append(s[start:end])
		s = s[end:]
	el_quant = {} # pairs of elements and quantities
	a2 = re.compile('[A-Z][a-z]?') # match just the element name
	for pair in pairs:
		match = a2.match(pair)
		start, end= match.start() , match.end()
		el = pair[:end]
		quant = pair[end:]
		# if no subscript present, assume 1
		if quant == '':
			quant = 1
		else:
			# else, convert it to numerical form
			quant = int(quant)
		# register the new element
		if el not in el_quant:
			el_quant[el] = 0
		el_quant[el] += quant
	return el_quant
			
		


try:
	args = sys.argv[1:]

	left = args[:args.index('=')] # separate inputs and outputs
	right = args[args.index('=')+1 :]
	"""
	Plan:
	1. Get all element symbols
	2. Get mols of each element on left and right
	3. Figure out system to get equal number of each (maybe just least common multiple??
	4. Reduce by common factor afterwards
	"""
	# remove + signs
	left = [s for s in left if s!='+']
	right = [s for s in right if s!='+']
	#isCapitalAlpha = lambda x: ord(x) >= 65 and ord(x) <= 90 # is this a capital letter?
	ldicts, rdicts = [ tokenToDict(s) for s in left ] , [tokenToDict(s) for s in right]
	ldf, rdf = pd.DataFrame(ldicts).fillna(0.).T , pd.DataFrame(rdicts).fillna(0.).T
	rdf = rdf.loc[ldf.index.tolist(),:]
	# transpose so that each row corresponds to 1 element, convert to numpy
	ML , MR = ldf.values.astype(float) , rdf.values.astype(float)

	#elements = [c for c in "".join(left) if isCapitalAlpha(c) ]
	#elements = set(elements)
	
except:
	print(sys.argv)

# matrix: nelements x n_reactants
# examples for testing:
# C02 + H2O => C6 H12 O6 + O2
# rows: C, H, O
# cols: C02, h20 
#ML = np.array([[1,0],[0,2],[2,1]], dtype=np.float)
#MR = np.array([[6, 12, 6],[0, 0 , 2]], dtype=np.float).T
# put ML and -MR together, to symbolize [ML . -MR] * [n1 . n2] = 0
# This is the real linear system that we need to solve. We can use scipy nullspace solution for this

M = np.concatenate([ML, -MR], axis = 1)

ns = null_space(M)
ns = ns/np.min(ns)
coeficients = np.rint(ns).astype(int) # round to nearest int # this was causing rounding errors: .astype(int) # make sure they're the same

#print("Raw null space solution (make sure it matches stoichiometric coeficients for a suitable solution): ", ns)
print("Stoichiometric coeficients: ", list(zip( [el[0] for el in coeficients] , left+right) ) )


