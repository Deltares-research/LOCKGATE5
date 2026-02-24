import numpy as np

# Subroutine VOL Functie
def VOL(h1, w1, w2, uo, dl, p, q, alfa):
    phi = np.zeros(101)
    for x in range(1, h1 + 1):
        phi[x] = -p[x, w1 + 1] + p[x, w1 + w2 + 1] + 0.5 * q[x]
        alfa[x] = phi[x] / uo

    V = 0.0
    for x in range(0, h1 + 1):
        V += alfa[x] * dl

    return V, alfa

# VELD subroutine
def VELD(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1] + p[x+1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

# PHI-RANDEN subroutines --> Deze rand is niet in beweging (grenst aan water of aan lucht)
    #bovenrand, phi=0
def P1(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z-1] + p[x+1, z]) / 5
    p[x, z] = po + rl * (pr - po)

    #linkerrand, phi=0
def P2(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x+1, z] + p[x, z-1]) / 5
    p[x, z] = po + rl * (pr - po)

    #benedenrand, phi=0
def P3(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1] + p[x+1, z]) / 5
    p[x, z] = po + rl * (pr - po)

    #rechterrand, phi=0
def P4(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x-1, z] + p[x, z-1]) / 5
    p[x, z] = po + rl * (pr - po)

# VN-RANDEN subroutines (Vaste randvoorwaarde, bodem of de kant van de sluis. Hier is dus geen debiet (q) mogelijk!)
    #bovenrand, vn=0
def V1(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z-1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

    #linkerrand, vn=0
def V2(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x+1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

    #benedenrand, vn=0
def V3(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

    #rechterrand, vn=0
def V4(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x-1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

# Q-RANDEN subroutines (grenzend aan de sluisdeur --> Q betekent er is beweging aan deze rand, gezien water in rust is, is de enige vorm van beweging afkomstig van de vibrerende deur)
    #bovenrand, qschuif
def Q1(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x-1, z] + p[x, z-1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

    #linkerrand, qschuif
def Q2(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x, z+1] + p[x+1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

    #benedenrand, qschuif
def Q3(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x-1, z] + p[x, z+1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

    #rechterrand, qschuif
def Q4(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x, z+1] + p[x-1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

# PHI/PHI-HOEKEN subroutines (hoeken die grenzen aan twee water/lucht randen)
def PP5(x, z, rl, p):
    po = p[x, z]
    pr = (p[x+1, z] + p[x, z-1]) / 6
    p[x, z] = po + rl * (pr - po)

def PP6(x, z, rl, p):
    po = p[x, z]
    pr = (p[x+1, z] + p[x, z+1]) / 6
    p[x, z] = po + rl * (pr - po)

def PP7(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1]) / 6
    p[x, z] = po + rl * (pr - po)

def PP8(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z-1]) / 6
    p[x, z] = po + rl * (pr - po)

# VN/VN-HOEKEN subroutines (hoeken die aan twee kanten een muur hebben, geen debieten dus)
def VV5(x, z, rl, p):
    po = p[x, z]
    pr = (p[x+1, z] + p[x, z-1]) / 2
    p[x, z] = po + rl * (pr - po)

def VV6(x, z, rl, p):
    po = p[x, z]
    pr = (p[x+1, z] + p[x, z+1]) / 2
    p[x, z] = po + rl * (pr - po)

def VV7(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1]) / 2
    p[x, z] = po + rl * (pr - po)

def VV8(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z-1]) / 2
    p[x, z] = po + rl * (pr - po)

# PHI/VN-HOEKEN Subroutines (Hoek met een rand water/lucht en andere rand een muur)
def PV5(x, z, rl, p):
    po = p[x, z]
    pr = (p[x+1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

def PV6(x, z, rl, p):
    po = p[x, z]
    pr = (p[x+1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def PV7(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def PV8(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

# Q/PHI-HOEKEN Subroutines (Hoek met een rand sluisdeur die vibreert en andere kant water/lucht)
def QP5(x, z, rl, p, q):
    #linkerbovenhoek, links q en boven phi=0
    po = p[x, z]
    pr = (q[z] + p[x+1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

def QP6(x, z, rl, p, q):
    #linkeronderhoek, links q en onder phi=0
    po = p[x, z]
    pr = (q[z] + p[x+1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def QP7(x, z, rl, p, q):
    #rechteronderhoek, rechts q en onder phi=0

    po = p[x, z]
    pr = (-q[z] + p[x-1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def QP8(x, z, rl, p, q):
    #rechterbovenhoek, rechts q en onder phi=0
    po = p[x, z]
    pr = (-q[z] + p[x-1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

# PHI/Q-HOEKEN Subroutines (Hoeken met een kant water/lucht, andere kant de sluisdeur)
def PQ5(x, z, rl, p, q):
    #Linkerbovenhoek, boven q en links phi=0
    po = p[x, z]
    pr = (-q[x] + p[x+1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

def PQ6(x, z, rl, p, q):
    #Linkeronderhoek, onder q en links phi=0
    po = p[x, z]
    pr = (-q[x] + p[x+1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def PQ7(x, z, rl, p, q):
    #rechteronderhoek, onder q en recht phi=0
    po = p[x, z]
    pr = (q[x] + p[x-1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def PQ8(x, z, rl, p, q):
    #Rechterbovenhoek, boven q en rechts phi=0
    po = p[x, z]
    pr = (q[x] + p[x-1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

#Q_VN-HOEKEN (Hoeken met een kant sluisdeur en andere rand een muur zonder debiet)
def QV5(x, z, rl, p, q):
    # linker bovenhoek, links q en boven vn=0
    po = p[x][z]
    pr = (q[z] + p[x+1][z] + p[x][z-1]) / 2
    p[x][z] = po + rl * (pr - po)

def QV6(x, z, rl, p, q):
    # linker onderhoek, links q en onder vn=0
    po = p[x][z]
    pr = (q[z] + p[x+1][z] + p[x][z+1]) / 2
    p[x][z] = po + rl * (pr - po)

def QV7(x, z, rl, p, q):
    # rechter onderhoek, rechts q en onder vn=0
    po = p[x][z]
    pr = (-q[z] + p[x-1][z] + p[x][z+1]) / 2
    p[x][z] = po + rl * (pr - po)

def QV8(x, z, rl, p, q):
    # rechter bovenhoek, rechts q en boven vn=0
    po = p[x][z]
    pr = (-q[z] + p[x-1][z] + p[x][z-1]) / 2
    p[x][z] = po + rl * (pr - po)

#VN/Q-HOEKEN (HOeken met een kant een muur en andere kant een sluisdeur)
def VQ5(x, z, rl, p, q):
    # linker bovenhoek, boven q en links vn=0
    po = p[x][z]
    pr = (-q[x] + p[x+1][z] + p[x][z-1]) / 2
    p[x][z] = po + rl * (pr - po)

def VQ6(x, z, rl, p, q):
    # linker onderhoek, onder q en links vn=0
    po = p[x][z]
    pr = (q[x] + p[x+1][z] + p[x][z+1]) / 2
    p[x][z] = po + rl * (pr - po)

def VQ7(x, z, rl, p, q):
    # rechter onderhoek, onder q en rechts vn=0
    po = p[x][z]
    pr = (q[x] + p[x-1][z] + p[x][z+1]) / 2
    p[x][z] = po + rl * (pr - po)

def VQ8(x, z, rl, p, q):
    # rechter bovenhoek, boven q en rechts vn=0
    po = p[x][z]
    pr = (-q[x] + p[x-1][z] + p[x][z-1]) / 2
    p[x][z] = po + rl * (pr - po)
