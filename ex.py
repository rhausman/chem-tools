import torch
import numpy as np

# reaction: CO2 + H20 => C6H12O6 + O2
ML = np.array([[1,0, 2], [0,2,1]], dtype = np.float).T # this will have one row for C, one row for H, one row for O. Each col is compound
ML = torch.tensor(ML, requires_grad=False)
# nL => coefficiencts, to be found
nL = torch.tensor(np.array([[2,2]], dtype=np.float).T, requires_grad=True)
# now, right side
MR = np.array([[6, 12, 6],[0, 0 , 2]], dtype=np.float).T
MR = torch.tensor(MR, requires_grad=False)
# nR => to be calculated
nR = torch.tensor(np.array([[1,1]], dtype=np.float).T, requires_grad=True)
