
import chaospy as cp
import numpy as np

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

E = cp.E(U_hat, dist)
Var = cp.Var(U_hat, dist)
print('Polynome de chaos utilisant la methode Pseudo-Spectrale')
print('et une quadrature Gaussienne :')
print('E : ',E)
print('Var : ',Var)


# polynome de chaos
# utilisant la methode "Point Collocation" et des tirages pseudo aleatoires
ordre = 5
P = cp.orth_ttr(ordre, dist)
nodes = dist.sample(2*len(P), "M")
solves = [u(t, s[0], s[1]) for s in nodes.T]
U_hat = cp.fit_regression(P, nodes, solves, rule="T")

E= cp.E(U_hat, dist)
Var = cp.Var(U_hat, dist)
print(' ')
print('Polynome de chaos utilisant la methode "Point Collocation"')
print('et des tirages pseudo aleatoires :')
print('E : ',E)
print('Var : ',Var)
