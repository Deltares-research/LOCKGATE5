
#TOEGEVOEGDE WATERMASSA
#Verticaal translerende, horizontale strip in oneidig water
#en alleen rechterzijde

#Gebaseerd op paper van P. A. Kolkman, "A simple scheme for calculating
#the added mass of hydraulic gates", Journal of Fluid and Structures
#1988, 2, 339-353

#Waterloopkundig Laboratorium
#A. Vrijburcht
#Q1442, 25 november 1993

#Vertaald van Fortran naar python door:
#N.L. Zuiderwijk
#2024

#In dit voorbeeld wordt aangenomen dat een deur in het verticale plane oscilleert. 
#Vanwege de aanname symmetrie in deur en afstand tot deurkas hoef je alleen het rechterdeel van de flow field te berekenen.
#x-dir: In het horizontale plane in get verlengde van de geopende deur en deurkas
#y-dir: In het verticale plane
#z-dir: In het horizontale plane loodrecht op de geopende deur en richting deurkas uit (de sluiskolk in)
#putten verwijst naar onderkant van de sluisdeur (strip)
#Bron verwijst naar bovenkant sluisdeur (strip)
import numpy as np
import HYMS
import importlib
importlib.reload(HYMS)
from HYMS import *
import matplotlib.pyplot as plt


# Initialize parameters
w1 = 30     #Verticale afstand onderrand / strip (?) Ik denk dat strip gaat over een rubberen strip die op de deurkas zit bevestigd om een spleet af te dichten/de deur zonder stoot te openen of het gaat om de spleet
w2 = 1      #Dikte strip (ookwel deur)
w3 = 30     #Verticale afstand (?) strip / bovenrand
h1 = 50     #breedte strip die de deur voorsteld (translerende deel).
h2 = 10     #horinzontale afstand strip (ookwel deur) tot de zijkant van de deurkas (we berekenen maar helft van het flow field vanwege aanname symmetrisch dus alleen rechterhelft)
#h1 + h2 = totale lengte deur in horizontale plane en de afstand deur tot deurkas
uo = 1.0        #Snelheid van de translerende beweging deur (m/s)
dl = 1.0        #deurdikte (m in z-plane) dus de diepte in
rl = 1.8        #Relaxation factor (usually 1.5-1.7)
epsn = 0.05    #Nauwkeurigheidsmarge (95%), Accuracy range
V = 0.00      #Volume (Maar waarvan?)

# Initialize arrays
q = np.zeros(101)       #Wordt de debiet array
p = np.zeros((101, 101))#Wordt de pressure array per tak/strip?
alfa = np.zeros(101) #wordt de array van ratio (potential / velocity vector) langs de lengte van de sluisdeur

# Brondebieten (in m^2/s)
for i in range(1, h1 + 1):
    q[i] = uo * dl

j = 0
Vo = V

# Main loop
while True:
    Vo = V
    j += 1

    ###########################################################
    #### Onderrand ####
    z = 1
    #Links
    x = 1
    HYMS.PV6(x, z, rl, p) 
    #Onder
    for x in range(2, h1 + h2 + 1):
        HYMS.P3(x, z, rl, p)  
    #Rechts
    HYMS.PP7(h1 + h2 + 1, z, rl, p)  

    ###########################################################
    #### Tussen onderrand en putten ####
    for z in range(2, w1 + 1):
        #links
        HYMS.V2(1, z, rl, p) 
        #veld
        for x in range(2, h1 + h2 + 1):
            HYMS.VELD(x, z, rl, p)  
        #Rechts
        HYMS.P4(h1 + h2 + 1, z, rl, p) 

    ###########################################################
    # Ter hoogte van putten
    z = w1 + 1
    #links
    HYMS.VQ5(1, z, rl, p, q)  
    #putten
    for x in range(2, h1 + 1):
        HYMS.Q1(x, z, rl, p, q) 
    #veld
    for x in range(h1 + 1, h1 + h2 + 1):
        HYMS.VELD(x, z, rl, p) 
    #rechts
    HYMS.P4(h1 + h2 + 1, z, rl, p) 

    ###########################################################
    # Ter hoogte van bronnen
    z = w1 + w2 + 1
    #links
    HYMS.VQ6(1, z, rl, p, q) 
    #bronnen
    for x in range(2, h1 + 1):
        HYMS.Q3(x, z, rl, p, q)  
    #veld
    for x in range(h1 + 1, h1 + h2 + 1):
        HYMS.VELD(x, z, rl, p)
    #rechts
    HYMS.P4(h1 + h2 + 1, z, rl, p) 

    ###########################################################
    # Tussen bronnen en bovenrand
    #links
    for z in range(w1 + w2 + 2, w1 + w2 + w3 + 1):
        HYMS.V2(1, z, rl, p) 
        #veld
        for x in range(2, h1 + h2 + 1):
            HYMS.VELD(x, z, rl, p)  
        #rechts
        HYMS.P4(h1 + h2 + 1, z, rl, p) 

    ###########################################################
    # Bovenrand
    z = w1 + w2 + w3 + 1
    #links
    HYMS.PV5(1, z, rl, p) 
    #boven
    for x in range(2, h1 + h2 + 1):
        HYMS.P1(x, z, rl, p) 
    #rechts
    HYMS.PP8(h1 + h2 + 1, z, rl, p) 

    # Volume calculation
    V, alfa = VOL(h1, w1, w2, uo, dl, p, q, alfa) #Deze stap is me nog onbekend

    # Dimensieloos volume
    Vd = 2 * V / ((2 * h1 * dl) ** 2) #Still dont get is, V is in m3, h1 in m and dl in m --> (h1*dl) ^2 is not m3?

    # Check for convergence
    eps = (V - Vo) / (V / j)
    print(j, V, Vd)

    if eps <= epsn:
        break

#remove all first rows
alfa = alfa[1::]
p = p[1::,1::]

# Output alfa !!!(IK denk rotatiesnelheid / versnelling?)
for x in range(0, h1 + 1):
    print(alfa[x])

plt.plot(alfa)
plt.title('alfa')
plt.ylabel('?')
plt.xlabel('?')

plt.figure()
plt.imshow(p.transpose(), cmap='bwr', origin='lower',vmin=-30,vmax=30)
plt.title('Element overview of potential flow field')
plt.xlabel('x-dir [m]')
plt.ylabel('y-dir [m]')
plt.xlim([0,h1+h2])
plt.ylim([0,w1+w2+w3])
plt.colorbar(label='Value')

