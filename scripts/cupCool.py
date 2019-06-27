'''Coffee cup Function (3 parameters)'''
import numpy as np

def evaluate(values):
    Y = np.zeros([values.shape[0]])
    for i, X in enumerate(values):
           Y[i]=X[1]*np. exp(-X[2]*X[0])
    return Y
