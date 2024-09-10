# Program HYMA2
# Toegevoegde MASSATRAAGHEIDSMOMENT
# Om bodem roterende, verticale strip loodrecht op bodem
# aan een zijde water en water erboven

# Laad packages in
import numpy as np
from process import moment, proc

#-----------------------------------------------------------------------------
# Invoer
#-----------------------------------------------------------------------------
s = 6
w = 12
h = 54
wo = 1.
dl = 1.
rl = 1.5
epsn = .005
M = 0.


#-----------------------------------------------------------------------------
# Rekenen
#-----------------------------------------------------------------------------

# initialiseren
q = np.zeros(s)
p = np.zeros((h+1, w+1))
j = 0

# Bron debieten
for i in range(0, s):
    q[i] = wo * (i - 0.5) * dl**2

while True:
    Mo = M
    j += 1

    # ------
    # Door het domein
    p = proc(s, h, w, rl, p, q)

    # ------
    # Moment
    M, alfa = moment(s, wo, dl, q, p)
    Md = M / ((s*dl)**4)
    eps = (M-Mo) / (M/j)
    print(j, M, Md)

    if eps < epsn:
        for z in range(0, s):
            print(alfa[z])
        break
