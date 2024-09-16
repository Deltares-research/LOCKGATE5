import numpy as np

# VELD subroutine
def VELD(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1] + p[x+1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

# PHI-RANDEN subroutines
def P1(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z-1] + p[x+1, z]) / 5
    p[x, z] = po + rl * (pr - po)

def P2(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x+1, z] + p[x, z-1]) / 5
    p[x, z] = po + rl * (pr - po)

def P3(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1] + p[x+1, z]) / 5
    p[x, z] = po + rl * (pr - po)

def P4(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x-1, z] + p[x, z-1]) / 5
    p[x, z] = po + rl * (pr - po)

# VN-RANDEN subroutines
def V1(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z-1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

def V2(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x+1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

def V3(x, z, rl, p):
    po = p[x, z]
    pr = (p[x-1, z] + p[x, z+1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

def V4(x, z, rl, p):
    po = p[x, z]
    pr = (p[x, z+1] + p[x-1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

# Q-RANDEN subroutines
def Q1(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x-1, z] + p[x, z-1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

def Q2(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x, z+1] + p[x+1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

def Q3(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x-1, z] + p[x, z+1] + p[x+1, z]) / 3
    p[x, z] = po + rl * (pr - po)

def Q4(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x, z+1] + p[x-1, z] + p[x, z-1]) / 3
    p[x, z] = po + rl * (pr - po)

# PHI/PHI-HOEKEN subroutines
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

# VN/VN-HOEKEN subroutines
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

# PHI/VN-HOEKEN Subroutines
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

# Q/PHI-HOEKEN Subroutines
def QP5(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x+1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

def QP6(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[z] + p[x+1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def QP7(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x-1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def QP8(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[z] + p[x-1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

# PHI/Q-HOEKEN Subroutines
def PQ5(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x+1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

def PQ6(x, z, rl, p, q):
    po = p[x, z]
    pr = (-q[x] + p[x+1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def PQ7(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x-1, z] + p[x, z+1]) / 4
    p[x, z] = po + rl * (pr - po)

def PQ8(x, z, rl, p, q):
    po = p[x, z]
    pr = (q[x] + p[x-1, z] + p[x, z-1]) / 4
    p[x, z] = po + rl * (pr - po)

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
