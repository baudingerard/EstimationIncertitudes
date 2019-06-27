# import de librairies
import numpy as np
import matplotlib.pyplot as plt
import pup

'''
-------------------------
-------------------------
- Test des fonctions  -
------------------------
------------------------
'''
#test mean et sigma
psup=np.array([17.04,16.46,16.10,16.46,17.50])
pmsup=pup.mean(psup)
spsup=pup.sigma(psup)
dpsup=pup.u95(spsup,np.size(psup)-1)
print('N =',np.size(psup))
print ('t(N-1) =',pup.t95[np.size(psup)-2])
print ("pression sup = ","%4.2f" %pmsup," +/- ","%4.2f" %dpsup,' , 95 %')
print(' ')

pinf=np.array([7.335,7.762,7.760])
pminf=pup.mean(pinf)
spinf=pup.sigma(pinf)
dpinf=pup.u95(spinf,np.size(pinf)-1)
print('N =',np.size(pinf))
print ('t(N-1) =',pup.t95[np.size(pinf)-2])
print ("pression inf = ","%4.2f" %pminf," +/- ","%4.2f" %dpinf,' , 95 %')
print(' ')

# test x - y
taille=np.array([160,170,180,190])
poids=np.array([64,66,84,86])
a,b,sr,sa,sb,r=pup.ls(taille,poids)
da,db=pup.u95ab(sa,sb,np.size(taille)-1)

print ("pente = ","%3.2f" %a," +/- ","%3.2f" %da,' , 95 %')
print ("y0 = ","%.f" %b," +/- ","%.f" %db,' , 95 %')
	