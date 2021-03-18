import sys
import os
import pandas as pd
import re
import numpy as np



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




args = sys.argv[1:]
left = args 
"""
Plan:
1. Get all element symbols
2. Get mols of each element on left and right
3. Figure out system to get equal number of each (maybe just least common multiple??
4. Reduce by common factor afterwards
"""
# remove + signs
left = [s for s in left if s!='+']
ldicts= [ tokenToDict(s) for s in left ] 


ldf= pd.DataFrame(ldicts).fillna(0.).T 


elements = pd.read_csv("elements.csv")
elements = elements.set_index("Symbol")

l = ldf.values
r = elements[elements.index.isin(ldf.index.tolist())].loc[ldf.index.tolist(),["AtomicMass"]]
print(np.dot(l.T, r.values))


