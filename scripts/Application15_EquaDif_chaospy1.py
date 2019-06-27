import chaospy as cp
import numpy as np

# modele - u represente la temperature adimensionnelle
def u(t, a,) :
	return np. exp(-a*t)

# definition des distributions statistiques:
dist_a = cp.Uniform(0., 0.001)

#integration Monte Carlo avec plan de tirages Latin Hypercube 
sample_a = dist_a.sample(size=1000, rule="L")
t= np.linspace(0, 1200, 10)  # 1200 s = 20 mn
sample_u= [u(t, a) for a in sample_a]

E = np.mean(sample_u,0)
Var = np.var(sample_u,0)
print('MC tirages Latin Hypercube :')
print('E : ',E)
print('Var : ',Var)