from SALib.sample import saltelli
from SALib.analyze import sobol
import cupCool
import numpy as np


# definition du probleme
# Y=T-Ti= I*np. exp(-a*t)
#  x1:t, x2:I, x3:a
problem = {
    'num_vars': 3,
    'names': ['x1', 'x2', 'x3'],
    'bounds': [[0,500],
                   [10, 16],
                   [0.0001, 0.001]]}

# generation des samples d entrees
paramvalues = saltelli.sample(problem, 1000, calc_second_order=True)
# Le sampler Saltelli genere 8000 samples.
# Le sampler Saltelli genere N*(2D+2) samples,
# avec N=1000 (argument) et D=3 (le nombre d'entrees du modele)

# evaluation du modele
Y = cupCool.evaluate(paramvalues)

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


