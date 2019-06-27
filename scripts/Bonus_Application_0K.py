# import de librairies
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op

t95=np.array([12.7,4.30,3.18,2.78,2.57,2.45,2.36,2.31,2.26,2.23,
                      2.2,2.18,2.16,2.14,2.13,2.12,2.11,2.10,2.09,2.09])
t95inf=2.

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

def u95(sa,sb,npts):
	if npts <= 20 :
		da=sa*t95[npts-2]
		db=sb*t95[npts-2]
	if npts > 20 :
		da=sa*t95inf
		db=sb*t95inf
	return da, db

if __name__ == "__main__":
	'''
	--------------------------------------
	--------------------------------------
	- Test des fonctions least-square -
	--------------------------------------
	--------------------------------------
	'''
	# points 
	p=np.array([1013,1130,1112,1093,1072,1061,1049])  # x
	teta=np.array([19.8,52.9,47.8,42.4,36.2,33.5,30.2])  # y

	# modele: PV=nRT=nR(teta-teta0K), soit teta=teta0+ (V/nR)*P
	# on va rechercher teta0 en degres C a partir des points de refroidissement
	# on note a=V/nR=a et b=teta0

	a,b,sr,sa,sb,r=ls(p,teta)
	da,db=u95(sa,sb,np.size(p)-1)
	print ("PV/nR = ","%4.3f" %a," +/- ","%4.3f" %da,' deg. C , 95 %')
	print ("teta0 = ","%4.1f" %b," +/- ","%4.1f" %db,' deg. C , 95 %')
	print ("correlation coef. = ","%6.5f" %r)

	# avec incertitudes, P : 1 %, teta : 1 deg. C
	dp=p*1/300
	dteta=np.array([1,1,1,1,1,1,1])

	ai,bi,sai,sbi=lsUncertainties(p,teta,dp,dteta)
	dai,dbi=u95(sai,sbi,np.size(p)-1)
	print ("PV/nR = ","%4.3f" %ai," +/- ","%4.3f" %dai,' deg. C , 95 %')
	print ("teta0 = ","%4.1f" %bi," +/- ","%4.1f" %dbi,' deg. C , 95 %')

	# trace des donnees et de la droite de reference
	plt.errorbar(p, teta, yerr=dteta,  xerr=dp, fmt=".k", capsize=0,label='points exp.')
	x0 = np.linspace(1000, 1150, 10)
	plt.plot(x0, a*x0+b,"b",label='sans incertitudes')
	plt.plot(x0, ai*x0+bi,"r",label='avec incertitudes')
	plt.legend(fontsize=14)
	plt.xlim(1000, 1150)
	plt.xlabel("p (mbar)")
	plt.ylabel("teta (deg. C)")
	#plt.savefig("Vraie.png")
	plt.show()
	