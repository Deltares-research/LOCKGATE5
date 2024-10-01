# Program HYM1
# Toegevoegde watermassa
# Om bodem roterende, verticale strip loodrecht op bodem
# aan een zijde water en water erboven

#In HYM1 zijn andere subroutines gebruikt dan zoals gedefineerd in HYMTR. Desondanks doen ze hetzelfde, hieronder zijn ze uitgewerkt:
# PROC1 = VELD (in het midden)
# PROC2 = PP5 (grenzend aan twee lucht/watervlakken)
# PROC3 = P2 (bovenin, grenzend aan 1 zijde lucht en 1 symmetrie zijde)
# PROC4 = Q2 (linkerpunt boven schuif)
# PROC5 = QV6 (linksonder, links deur en onder muur (Vn=0))
# PROC6 = V3 (muur beneden)
# PROC7 = PV7 (muur beneden en symmetrie rechts)
# PROC8 = P4 (Line of assymetrie rechts)
# PROC9 = PP8 (Hoekpunt rechtsboven)
# PROC10 = P1 (free surface boven/line of assymetrie)

# Laad packages in
import numpy as np
import HYMS
import importlib
importlib.reload(HYMS)
from HYMS import *
import matplotlib.pyplot as plt

# Constants and initializations
s = 20 #nummer strips op de deur
w = 22
h = 54
j = 0
wo = 1.0
dl = 1.0
rl = 1.7
epsn = 0.1
M = 0.0

q = np.zeros(101)
p = np.zeros((101, 101))
alfa = np.zeros(101)

def MOM(z, s, wo, dl, q, p, M, alfa):
    phi = np.zeros(101)
    for z in range(0, s+1):
        phi[z] = p[1, z] + 0.2 * q[z]
        alfa[z] = phi[z] / wo
    M = 0.0
    for z in range(0, s+1):
        M = alfa[z] * (z - 0.5) * dl

    return M,alfa


# Main loop

# ...BRONDEBIETEN
for i in range(0, s+1):
    q[i] = wo * (i - 0.5) * dl ** 2 #per coordinaat

while True and j < 1000:
    Mo = M
    j += 1

    # TER HOOGTE VAN ONDERRAND
    z = 0
    x = 0
    HYMS.QV6(x, z, rl, p, q)
    
    for x in range(1, h):
        HYMS.V3(x, z, rl, p)
    
    x = h
    HYMS.PV7(x, z, rl, p)

    # TER HOOGTE VAN BRONNEN
    for z in range(1, s+1):
        x = 0
        HYMS.Q2(x, z, rl, p, q)
        for x in range(1, h):
            HYMS.VELD(x, z, rl, p)
        x = h
        HYMS.P4(x, z, rl, p)

    # TER HOOGTE BOVEN BRONNEN
    for z in range(s+1, w):
        x = 0
        HYMS.P2(x, z, rl, p)
        for x in range(1, h):
            HYMS.VELD(x, z, rl, p)
        x = h
        HYMS.P4(x, z, rl, p)

    # TER HOOGTE VAN BOVENRAND
    z = w
    x = 0
    HYMS.PP5(x, z, rl, p)
    for x in range(1, h):
        P1(x, z, rl, p)
    x = h
    HYMS.PP8(x, z, rl, p)

    # MOMENT
    M,alfa = MOM(z, s, wo, dl, q, p, M, alfa)
    Md = M / ((s * dl) ** 4) #Dimensionless moment (s = breedte sluisdeur, dl = hoogte sluisdeur)

    eps = (M - Mo) / (M / j)

    print(j, M, Md)

    if eps <= epsn:
        break

for z in range(0, s+1):
    print(alfa[z])

plt.plot(alfa)
plt.title('alfa')
plt.xlim(0,s+1)
plt.ylabel('?')
plt.xlabel('?')

plt.figure()
plt.imshow(p.transpose(), cmap='bwr', origin='lower',vmin=-80,vmax=80)
plt.title('Element overview of potential flow field')
plt.xlabel('x-dir [m]')
plt.ylabel('y-dir [m]')
plt.xlim(1, len(p[1,:])-1)
plt.ylim(1, len(p[1,:])-1)
plt.colorbar(label='Value')