from uncertainties import ufloat
from uncertainties.umath import *  
# ce sous-module permet de capturer les fonctions du module math, 
# ce qui permet d'utiliser les fonctions cos(), sin(),etc. avec des incertitudes.

# fonction surface avec pour donnees la longueur et la largeur
def surface(L,l):
   return L * l

uL=ul = 2 # incertitudes types sur la longueur et la largeur

longueur = ufloat(100,uL)
largeur  = ufloat(50,ul)

# resultats en tenant compte de la regle des chiffres significatifs
resultat = surface(longueur,largeur)
print ('avec la regle des chiffres significatifs : ')
print ('surface : ',"%.f" % resultat.n,"+/-","%.f" % resultat.s)
#on doit trouver 5000 +/- 224

