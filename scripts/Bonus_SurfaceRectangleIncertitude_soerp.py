from soerp import *   # uv, N, U, Exp, etc.
from soerp.umath import * 

# fonction surface avec pour donnees la longueur et la largeur
def surface(x,y):
   return x * y

stv = 2 # deviation standard pour le rayon
# une deviation standard stv en rayon sur chaque coin correspond
# a une deviation standard en x ou y de stv/sqrt(2)
stv = stv/umath.sqrt(2)
longueur = N(100,stv)
largeur  = N(100,stv)

surf=surface(longueur,largeur)
surf.describe()

# resultats en tenant compte de la regle des chiffres significatifs
print ('avec la regle des chiffres significatifs : ')
print ('surface = ',"%.f" % surf.mean,"+/-","%.f" % umath.sqrt(surf.var))
#10000+/-200

def surface2(x1,y1,x2,y2,x3,y3,x4,y4):
	return  umath.sqrt((x2-x1)**2+(y2-y1)**2)*umath.sqrt((x3-x1)**2+(y3-y1)**2)/2+umath.sqrt((x4-x2)**2+(y4-y2)**2)*umath.sqrt((x4-x3)**2+(y4-y3)**2)/2

x1 = N(0, stv)
y1 = N(0, stv)
x2 = N(100,stv)
y2 = N(0, stv)
x3 = N(0, stv)
y3 = N(100, stv)
x4 = N(100, stv)
y4 = N(100, stv)

surf2=surface2(x1,y1,x2,y2,x3,y3,x4,y4)
print(' ')
print ('formule exacte : ')
surf2.describe()

# resultats en tenant compte de la regle des chiffres significatifs
print ('formule exacte : ')
print ('avec la regle des chiffres significatifs : ')
print ('surface = ',"%.f" % surf2.mean,"+/-","%.f" % umath.sqrt(surf2.var))