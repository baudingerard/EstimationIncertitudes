from mcerp import * # N, U, Gamma, Beta, correlate, etc.
import mcerp.umath as umath
import numpy as np

# fonction surface avec pour donnees la longueur et la largeur
def surface(L,l):
   return L * l

# longueur et largeur
L = 100.
l = 50.
# leurs deviations standards
stvL=stvl = 2.

longueur = N(L, stvL)
largeur = N(l, stvl)
  
# calcul des surfaces 
surfaces = surface(longueur, largeur)
surfaces.describe()
print('surface.mean : ',surfaces.mean,'  stv : ',np.sqrt(surfaces.var))

'''
9999.1573234 199.631782423
'''
surfaces.plot(color="k")
surfaces.plot(hist=True,color="k",alpha=0.25)
surfaces.show()

