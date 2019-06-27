import chaospy as cp
import numpy as np
from pylab import *

# modele : u represente l'ecart de temperature T-Ti
def u(t, a, I) :
	return I*np. exp(-a*t)

# Definition des distributions statistiques
dist_a = cp.Uniform(0., 0.001)
dist_I = cp.Uniform(10, 16)
dist = cp.J(dist_a, dist_I)
N=1000

#integration Monte Carlo avec plan de tirages Latin Hypercube 
samples = dist.sample(N, rule="L")
t = np.linspace(0, 1200, 10)
sample_u = [u(t, *s) for s in samples.T]

E = np.mean(sample_u,0)
Var = np.var(sample_u,0)
deviation = np.std(sample_u, 0)
print('MC avec plan de tirages Latin Hypercube :')
print('E : ',E)
print('Var : ',Var)
print('deviation : ',deviation)

# prepare confidence level curves
nstd = 1. # to draw nstd-sigma intervals
u_up = E + nstd * deviation
u_dw = E - nstd * deviation

#plot
fig, ax = plt.subplots(1)
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
rcParams['font.size']= 14
xlabel('t (s)', fontsize=14)
ylabel('u', fontsize=14)
#title('Equation de la chaleur : MC Latin Hypercube', fontsize=14)
plot(t, E, 'k', lw=2, label='E')
ax.fill_between(t, u_up, u_dw, color="k", alpha=.25, label='interval 1-sigma')
legend(loc='upper right',fontsize=14)
show()
