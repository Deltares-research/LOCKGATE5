# Program HYM1
# Toegevoegde watermassa
# Horizontaal translerende, vertical strip loodrecht op bodem
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

#-----------------------------------------------------------------------------
# Invoer
#-----------------------------------------------------------------------------
s = 12 #Breedte van de sluisdeur (of #nummer strips op de deur)
w = 20 #Coordinaat van de bovenrand water
h = 10 #Afstand muur deurkas tot aan sluisdeur
uo = 1. #Snelheid van de translerende sluis deur
dl = 1. #stapje in lengte langzij deurlengte
rl = 1.5 #Relaxation factor
epsn = .025 #Nauwkeurigheidsmarge (97.5%)
V = 0.01

#-----------------------------------------------------------------------------
# Rekenen
#-----------------------------------------------------------------------------

# initialiseren
q = np.zeros(101)       #Wordt de debiet array
p = np.zeros((101, 101))#Wordt de pressure array per tak/strip?
alfa = np.zeros(101) #wordt de array van ratio (potential / velocity vector) langs de lengte van de sluisdeur
phi = np.zeros(101)

#SUBROUTINE VOL1
def VOL1(z,s,uo,dl,q,p,V,alfa):
	for z in range (0,s+1):
		phi[z] = p[0,z] + 0.2*q[z]
		alfa[z] = phi[z]/uo
	V = 0
	for z in range (0, s+1):
		V = V + alfa[z]*dl
	
	return V, alfa

j = 0

# Bron debieten
for i in range(0, s+1):
    q[i] = uo * dl

while True:
	Vo = V
	j += 1
    ###########################################################
    #### Onderrand ####	
	z = 0
	x = 0 
	# bron linksonder
	HYMS.QV6(x,z,rl,p,q)
	#onderrand
	for x in range(1, h):
		HYMS.V3(x, z, rl, p) 
	#rechtsonder
	x = h
	HYMS.PV7(x,z,rl,p)

    ###########################################################
    #### Ter hoogte van bronnen (oftwel rand sluisdeur) ####	
	for z in range(1, s+1):
		#bron
		x = 0
		HYMS.Q2(x,z,rl,p,q)
		#rechts van de bron
		for x in range(1, h):
			HYMS.VELD(x,z,rl,p)
		#uiterst rechts van bronnen
		x = h
		HYMS.P4(x,z,rl,p)
	
    ###########################################################
    #### Ter hoogte boven bronnen (oftwel boven rand sluisdeur) ####	
	for z in range(s+1, w):
		#linkerrand boven de bronnen
		x = 0
		HYMS.P2(x,z,rl,p)
		#rechts boven bronnen
		for x in range (1,h):
			HYMS.VELD(x,z,rl,p)
		#uiterst rechts boven bronnen
		x = h
		HYMS.P4(x,z,rl,p)

    ###########################################################
    #### Ter hoogte van bovenrand ####	
	z = w
	x = 0
	for x in range(1, h):	
		HYMS.P1(x,z,rl,p)
	x = h
	HYMS.PP8(x,z,rl,p)

	#Volume
	V, alfa = VOL1(z,s,uo,dl,q,p,V,alfa)
	Vd = V / ((s*dl)**2)

    # Check for convergence
	eps = (V - Vo) / (V / j)
	print(j, V, Vd)
	
	if eps <= epsn:
		break

# Output alfa !!!(IK denk rotatiesnelheid / versnelling?)
#for x in range(1, s):
#    print(alfa[x])

plt.plot(alfa)
plt.title('alfa')
plt.ylabel('Ratio')
plt.xlim([0,w])
plt.xlabel('z-dir')

plt.figure()
plt.imshow(p.transpose(), cmap='bwr', origin='lower',vmin=-8,vmax=8)
plt.title('Element overview of potential flow field')
plt.xlabel('x-dir')
plt.ylabel('z-dir')
plt.xlim([0,h])
plt.ylim([0,w])
plt.colorbar(label='Ratio')