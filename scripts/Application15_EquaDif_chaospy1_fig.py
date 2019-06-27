import chaospy as cp
import numpy as np
from pylab import *

# modele - u represente la temperature adimensionnelle
def u(t, a,) :
	return np. exp(-a*t)

# definition des distributions statistiques:
dist_a = cp.Uniform(0., 0.001)

N=1000

#integration Monte Carlo avec plan de tirages Latin Hypercube 
sample_a = dist_a.sample(size=N, rule="L")
t= np.linspace(0, 1200, 10)  # 1200 s = 20 mn
sample_u= [u(t, a) for a in sample_a]

E = np.mean(sample_u,0)
Var = np.var(sample_u,0)
deviation = np.std(sample_u, 0)
print('MC tirages Latin Hypercube :')
print('E : ',E)
print('Var : ',Var)
print('deviation : ',deviation)

# prepare confidence level curves
nstd = 1. # to draw nstd-sigma intervals
u_up = E + nstd * deviation
u_dw = E - nstd * deviation

#plot
fig, ax = plt.subplots(1)
rcParams['xtick.labelsize'] = 18
rcParams['ytick.labelsize'] = 18
rcParams['font.size']= 20
xlabel('t (s)', fontsize=18)
ylabel('u', fontsize=18)
title('Equation de la chaleur : MC Latin Hypercube', fontsize=18)
plot(t, E, 'r', lw=2, label='E')
ax.fill_between(t, u_up, u_dw, alpha=.25, label='interval 1-sigma')
#ylim(290, 320)
#xlim(0,1300)
legend(loc='upper right',fontsize=18)
show()