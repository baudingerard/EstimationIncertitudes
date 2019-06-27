from mcerp import * # N, U, Gamma, Beta, correlate, etc.
import mcerp.umath as umath
import numpy as np

sp = 2 # deviation standard pour le rayon
# une deviation standard de 2 m en rayon sur chaque coin correspond a une deviation standard en x ou y de stv/sqrt(2)
sp = sp/umath.sqrt(2) 

x1 = N(0, sp)
y1 =N(0, sp)
x2 = N(100,sp)
y2 = N(0, sp)
x3 = N(0, sp)
y3 = N(50, sp)
x4 = N(100, sp)
y4 = N(50, sp)
 
# calcul des surfaces 
'''# approximatif
surface = umath.sqrt((x2-x1)**2+(y2-y1)**2)*umath.sqrt((x3-x1)**2+(y3-y1)**2)/2+umath.sqrt((x4-x2)**2+(y4-y2)**2)*umath.sqrt((x4-x3)**2+(y4-y3)**2)/2
'''
# exact
v12 = [x2-x1,y2-y1] ; v13 = [x3-x1, y3-y1] ; v14 = [x4-x1,y4-y1]
surface = np.cross(v12,v14)/2 + np.cross(v14,v13)/2

surface.describe()
print('surface.mean : ',surface.mean,'  stv : ',np.sqrt(surface.var))

'''
surface.mean :  4999.957807386318   stv :  157.22298079
'''
surface.plot(color="k")
surface.plot(hist=True,color="k",alpha=0.25)
surface.show()
print (' ')
print('correlation matrix:')
print (correlation_matrix([x1,y1,x2,y2,x3,y3,x4,y4]))

plotcorr([x1,y1,x2,y3,x3,y3,x4,y4], labels=['x1','y1','x2','y2','x3','y3','x4','y4'])
plt.show()
