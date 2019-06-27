# import de librairies
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op

'''
fonctions numpy:
np.array([x1,x3,...]) : creation de tableau numpy des valeurs de x1, x2, ...
np.size(p) : taille du tableau p
np.sum(p) : somme des valeurs du tableau p
a*b : produit terme a terme de deux tableaux numpy a et b
'''

t95=np.array([12.7,4.30,3.18,2.78,2.57,2.45,2.36,2.31,2.26,2.23,
                      2.2,2.18,2.16,2.14,2.13,2.12,2.11,2.10,2.09,2.09])
t95inf=2.

t90=np.array([36.31,2.92,2.35,2.13])
t90inf=1.64

def ls(x,y):
	N=np.size(x)
	xm=np.sum(x)/N
	ym=np.sum(y)/N
	xym=np.sum(x*y)/N
	x2m=np.sum(x*x)/N
	a=(xym-xm*ym)/(x2m-xm*xm)
	b=ym-a*xm
	residus=y-(a*x+b)
	sr=np.sqrt(np.sum(residus*residus)/(N-2))
	sa=sr/np.sqrt(np.sum((x-xm)*(x-xm)))
	sb=sr*np.sqrt(np.sum(x*x)/N/np.sum((x-xm)*(x-xm)))
	r=np.sum((x-xm)*(y-ym))/np.sqrt(np.sum((x-xm)*(x-xm))*np.sum((y-ym)*(y-ym)))
	return a,b,sr,sa,sb,r

def lsUncertainties(x,y,dx,dy):
	ai,bi,sr,sa,sb,r=ls(x,y)
	while True:
		aiest=ai
		w=1/(dy*dy+aiest*dx*dx)
		delta=np.sum(w)*np.sum(w*x*x)-(np.sum(w*x))**2
		ai=(np.sum(w)*np.sum(w*x*y)-np.sum(w*x)*np.sum(w*y))/delta
		bi=(np.sum(w*y)*np.sum(w*x*x)-np.sum(w*x)*np.sum(w*x*y))/delta
		sbi=np.sqrt(np.sum(w*x*x)/delta)
		sai=np.sqrt(np.sum(w)/delta)
		print('aiest = ',aiest,'ai = ',ai, 'aiest-ai = ',aiest-ai)
		if np.abs(aiest-ai) < 1e-12 : break
	return ai,bi,sai,sbi

def u95(sr,sa,sb,npts):
	if npts <= 20 :
		da=sa*t95[npts-2]
		db=sb*t95[npts-2]
	if npts > 20 :
		da=sa*t95inf
		db=sb*t95inf
	return da, db

def u90(sr,sa,sb,npts):
	if npts <= 20 :
		da=sa*t90[npts-2]
		db=sb*t90[npts-2]
	if npts > 20 :
		da=sa*t90inf
		db=sb*t90inf
	return da, db


if __name__ == "__main__":
	'''
	--------------------------------------
	--------------------------------------
	- Test des fonctions least-square -
	--------------------------------------
	--------------------------------------
	'''
	# test x - y
	taille=np.array([160,170,180,190])
	poids=np.array([64,66,84,86])
	a,b,sr,sa,sb,r=ls(taille,poids)
	da,db=u90(sr,sa,sb,np.size(taille)-1)

	print ("pente = ","%3.2f" %a," +/- ","%3.2f" %da,' , 90 %')
	print ("y0 = ","%.f" %b," +/- ","%.f" %db,' , 90 %')
	