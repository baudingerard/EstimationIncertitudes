import chaospy as cp
import numpy as np

# modele : u represente l'ecart de temperature T-Ti
def u(t, a, I) :
	return I*np. exp(-a*t)

# Definition des distributions statistiques
dist_a = cp.Uniform(0., 0.001)
dist_I = cp.Uniform(10, 16)
dist = cp.J(dist_a, dist_I)

#integration Monte Carlo avec plan de tirages Latin Hypercube 
samples = dist.sample(1000, rule="L")
t = np.linspace(0, 1200, 10)
sample_u = [u(t, *s) for s in samples.T]

E = np.mean(sample_u,0)
Var = np.var(sample_u,0)
print('MC avec plan de tirages Latin Hypercube :')
print('E : ',E)
print('Var : ',Var)
