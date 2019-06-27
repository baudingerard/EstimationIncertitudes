import matplotlib.mlab as mlab
import numpy as np
import pylab

# fonction surface avec pour donnees la longueur et la largeur
def surface(L,l):
   return L * l

# longueur et largeur
L = 100
l = 50
# leurs deviations standards
stvL=stvl = 2
 
# nombre iterations : 1 million, preconisation LNE
N = 1000000

longueur = np.random.normal(L, stvL, N)
largeur = np.random.normal(l, stvl, N)
 
# calcul des surfaces 
surfaces = surface(longueur, largeur)
mu = pylab.mean(surfaces)
sigma = pylab.std(surfaces)

# resultats des simulations
print (mu, sigma)
'''
5000.084989964445 223.6842714131764
'''
# resultats en tenant compte de la regle des chiffres significatifs
print ("Resultats :")
print( "Moyenne = ","%.f" % mu)
print ("deviation standard  = ", "%.f" % sigma)
''' 
Resultats :
Moyenne =  5000
deviation standard  =  224
'''
# trace de l'histogramme
n, bins, patches = pylab.hist(surfaces, 60, normed=1, facecolor='gray', alpha=0.75)
y = mlab.normpdf( bins, mu, sigma)
l = pylab.plot(bins, y, 'k-', linewidth=2)
#plt.xlabel('Smarts')
pylab.xlabel('surface')
pylab.ylabel(u'probabilite')
pylab.title('$\mathrm{histogramme\ de\ la\ surface:}\ \mu=%.f,\ \sigma=%.f$' %(mu, sigma))
pylab.grid(True)
pylab.show()

