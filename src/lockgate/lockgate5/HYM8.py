# Program HYMA7
#     TOEGEVOEGDE WATERMASSA
#     Roterende deur in horizontaal vlak
#     Volledige omstroming om deurtip

# Laad packages in
import numpy as np
from process import moment2, proc2

#-----------------------------------------------------------------------------
# Invoer
#-----------------------------------------------------------------------------
#     w1 = hoogte bodem/strip
#     w2 = dikte strip
#     w3 = hoogte strip wateroppervlak
#     h1 = breedte strip (rechterhelft)
#     h2 = breedte strip/rechterrand

w1 = 40
w2 = 2
w3 = 40
h1 = 10
h2 = 50
j = 0
omega = 1.
dl = 1.
rl = 1.65
epsn = .005
M = .0001

#-----------------------------------------------------------------------------
# Rekenen
#-----------------------------------------------------------------------------

# initialiseren
q = np.zeros(h1+1)
p = np.zeros((h1+h2+1, w1+w2+w3+1))
j = 0

# Bron debieten
for i in range(0, h1):
    q[i] = omega*(i-0.5)*dl**2

while True:
    Mo = M
    j += 1

    # ------
    # Door het domein
    p = proc2(h1, h2, w1, w2, w3, rl, p, q)

    # ------
    # Volume
    M, alfa = moment2(h1, w1, w2, omega, dl, p)
    Md = M / ((h1*dl)**4)
    eps = (M-Mo) / (M/j)
    print(j, M, Md)

    if eps < epsn:
        for z in range(0, h1):
            print(alfa[z])
        break
