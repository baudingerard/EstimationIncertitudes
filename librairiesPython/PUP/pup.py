# import de librairies
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op

'''
t95(Nlib) : tableau renvoyant le coefficient de Student pour Nlib
degres de liberte
'''
t95=np.array([12.7,4.30,3.18,2.78,2.57,2.45,2.36,2.31,2.26,2.23,
                      2.2,2.18,2.16,2.14,2.13,2.12,2.11,2.10,2.09,2.09])
t95inf=2.

def mean(x):
	'''
	calcule la moyenne d'une serie de valeurs x
	retourne : xm
	'''
	N=np.size(x)
	xm=np.sum(x)/N
	return xm
	
def sigma(x):
	'''
	calcule l'ecart type d'une serie de valeurs x
	retourne : sigma
	'''
	N=np.size(x)
	xm= mean(x)
	s=np.sqrt(np.sum((x-xm)*(x-xm))/(N-1))
	return s

def ls(x,y):
        '''
        resoud par les moindres carres la regression lineaire y=a+bx
        retourne a, b, sr (ecart type des residus), sa (ecart type sur a),
        sb (ecart type sur b),     r (coefficient de correlation
        utilisation : a,b,sr,sa,sb,r=pup.ls(x,y)
        '''
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
	'''
	resoud par les moindres carres avec incertitudes dx et dy
	la regression lineaire y=a+bx
	retourne a, b,  sa (ecart type sur a), sb (ecart type sur b)
	utilisation : a,b,sa,sb,r=pup.lsUncertainties(x,y,dx,dy)
	'''
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

def u95(sx,N):
        '''
        calcule l'incertitude etendue d'une grandeur x a partir
        de son ecart-type sx et du nombre de points
        retourne : dx
        '''
        if N <= 20 :
              dx=sx*t95[N-2]/np.sqrt(N)
        if N > 20 :
              dx=sx*t95inf/np.sqrt(N)
        return dx

def u95ab(sa,sb,N):
	'''
	calcule l'incertitude etendue d'un couple de granderus a, b a partir
	de leurs ecarts-types sa, sb et du nombre de points
	retourne : da, db
	'''
	if N <= 20 :
		da=sa*t95[N-2]
		db=sb*t95[N-2]
	if N > 20 :
		da=sa*t95inf
		db=sb*t95inf
	return da, db

def snum(yana,ynum,n):
	'''
	calcule la deviation standard entre une serie de grandeurs numeriques
	et une serie de grandeurs analytiques a l'ordre n
	yana et ynum doivent etre de la meme dimension
	retourne : snum
	utilisation : std=pup.snum(Yana,Ynum,2), ici n=2 (somme des carres)
	'''
	N=np.size(yana)
	sn=(np.sum((yana-ynum)**n))**(1/n)/N
	return sn

if __name__ == "__main__":
	'''
	------------------------------------------------------------
	------------------------------------------------------------
	- Test des fonctions least-square sur application pile -
	------------------------------------------------------------
	------------------------------------------------------------
	'''
	# points 
	U=np.array([4.731,4.731,4.730,4.728,4.724,4.724,4.722,4.721,4.719,4.716])  # x
	I=np.array([92.83e-6,115.45e-6,152.65e-6,0.2352e-3,0.4686e-3,0.520e-3,0.5841e-3,0.6661e-3,0.775e-3,0.9264e-3])  # y

	# modele: U=E-R*I
	#a=-R
	#b=E

	a,b,sr,sa,sb,r=ls(I,U)
	da,db=u95ab(sa,sb,np.size(I)-1)
	print ("R = ","%3.2f" %a," +/- ","%3.2f" %da,' Ohm, 95 %')
	print ("E = ","%5.4f" %b," +/- ","%5.4f" %db,' V, 95 %')
	print ("correlation coef. = ","%6.5f" %r)

	# avec incertitudes
	dU=U*0.05/100+0.003
	dI=I*0.2/100
	dI[0:3]=dI[0:3]+0.03e-6
	dI[4:np.size(I)]=dI[4:np.size(I)]+0.0003e-3

	ai,bi,sai,sbi=lsUncertainties(I,U,dI,dU)
	print ("R = ","%3.2f" %ai," +/- ","%3.2f" %sai,' Ohm, 95 %')
	print ("E = ","%5.4f" %bi," +/- ","%5.4f" %sbi,' V, 95 %')

	# trace des donnees et de la droite de reference
	plt.errorbar(I, U, xerr=dI, yerr=dU,  fmt=".k", capsize=0,label='points exp.')
	#plt.plot(I,U,"ok", label='points exp.')
	Ic= np.linspace(90.e-6, 1.e-3, 50)
	Uc=a*Ic+b
	plt.plot(Ic, Uc,"b",label='sans incertitudes')
	plt.plot(Ic, ai*Ic+bi,"r",label='avec incertitudes')
	plt.legend(fontsize=14)
	plt.ylabel("U (V)")
	plt.xlabel("I (A)")
	plt.show()
	
	'''
	------------------------------------------
	------------------------------------------
	- Test des fonctions mean et sigma  -
	------------------------------------------
	------------------------------------------
	'''
	psup=np.array([17.04,16.46,16.10,16.46,17.50])
	pmsup=mean(psup)
	spsup=sigma(psup)
	dpsup=u95(spsup,np.size(psup)-1)
	print(" ")
	print('N =',np.size(psup))
	print ('t(N-1) =',t95[np.size(psup)-2])
	print ("pression sup = ","%4.2f" %pmsup," +/- ","%4.2f" %dpsup,' , 95 %')
	print(' ')