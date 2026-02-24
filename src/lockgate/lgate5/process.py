# Process functies
import numpy as np

# ------ VELD
def VELD(x, z, rl, p):
    " Binnenelementen "
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z + 1] + p[x + 1, z] + p[x, z - 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

# ------ PHI-randen
def P1(x, z, rl, p):
    " bovenrand, phi=0 "
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z - 1] + p[x + 1, z]) / 5
    p[x, z] = po + rl * (pr - po)
    return p

def P2(x, z, rl, p):
    " linkerrand, phi=0 "
    po = p[x, z]
    pr = (p[x, z + 1] + p[x + 1, z] + p[x, z - 1]) / 5
    p[x, z] = po + rl * (pr - po)
    return p

def P3(x, z, rl, p):
    " onderrand, phi=0 "
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z + 1] + p[x + 1, z]) / 5
    p[x, z] = po + rl * (pr - po)
    return p

def P4(x, z, rl, p):
    " rechterrand, phi=0 "
    po = p[x, z]
    pr = (p[x, z + 1] + p[x - 1, z] + p[x, z - 1]) / 5
    p[x, z] = po + rl * (pr - po)
    return p

# --------- VN-randen
def V1(x, z, rl, p):
    " bovenrand, vn=0 "
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z - 1] + p[x + 1, z]) / 3
    p[x,z] = po + rl * (pr - po)    
    return p 

def V2(x, z, rl, p):
    " linkerrand, vn=0 "
    po = p[x, z]
    pr = (p[x, z + 1] + p[x + 1, z] + p[x, z - 1]) / 3
    p[x, z] = po + rl * (pr - po)
    return p

def V3(x, z, rl, p):
    " onderrand, vn=0 "
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z + 1] + p[x + 1, z]) / 3
    p[x, z] = po + rl * (pr - po)
    return p

def V4(x, z, rl, p):
    " rechterrand, vn=0 "
    po = p[x, z]
    pr = (p[x, z + 1] + p[x - 1, z] + p[x, z - 1]) / 3
    p[x, z] = po + rl * (pr - po)
    return p  


# --------- Q-randen
def Q1(x, z, rl, p, q):
    " bovenrand, qschuif "
    po = p[x, z]
    pr = (-q[x] + p[x - 1, z] + p[x, z - 1] + p[x + 1, z]) / 3
    p[x, z] = po + rl * (pr - po)
    return p

def Q2(x, z, rl, p, q):
    " linkerrand, qschuif "
    po = p[x, z]
    pr = (q[z] + p[x, z + 1] + p[x + 1, z] + p[x, z - 1]) / 3
    p[x, z] = po + rl * (pr - po)
    return p

def Q3(x, z, rl, p, q):
    " onderrand, qschuif "
    po = p[x, z]
    pr = (q[x] + p[x - 1, z] + p[x, z + 1] + p[x + 1, z]) / 3
    p[x, z] = po + rl * (pr - po)
    return p

def Q4(x, z, rl, p, q):
    " rechterrand, qschuif "
    po = p[x, z]
    pr = (-q[z] + p[x, z + 1] + p[x - 1, z] + p[x, z - 1]) / 3
    p[x, z] = po + rl * (pr - po)
    return p

# --- Corners:
# PHI/PHI-HOEKEN
def PP5(x, z, rl, p):
    po = p[x, z]
    pr = (p[x + 1, z] + p[x, z - 1]) / 6
    p[x, z] = po + rl * (pr - po)
    return p

def PP6(x, z, rl, p):
    po = p[x, z]
    pr = (p[x + 1, z] + p[x, z + 1]) / 6
    p[x, z] = po + rl * (pr - po)
    return p

def PP7(x, z, rl, p):
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z + 1]) / 6
    p[x, z] = po + rl * (pr - po)
    return p

def PP8(x, z, rl, p):
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z - 1]) / 6
    p[x, z] = po + rl * (pr - po)
    return p

