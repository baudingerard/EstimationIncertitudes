from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import math


def Ishigami(values):
    '''Non-monotonic Ishigami Function (3 parameters)
    First-order indices:
    x1: 0.3139
    x2: 0.4424
    x3: 0.0
    '''
    Y = np.zeros([values.shape[0]])
    A = 7
    B = 0.1
    for i, X in enumerate(values):
        Y[i] = math.sin(X[0]) + A * math.pow(math.sin(X[1]), 2) + \
        B * math.pow(X[2], 4) * math.sin(X[0])
    return Y


# definition du probleme
problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[-3.14159265359, 3.14159265359],
                   [-3.14159265359, 3.14159265359],
                   [-3.14159265359, 3.14159265359]]}

# generation des samples d entrees
paramvalues = saltelli.sample(problem, 1000, calc_second_order=True)
#  Le sampler Saltelli genere 8000 samples.
# Le sampler Saltelli genere N*(2D+2) samples,
# avec N=1000 (argument) et D=3 (le nombre d'entrees du modele)

# evaluation du modele
Y = Ishigami(paramvalues)

# analyse de la sortie
Si = sobol.analyze(problem, Y, conf_level=0.95, print_to_console=False)
# Si est un dictionnaire Python dont les cles sont
#"S1", "S2", "ST", "S1_conf", "S2_conf", et "ST_conf".
# Les cles  _conf stockent les intervals de confiance correspondantes
# typiquement avec un interval de confiance a 95%. 


# Impression du premier indice
print (Si['S1'])
# Impression de l'indice totale
print (Si['ST'])
# Impression des effets d'interaction
print ("x1-x2:", Si['S2'][0,1])
print( "x1-x3:", Si['S2'][0,2])
print ("x2-x3:", Si['S2'][1,2])

