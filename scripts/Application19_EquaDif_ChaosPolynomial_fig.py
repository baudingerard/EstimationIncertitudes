
import chaospy as cp
import numpy as np
from pylab import *

# modele : u represente l'ecart de temperature T-Ti
def u(t, a, I):
    return I*np.exp(-a*t)

# Definition des distributions statistiques
dist_a = cp.Uniform(0, 0.001)
dist_I = cp.Uniform(10, 16)
dist = cp.J(dist_a, dist_I)

t = np.linspace(0, 1200, 10)

# polynome de chaos
# utilisant la methode Pseudo-Spectrale et une quadrature Gaussienne
ordre = 5
P, norms = cp.orth_ttr(ordre, dist, retall=True)
nodes, weights = cp.generate_quadrature(ordre+1, dist, rule="G")
solves = [u(t, s[0], s[1]) for s in nodes.T]
U_hat = cp.fit_quadrature(P, nodes, weights, solves, norms=norms)

E1 = cp.E(U_hat, dist)
Var1 = cp.Var(U_hat, dist)
print('Polynome de chaos utilisant la methode Pseudo-Spectrale')
print('et une quadrature Gaussienne :')
print('E : ',E1)
print('Var : ',Var1)

u_up1=E1+np.sqrt(Var1)
u_dw1=E1-np.sqrt(Var1)

# polynome de chaos
# utilisant la methode "Point Collocation" et des tirages pseudo aleatoires
ordre = 5
P = cp.orth_ttr(ordre, dist)
nodes = dist.sample(2*len(P), "M")
solves = [u(t, s[0], s[1]) for s in nodes.T]
U_hat = cp.fit_regression(P, nodes, solves, rule="T")

E2= cp.E(U_hat, dist)
Var2 = cp.Var(U_hat, dist)
print(' ')
print('Polynome de chaos utilisant la methode "Point Collocation"')
print('et des tirages pseudo aleatoires :')
print('E : ',E2)
print('Var : ',Var2)

#plot
fig, ax = plt.subplots(1)
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
rcParams['font.size']= 16
xlabel('t (s)', fontsize=14)
ylabel('u', fontsize=14)
#title('Equation de la chaleur : Chaos Polynomial', fontsize=18)
plot(t, E1, 'k', lw=2, label='E pseudo-spectral')
ax.fill_between(t, u_up1, u_dw1, color="k", alpha=.25, label='interval 1-sigma')
plot(t, E2, 'ok', lw=2, label='E Point Collocation')
legend(loc='upper right',fontsize=14)
show()
