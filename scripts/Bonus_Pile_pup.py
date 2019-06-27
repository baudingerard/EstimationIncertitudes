# import de librairies
import numpy as np
import matplotlib.pyplot as plt
import pup


'''
--------------------------------------
--------------------------------------
- Test des fonctions least-square -
--------------------------------------
--------------------------------------
'''
# points 
U=np.array([4.731,4.731,4.730,4.728,4.724,4.724,4.722,4.721,4.719,4.716])  # x
I=np.array([92.83e-6,115.45e-6,152.65e-6,0.2352e-3,0.4686e-3,0.520e-3,0.5841e-3,0.6661e-3,0.775e-3,0.9264e-3])  # y

# modele: U=E-R*I
#a=-R
#b=E

a,b,sr,sa,sb,r=pup.ls(I,U)
da,db=pup.u95ab(sa,sb,np.size(I)-1)
print ("R = ","%3.2f" %a," +/- ","%3.2f" %da,' Ohm, 95 %')
print ("E = ","%5.4f" %b," +/- ","%5.4f" %db,' V, 95 %')
print ("correlation coef. = ","%6.5f" %r)

# avec incertitudes
dU=U*0.05/100+0.003
dI=I*0.2/100
dI[0:3]=dI[0:3]+0.03e-6
dI[4:np.size(I)]=dI[4:np.size(I)]+0.0003e-3

ai,bi,sai,sbi=pup.lsUncertainties(I,U,dI,dU)
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
	