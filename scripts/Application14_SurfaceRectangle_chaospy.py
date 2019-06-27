"""
Surface du rectangle pour 1 et 2 x largeur
Analyse faite avec deux differentes approche:
    1. Monte Carlo 
    2. Monte Carlo avec Plan de Tirage Latin Hypercube 
"""
import chaospy as cp
import numpy as np

# The model solver
def s(x, param):
    return param[0] *param[1] *x

x=np.linspace(1, 2, 2)
# Defining the random distributions:
dist_L = cp.Normal(100, 2)
dist_l = cp.Normal(50, 2)
dist = cp.J(dist_L,dist_l)


## Monte Carlo integration
samples = dist.sample(size=5000)
evals = [s(x, sample) for sample in samples.T]

E = np.mean(evals, 0)
var = np.var(evals, 0)

print('MC classique :')
print('x : ',x)
print('mean : ',E)
print('var : ',var)


samples = dist.sample(size=5000, rule="L")
evals = [s(x, sample) for sample in samples.T]

E = np.mean(evals, 0)
var = np.var(evals, 0)

print('MC  : Plan de Tirage Latin Hypercube ')
print('mean : ',E)
print('var : ',var)