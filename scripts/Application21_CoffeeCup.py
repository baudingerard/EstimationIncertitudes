import chaospy as cp # To create distributions
import numpy as np # For the time array
from scipy . integrate import odeint # To integrate our equation
from matplotlib.pyplot import *
import pup

T0=273.15

# modele :analytique, represente l'ecart de temperature T-Ti
def u(t, a, T_env, T_i) :
	return T_env+(T_i-T_env)*np. exp(-a*t)


def coffee_cup (t, a , T_env, T_i ):
	# The equation describing the model
	def f(T, t , a , T_env ):
		return -a *(T - T_env )
	# Solving the equation by integration
	temperature = odeint (f, T_i , t , args =(a , T_env ))[: , 0]
	# Return time and model output
	return temperature

a=(0.001+0.01)/2.
T_env=20+T0
T_i=45+T0
ti=0.  # s
tf=1200.  # s
N=50

# Initial temperature and time array
t = np. linspace (ti, tf , N) #

Tana=u(t, a, T_env, T_i)
T= coffee_cup(t, a,T_env, T_i)
std=pup.snum(Tana,T,2)
print('standard deviation between the analytical and numerical solutions :')
print('snum : ',std)

amax=0.001
amin=0.0001
T_envmax=25+T0
T_envmin=15+T0

TamaxImax=coffee_cup(t, amax,T_envmin, T_i)
TamaxImin=coffee_cup(t, amax,T_envmax, T_i)
TaminImin=coffee_cup(t, amin,T_envmax, T_i)
TaminImax=coffee_cup(t, amin,T_envmin, T_i)

dist_a = cp.Uniform(amin, amax)
dist_T_env = cp.Uniform(T_envmin, T_envmax)
dist = cp.J(dist_a, dist_T_env)

#integration Monte Carlo avec plan de tirages Latin Hypercube 
samples = dist.sample(1000, rule="L")
sample_u = [coffee_cup(t, *s, T_i) for s in samples.T]

E = np.mean(sample_u,0)
Var = np.var(sample_u,0)
deviation = np.std(sample_u, 0)
'''
print('MC avec plan de tirages Latin Hypercube :')
print('E : ',E)
print('Var : ',Var)
'''
# prepare confidence level curves
nstd = 1. # to draw nstd-sigma intervals
u_up = E + nstd * deviation
u_dw = E - nstd * deviation

# range method
tinfini=3.29  # normal law
#tinfini=np.sqrt(3) # uniform law
srange=(TaminImin-TamaxImax)/2/tinfini
murange=(TaminImin+TaminImax+TamaxImin+TamaxImax)/4
nstdr=1. # to draw nstdr sigma intervals
Trange_up=murange +nstdr * srange
Trange_dw=murange - nstdr * srange
'''
# range method 4 points
cn=2.23  # normal law
#tinfini=np.sqrt(3) # uniform law
srange=(TaminImin-TamaxImax)/cn
murange=(TaminImin+TaminImax+TamaxImin+TamaxImax)/4
nstdr=1. # to draw nstdr sigma intervals
Trange_up=murange +nstdr * srange
Trange_dw=murange - nstdr * srange
'''

# affichage 
#plot
#set_cmap('gray')
fig, ax = subplots(1)
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16
rcParams['font.size']= 16
xlabel('t (s)', fontsize=14)
ylabel('T (K)', fontsize=14)
plot(t, E, 'k', lw=2, label='E MC & LH')
ax.fill_between(t, u_up, u_dw, color='0.7', alpha=.25, label='MC & LH, 1-sigma')
#plot(t,TamaxImax,'k',label='$DNS \ \ amax-Imax$')
#plot(t,TamaxImin,'c',label='$DNS \ \ amax-Imin$')
#plot(t,TaminImax,'r',label='$DNS \ \ amin-Imax$')
#plot(t,TaminImin,'m',label='$DNS \ \ amin-Imin$')
plot(t, murange, 'k--', lw=2, label='DNS & range')
ax.fill_between(t, Trange_up, Trange_dw, color='0.3', alpha=.35, label='DNS & range, 1-sigma')
legend(loc='lower left',frameon=False,fontsize=14)
ylim(290, 320)
xlim(0,1300)
gray()
# sauvegarde de l'image
#plt.savefig('T_coffee-cup.png')
show()
close()