# VN/VN-HOEKEN
def VV5(x, z, rl, p):
    po = p[x, z]
    pr = (p[x + 1, z] + p[x, z - 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def VV6(x, z, rl, p):
    po = p[x, z]
    pr = (p[x + 1, z] + p[x, z + 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def VV7(x, z, rl, p):
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z + 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def VV8(x, z, rl, p):
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z - 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

# PHI/VN-HOEKEN
def PV5(x, z, rl, p):
    po = p[x, z]
    pr = (p[x + 1, z] + p[x, z - 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def PV6(x, z, rl, p):
    po = p[x, z]
    pr = (p[x + 1, z] + p[x, z + 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def PV7(x, z, rl, p):
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z + 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def PV8(x, z, rl, p):
    po = p[x, z]
    pr = (p[x - 1, z] + p[x, z - 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

# Q/PHI-HOEKEN
def QP5(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x + 1, z] + p[x, z - 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def QP6(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x + 1, z] + p[x, z + 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def QP7(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x - 1, z] + p[x, z + 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def QP8(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x - 1, z] + p[x, z - 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

# PHI/Q-HOEKEN
def PQ5(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x + 1, z] + p[x, z - 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def PQ6(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x + 1, z] + p[x, z + 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def PQ7(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x - 1, z] + p[x, z + 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

def PQ8(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x - 1, z] + p[x, z - 1]) / 4
    p[x, z] = po + rl * (pr - po)
    return p

# Q/VN-HOEKEN
def QV5(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x + 1, z] + p[x, z - 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def QV6(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x + 1, z] + p[x, z + 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def QV7(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x - 1, z] + p[x, z + 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def QV8(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x - 1, z] + p[x, z - 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

# VN/Q-HOEKEN
def VQ5(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x + 1, z] + p[x, z - 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def VQ6(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x + 1, z] + p[x, z + 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def VQ7(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x - 1, z] + p[x, z + 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

def VQ8(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x - 1, z] + p[x, z - 1]) / 2
    p[x, z] = po + rl * (pr - po)
    return p

# ------- Subroutines
def volume(s, uo, dl, q, p):
    # Functie volume 
    phi = np.zeros(s)
    alfa = np.zeros(s)
    
    for z in range(0, s):
        phi[z] = p[0, z] + 0.2 * q[z]
        alfa[z] = phi[z] / uo
    
    V = 0.0
    for z in range(1, z):
        V += alfa[z] * dl
    
    return V, alfa
def volume2(h1, w1, w2, uo, dl, p):
    # Functie volume with two sizes
    phi = np.zeros(h1)
    alfa = np.zeros(h1)

    for x in range(0, h1):
        phi[x] = -p[x, w1+1] + p[x, (w1+w2+1)]
        alfa[x] = phi[x] / uo

    V = 0.0
    for x in range(0, h1):
        V += alfa[x]*dl

    return V, alfa
    
def moment(s,wo,dl,q,p):
    # Functie massatraagheidsmoment 
    phi = np.zeros(s)
    alfa = np.zeros(s)

    for z in range(0, s):
        phi[z] = p[0, z] + .2*q[z]
        alfa[z] = phi[z] / wo

    M = 0.0
    for z in range(0, s):
        M = M + alfa[z]*(z-0.5)*dl #TODO: Is this ok?
    
    return M, alfa

def moment2(h1, w1, w2, omega, dl, p):
    # Functie massatraagheidsmoment
    phi = np.zeros(h1)
    alfa = np.zeros(h1)

    for z in range(0, h1):
        phi[z] = - p[z, w1+1] + p[z, (w1+w2+1)]
        alfa[z] = phi[z]/omega

    M = 0.0
    for z in range(0, h1):
        M = M + alfa[z] * (z - 0.5) * dl**2

    return M, alfa

# -------- Total routine
def proc(s, h, w, rl, p, q):
    # Ter hoogte van onderrand
    #   linksonder
    z = 0
    x = 0
    p = QV6(x, z, rl, p, q)

    #   onderrand
    for x in range(1, h):
        p = V3(x, z, rl, p)

    #   rechtsonder
    x = h
    p = PV7(x, z, rl, p) 

    # -----
    # Ter hoogte van bronnen
    for z in range(1, s):
        #   bronnen
        x = 0
        p = Q2(x, z, rl, p, q)
        #   rechts van bronnen
        for x in range(1, h):
            p = VELD(x, z, rl, p)
        #   uiterst rechts van bronnen
        x = h
        p = P4(x, z, rl, p)


    # -----
    # Ter hoogte boven bronnen
    for z in range(s, w):
        #   linkerrand boven bronnen
        x = 0
        p = P2(x,z,rl,p)
        #   rechts boven bronnen
        for x in range(1, h):
            p = VELD(x, z, rl, p)
        #   uiterst rechts boven bronnen
        x = h
        p = P4(x, z, rl, p)
            

    # ------    
    # Ter hoogte bovenrand
    z = w
    x = 0
    p = PP5(x, z, rl, p)
    for x in range(1, h):
        p = P1(x, z, rl, p)
    x = h
    p = PP8(x, z, rl, p)

    return p

def proc2(h1, h2, w1, w2, w3, rl, p, q):
    # Ter hoogte van onderrand
    #   linksonder
    z = 0
    x = 0
    p = VV6(x, z, rl, p)

    #   onderrand
    for x in range(1, h1+h2):
        p = V3(x, z, rl, p)

    #   rechtsonder
    x = h1 + h2
    p = PV7(x, z, rl, p)

    # -----
    # Tussen onderrand en putten
    for z in range(1, w1):
        #  links
        x = 0
        p = V2(x, z, rl, p)
        #   veld
        for x in range(1, h1+h2):
            p = VELD(x, z, rl, p)
        #  rechts
        x = h1+h2
        p = P4(x, z, rl, p)

    # -----
    # Ter hoogte van putten
    z = w1
    # Links
    x = 0
    p = VQ6(x, z, rl, p, q)
    # putten
    for x in range(1, h1):
        p = Q1(x, z, rl, p, q)
    # veld
    for x in range(h1, h1+h2):
        p = VELD(x, z, rl, p)
    # rechts
    x = h1+h2
    p = P4(x, z, rl, p)

    # -----
    # Ter hoogte van schuif
    for z in range(w1+1, w1+w2):
        # links bij schuif
        x = h1
        p = V2(x, z, rl, p)
        # veld
        for x in range(h1 + 1, h1 + h2):
            p = VELD(x, z, rl, p)
        # uiterst rechts boven bronnen
        x = h1+h2
        p = P4(x, z, rl, p)

    # -----
    # Ter hoogte van bronnen
    z = w1 + w2
    x = 0
    p = VQ6(x, z, rl, p, q)
    for x in range(1, h1):
        p = Q3(x, z, rl, p, q)
    for x in range(h1, h1 + h2):
        p = VELD(x, z, rl, p)
    x = h1 + h2
    p = P4(x, z, rl, p)

    # -----
    # Tussen bonnen en bovenrand
    for z in range((w1+w2+1), (w1+w2+w3)):
        # links
        x = 0
        p = V2(x, z, rl, p)
        # Veld
        for x in range(1, h1+h2):
            p = VELD(x, z, rl, p)
        # rechts
        x = h1+h2
        p = P4(x, z, rl, p)

    # -----
    # Bovenrand
    z = w1+w2+w3
    # links
    x = 0
    p = PV5(x, z, rl, p)
    # boven
    for x in range(1, h1+h2):
        p = P1(x, z, rl, p)
    # rechts
    x = h1+h2
    p = PP8(x, z, rl, p)

    return p

def proc3(h1, h2, w1, w2, w3, rl, p, q):
    # Ter hoogte van onderrand
    #   linksonder
    z = 0
    x = 0
    p = PV6(x, z, rl, p)

    #   onderrand
    for x in range(1, h1+h2):
        p = P3(x, z, rl, p)

    #   rechtsonder
    x = h1 + h2
    p = PP7(x, z, rl, p)

    # -----
    # Tussen onderrand en putten
    for z in range(1, w1):
        #  links
        x = 0
        p = V2(x, z, rl, p)
        #   veld
        for x in range(1, h1+h2):
            p = VELD(x, z, rl, p)
        #  rechts
        x = h1+h2
        p = P4(x, z, rl, p)

    # -----
    # Ter hoogte van putten
    z = w1
    # Links
    x = 0
    p = VQ5(x, z, rl, p, q)
    # putten
    for x in range(1, h1):
        p = Q1(x, z, rl, p, q)
    # veld
    for x in range(h1, h1+h2):
        p = VELD(x, z, rl, p)
    # rechts
    x = h1+h2
    p = P4(x, z, rl, p)

    # -----
    # Ter hoogte van schuif
    for z in range(w1+1, w1+w2):
        # links bij schuif
        x = h1
        p = V2(x, z, rl, p)
        # veld
        for x in range(h1 + 1, h1 + h2):
            p = VELD(x, z, rl, p)
        # uiterst rechts boven bronnen
        x = h1+h2
        p = P4(x, z, rl, p)

    # -----
    # Ter hoogte van bronnen
    z = w1 + w2
    x = 0
    p = VQ6(x, z, rl, p, q)
    for x in range(1, h1):
        p = Q3(x, z, rl, p, q)
    for x in range(h1, h1 + h2):
        p = VELD(x, z, rl, p)
    x = h1 + h2
    p = P4(x, z, rl, p)

    # -----
    # Tussen bonnen en bovenrand
    for z in range((w1+w2+1), (w1+w2+w3)):
        # links
        x = 0
        p = V2(x, z, rl, p)
        # Veld
        for x in range(1, h1+h2):
            p = VELD(x, z, rl, p)
        # rechts
        x = h1+h2
        p = P4(x, z, rl, p)

    # -----
    # Bovenrand
    z = w1+w2+w3
    # links
    x = 0
    p = PV5(x, z, rl, p)
    # boven
    for x in range(1, h1+h2):
        p = P1(x, z, rl, p)
    # rechts
    x = h1+h2
    p = PP8(x, z, rl, p)

    return p
