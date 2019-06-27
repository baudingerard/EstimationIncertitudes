import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
import emcee

print('version emcee utilisee : ',emcee.__version__)

# Choix des vraies valeurs des parametres m, b, f
m_true = -0.9594
b_true = 4.294
f_true = 0.534
# Generation de donnees synthetiques entachees de leurs incertitudes
N = 50  # nombre de points
np.random.seed(123)  # initialisation du generateur de points aleatoires (pour la reproductibilite)
x = np.sort(10*np.random.rand(N))
y_true = m_true*x+b_true
yerr = 0.1+0.5*np.random.rand(N)
y= m_true*x+b_true
y += np.abs(f_true*y) * np.random.randn(N)  # sous-estimation volontaire via la fraction f
y += yerr * np.random.randn(N)
# trace des donnees et de la droite de reference
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['font.size']= 12
plt.errorbar(x, y, yerr=yerr, fmt=".k", capsize=0)
x0 = np.linspace(0, 10, 500)
plt.plot(x0, m_true*x0+b_true, "k", alpha=0.3, lw=3)
plt.xlim(0, 10)
plt.xlabel("x",fontsize=12)
plt.ylabel("y",fontsize=12)
plt.savefig("Vraie.png")
plt.show()

# minimisation de la fonction cout avec la methode des moindres carres - utilisation de numpy
A = np.vander(x, 2)
C = np.diag(yerr * yerr)
ATA = np.dot(A.T, A / (yerr**2)[:, None])
cov = np.linalg.inv(ATA)
w = np.linalg.solve(ATA, np.dot(A.T, y / yerr**2))
# impressions et traces
print('estimation par la methode des moindres carres:')
print('m = {0:.3f} +/- {1:.3f}'.format(w[0], np.sqrt(cov[0, 0])))
print('b = {0:.3f} +/- {1:.3f}'.format(w[1], np.sqrt(cov[1, 1])))
plt.errorbar(x, y, yerr=yerr, fmt=".k", capsize=0)
plt.plot(x0, m_true*x0+b_true, "k", alpha=0.3, lw=3, label="vraie")
plt.plot(x0, np.dot(np.vander(x0, 2), w), "k", label="LS")
plt.legend(fontsize=14)
plt.xlim(0, 10)
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("Vraie-LS.png")
plt.show()

# minimisation de la probabilite conditionnelle de y connaissant x
# avec le module optimize de scipy
def lnlike(theta, x, y, yerr):
    m, b, lnf = theta
    model = m * x + b
    sigma2 = yerr**2 + model**2*np.exp(2*lnf)
    return -0.5*(np.sum((y-model)**2/sigma2 + np.log(sigma2)))

nll = lambda *args: -lnlike(*args)
result = op.minimize(nll, [m_true, b_true, np.log(f_true)], args=(x, y, yerr))
m_ml, b_ml, lnf_ml = result.x

print("Maximums de probabilite estimes:")
print("m = {0:.3f}".format(m_ml))
print("b = {0:.3f}".format(b_ml))
print("f = {0:.3f}".format(np.exp(lnf_ml)))

plt.errorbar(x, y, yerr=yerr, fmt=".k", capsize=0)
plt.plot(x0, m_true*x0+b_true, "k", alpha=0.3, lw=3, label="vraie")
plt.plot(x0, np.dot(np.vander(x0, 2), w), "k--", label="LS")
plt.plot(x0, np.dot(np.vander(x0, 2), [m_ml, b_ml]), "k", label="ML")
plt.legend(fontsize=14)
plt.xlim(0, 10)
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("Vraie-LS-ML.png")
plt.show()

# minimization avec inference bayesienne
def lnprior(theta):
    m, b, lnf = theta
    if -5.0 < m < 0.5 and 0.0 < b < 10.0 and -10.0 < lnf < 1.0:
        return 0.0
    return -np.inf
def lnprob(theta, x, y, yerr):
    lp = lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta, x, y, yerr)

ndim, nwalkers = 3, 100
pos = [result["x"] + 1e-4*np.random.randn(ndim) for i in range(nwalkers)]

# MCMC
sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=(x, y, yerr))
sampler.run_mcmc(pos, 500)

# outil d analyse et de trace 
import corner
samples = sampler.chain[:, 50:, :].reshape((-1, ndim))
fig = corner.corner(samples, labels=["$m$", "$b$", "$\ln\,f$"], truths=[m_true, b_true, np.log(f_true)])
fig.savefig("triangle.png")

plt.close("all")
xl = np.array([0, 10])
for m, b, lnf in samples[np.random.randint(len(samples), size=100)]:
    plt.plot(xl, m*xl+b, color="k", alpha=0.05)
plt.plot(xl, m_true*xl+b_true, color="k", lw=2, alpha=0.8)
plt.errorbar(x, y, yerr=yerr, fmt=".k")
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("lastfig.png")
plt.show()

samples[:, 2] = np.exp(samples[:, 2])
m_mcmc, b_mcmc, f_mcmc = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),
	zip(*np.percentile(samples, [16, 50, 84],axis=0)))

print('m = {0:.3f}    +{1:.3f} -{1:.3f}'.format(m_mcmc[0], m_mcmc[1],m_mcmc[2]))
print('b = {0:.3f}    +{1:.3f} -{1:.3f}'.format(b_mcmc[0], b_mcmc[1],b_mcmc[2]))
print('f = {0:.3f}   +{1:.3f} -{1:.3f}'.format(f_mcmc[0], f_mcmc[1],f_mcmc[2]))

