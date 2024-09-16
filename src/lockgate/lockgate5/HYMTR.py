import numpy as np
import HYMS
import importlib
importlib.reload(HYMS)
from HYMS import *
import matplotlib.pyplot as plt

# Initialize parameters
w1 = 30     #Verticale afstand onderrand / strip (?)
w2 = 1      #Dikte strip (?)
w3 = 30     #Verticale afstand (?) strip / bovenrand
h1 = 10     #breedte strip (?) (alleen rechterhelft)
h2 = 50     #horinzontale afstand strip (?) / rechterrand
uo = 1.0        #Flow velocity? 
dl = 1.0        #Oppervlakte?
rl = 1.8        #Onbekend
epsn = 0.005    #Onbekend
V = 0.0001      #Onbekend

# Initialize arrays
q = np.zeros(101)       #Wordt de debiet array
p = np.zeros((101, 101))#Wordt de 
alfa = np.zeros(101)

# Brondebieten calculation
for i in range(1, h1 + 1):
    q[i] = uo * dl

j = 0
Vo = V

# Subroutine VOL Functie
def VOL(h1, w1, w2, uo, dl, p, q, alfa):
    phi = np.zeros(101)
    for x in range(1, h1 + 1):
        phi[x] = -p[x, w1 + 1] + p[x, w1 + w2 + 1] + 0.5 * q[x]
        alfa[x] = phi[x] / uo

    V = 0.0
    for x in range(1, h1 + 1):
        V += alfa[x] * dl

    return V, alfa

# Main loop
while True:
    Vo = V
    j += 1

    # Onderrand - call subroutines to compute p values
    z = 1
    #Links
    x = 1
    HYMS.PV6(x, z, rl, p) 
    #Onder
    for x in range(2, h1 + h2 + 1):
        HYMS.P3(x, z, rl, p)  
    #Rechts
    HYMS.PP7(h1 + h2 + 1, z, rl, p)  

    # Tussen onderrand en putten
    for z in range(2, w1 + 1):
        #links
        HYMS.V2(1, z, rl, p) 
        #veld
        for x in range(2, h1 + h2 + 1):
            HYMS.VELD(x, z, rl, p)  
        #Rechts
        HYMS.P4(h1 + h2 + 1, z, rl, p) 

    # Ter hoogte van putten
    z = w1 + 1
    HYMS.VQ5(1, z, rl, p, q)  # Placeholder for custom subroutine
    for x in range(2, h1 + 1):
        HYMS.Q1(x, z, rl, p, q)  # Placeholder for custom subroutine
    for x in range(h1 + 1, h1 + h2 + 1):
        HYMS.VELD(x, z, rl, p)  # Placeholder for custom subroutine
    HYMS.P4(h1 + h2 + 1, z, rl, p)  # Placeholder for custom subroutine

    # Ter hoogte van bronnen
    z = w1 + w2 + 1
    HYMS.VQ6(1, z, rl, p, q)  # Placeholder for custom subroutine
    for x in range(2, h1 + 1):
        HYMS.Q3(x, z, rl, p, q)  # Placeholder for custom subroutine
    for x in range(h1 + 1, h1 + h2 + 1):
        HYMS.VELD(x, z, rl, p)  # Placeholder for custom subroutine
    HYMS.P4(h1 + h2 + 1, z, rl, p)  # Placeholder for custom subroutine

    # Tussen bronnen en bovenrand
    for z in range(w1 + w2 + 2, w1 + w2 + w3 + 1):
        HYMS.V2(1, z, rl, p)  # Placeholder for custom subroutine
        for x in range(2, h1 + h2 + 1):
            HYMS.VELD(x, z, rl, p)  # Placeholder for custom subroutine
        HYMS.P4(h1 + h2 + 1, z, rl, p)  # Placeholder for custom subroutine

    # Bovenrand
    z = w1 + w2 + w3 + 1
    HYMS.PV5(1, z, rl, p)  # Placeholder for custom subroutine
    for x in range(2, h1 + h2 + 1):
        HYMS.P1(x, z, rl, p)  # Placeholder for custom subroutine
    HYMS.PP8(h1 + h2 + 1, z, rl, p)  # Placeholder for custom subroutine

    # Volume calculation
    V, alfa = VOL(h1, w1, w2, uo, dl, p, q, alfa)

    # Dimensieloos volume
    Vd = 2 * V / ((2 * h1 * dl) ** 2)

    # Check for convergence
    eps = (V - Vo) / (V / j)
    print(j, V, Vd)

    if eps <= epsn:
        break

# Output alfa !!!(IK denk rotatiesnelheid / versnelling?)
for x in range(1, h1 + 1):
    print(alfa[x])

for x in range(1, h1 + 1):
    print(p[x])

    

