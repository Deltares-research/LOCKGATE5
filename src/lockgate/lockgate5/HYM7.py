# Program HYMA7
#     TOEGEVOEGDE WATERMASSA
#     Verticaal translerende, horizontale strip
#     - Strip op enige afstand boven bodem
#     - Waterspiegel boven strip
#     - Rechterzijde

# Laad packages in
import numpy as np
from process import volume2, proc2

#-----------------------------------------------------------------------------
# Invoer
#-----------------------------------------------------------------------------
#     w1 = hoogte bodem/strip
#     w2 = dikte strip
#     w3 = hoogte strip wateroppervlak
#     h1 = breedte strip (rechterhelft)
#     h2 = breedte strip/rechterrand

w1 = 2
w2 = 2
w3 = 30
h1 = 10
h2 = 70
j = 0
uo = 1.
dl = 1.
rl = 1.8
epsn = .005
V = .0001


#-----------------------------------------------------------------------------
# Rekenen
#-----------------------------------------------------------------------------

# initialiseren
q = np.zeros(h1+1)
p = np.zeros((h1+h2+1, w1+w2+w3+1))
j = 0

# Bron debieten
for i in range(0, h1):
    q[i] = uo*dl

while True:
    Vo = V
    j += 1

    # ------
    # Door het domein
    p = proc2(h1, h2, w1, w2, w3, rl, p, q)

    # ------
    # Volume
    V, alfa = volume2(h1, w1, w2, uo, dl, p)
    Vd = 2*V / ((2*h1*dl)**2)
    eps = (V-Vo) / (V/j)
    print(j, V, Vd)

    if eps < epsn:
        for z in range(0, h1):
            print(alfa[z])
        break
