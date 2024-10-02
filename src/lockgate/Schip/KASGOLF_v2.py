# PROGRAM KASGOLF

# Doordringen van golf van langsvarend schip in de deurkas
# Versie 1.00
# Waterloopkundig Laboratorium Delft
# A. Vrijburcht, 7 september 1993

# =====DECLARATIES========================================

import numpy as np
import os
from INTER import inter
import math
import matplotlib.pyplot as plt

Inv_naam = 'Test_invoer.IN'

T1 = np.zeros(21) #Tijdstabel [s]
N1 = np.zeros(21) #golfhoogte kolkzijde ter plaatse van spleet A [m]
T2 = np.zeros(21) #Tijdtabel 2 (?) [s]
N2 = np.zeros(21) #golfhoogte kolkzijde ter plaatse van spleet ? [m]

NV=NW=0

QA = np.zeros(1001) #?
QB = np.zeros(1001) #?
G = 9.81 #Gravitatieversnelling [m/s^2]

# =====INVOER=====================================================

#HKI =  #initiele waterstand [mNAP]
#ZK =  #niveau kolk- en deurkasbodem [mNAP]
#LKK =  #engte deurkas kolkzijde [m]
#LKAS =  #lengte deurkas kaszijde [m]
#BKAS =  #breedte deurkas kaszijde [m]
#BA =  #breedte verticale spleet A [m]
#BB =  #breedte verticale spleet B [m]
#AO = # Oppervlakte deuropening incl. onderzijde deur [m^2]
#MU =  #afvoercoeff. verticale spleten A en B [-]
#DT =  #tijdstap [s]
#TINIT =  #start tijd [s]
#TEND =  #eind tijd [s]
#M0 =  #keuze golf met translatiesnelheid (=0) of vaarsnelheid (=1)
#VS =  #vaarsnelheid [m/s]
#NT1 =  #aantal op te geven punten tabel (integer!)

#Uitlezen invoer bestand
Dict_inv = {}

with open(os.path.join(os.getcwd(),Inv_naam), 'r') as file:
    for line in file:
        if '=' in line:
            key, value = line.split('=')
            key = key.strip()  
            value = value.strip()  
            if ',' in value:
                value = list(map(float, value.split(',')))
            else:
                try:
                    value = float(value)
                except ValueError:
                    value = int(value)
            Dict_inv[key] = value

Dict_inv['NT1'] = int(Dict_inv['NT1'])

# Lengte array voor golven
J = 0
K = 0
T = Dict_inv['TINIT']
HKAS = Dict_inv['HKI']
QAT = 0         #Debiet in punt A
QBT = 0         #Debiet in punt B
NA = 0          #Gegenereerde golfhoogte punt A
NB = 0          #Gegenereerde golfhoogte punt B
NAT = 0         #Golfhoogte in punt A
NBT = 0         #Golfhoogte in punt B
Tot_A = Dict_inv['AO']#+(Dict_inv['BA']+Dict_inv['BB'])*(Dict_inv['HKI']-Dict_inv['ZK'])


# Length of array for waves
CK = np.sqrt(G * (Dict_inv['HKI'] - Dict_inv['ZK'])) #snelheid golf
if Dict_inv['M0'] == 0:
    DTG = Dict_inv['LKK'] / CK                       #looptijd golf in kas bij golfsnelheid (M0 == 0)
else:
    DTG = Dict_inv['LKK'] / Dict_inv['VS']           #looptijd golf in kas bij vaarsnelheid (M0 == 1)

NKASR = Dict_inv['LKAS'] / CK / Dict_inv['DT'] #Aantal tijdstappen voor golf langs gehele kas
NKAS = int(round(NKASR))
NK = int(round(NKAS / 10))
N = int(1.1 * NKAS)

# =====BEREKENING TRANSLATIEGOLVEN IN DEURKAS=====================
L_T = []
L_HKAS = []
L_HV = []
L_HA = []
L_H5 = []
L_HB = []
L_HW = []
L_HGEM = []
L_GGEM = []
L_NV = []
L_dH = []
L_H1 = []
L_H2 = []
L_H3 = []
L_H4 = []
L_H6 = []
L_H7 = []
L_H8 = []
L_H9 = []
L_NBT = []
L_NAT = []

'''
#Loop in de tijd voordat de golf bij de kas is
while inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T) == HKAS and inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T-DTG) == HKAS:
    L_T.append(T)
    L_HKAS.append(HKAS)
    L_HV.append(HKAS)
    L_HA.append(HKAS)
    L_H5.append(HKAS)
    L_HB.append(HKAS)
    L_HW.append(HKAS)
    L_HGEM.append(HKAS)
    L_GGEM.append(HKAS)
    L_NV.append(NV)
    L_dH.append(0)
   
    J += 1
    T = round(T+Dict_inv['DT'],2)
    
Jst_golf = J     
'''
#Deze while loop stopt als Teind is bereikt en begint pas als T de tijdstap van begin golf heeft bereikt
while True:

    #Berekenen waterstanden Spleet 1 (NV) en spleet 2 (NW)
    NV = inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T)
    NW = inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T-DTG)

    #Lengte van de golf array (vanaf het moment dat de golf langstrekt)
    if J <= (N):
        P = 0

        #Inkomend debiet via het kaskanaal
        if J >= (NKAS):
            QAT = QB[J-NKAS]
            QBT = QA[J-NKAS]
            
        NAT = -QAT / (Dict_inv['BKAS']*CK) #Inkomende golfhoogte locatie A
        NBT = QBT / (Dict_inv['BKAS']*CK) #Inkomende golfhoogte locatie B

        #Itereren tot juist benadering golfhoogte
        while True:
            P = P+1
            NAO = NA
            NBO = NB
            QA[J] = (Dict_inv['MU'] * Dict_inv['BA'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                     math.copysign(1, NV - NA - NAT) * np.sqrt(2 * G * abs(NV - NA - NAT)) - QAT) 
            QB[J] = (Dict_inv['MU'] * Dict_inv['BB'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                     math.copysign(1, (NB + NBT - NW)) * np.sqrt(2 * G * abs(NB + NBT - NW)) - QBT)
            NAN = QA[J] / (Dict_inv['BKAS']*CK)
            NBN = -QB[J] / (Dict_inv['BKAS']*CK)
            NA = (1.8 * NAO + 0.2 * NAN) / 2
            NB = (1.8 * NBO + 0.2 * NBN) / 2

            if P >= 1000 or (abs(NAO-NA) <= 0.001 and abs(NBO-NB) <= 0.001):
                break

        HV = Dict_inv['HKI'] + NV #waterstand in de kolk
        HA = HKAS + NA + NAT #waterstand bij spleet A. Waterstand KAS

        if J >= 9 * NK:
            H1 = HKAS + (QA[J - NK - 1] - QB[J - 9 * NK - 1]) / (Dict_inv['BKAS'] * CK)
            H9 = HKAS + (QA[J - 9 * NK - 1] - QB[J - NK - 1]) / (Dict_inv['BKAS'] * CK)
        elif J >= NK:
            H1 = HKAS + QA[J - NK - 1] / (Dict_inv['BKAS'] * CK)
            H9 = HKAS - QB[J - NK - 1] / (Dict_inv['BKAS'] * CK)
        else:
            H1 = HKAS
            H9 = HKAS

        if J >= 8 * NK:
            H2 = HKAS + (QA[J - 2 * NK - 1] - QB[J - 8 * NK - 1]) / (Dict_inv['BKAS'] * CK)
            H8 = HKAS + (QA[J - 8 * NK - 1] - QB[J - 2 * NK - 1]) / (Dict_inv['BKAS'] * CK)
        elif J >= 2 * NK:
            H2 = HKAS + QA[J - 2 * NK - 1] / (Dict_inv['BKAS'] * CK)
            H8 = HKAS - QB[J - 2 * NK - 1] / (Dict_inv['BKAS'] * CK)
        else:
            H2 = HKAS
            H8 = HKAS

        if J >= 7 * NK:
            H3 = HKAS + (QA[J - 3 * NK - 1] - QB[J - 7 * NK - 1]) / (Dict_inv['BKAS'] * CK)
            H7 = HKAS + (QA[J - 7 * NK - 1] - QB[J - 3 * NK - 1]) / (Dict_inv['BKAS'] * CK)
        elif J >= 3 * NK:
            H3 = HKAS + QA[J - 3 * NK - 1] / (Dict_inv['BKAS'] * CK)
            H7 = HKAS - QB[J - 3 * NK - 1] / (Dict_inv['BKAS'] * CK)
        else:
            H3 = HKAS
            H7 = HKAS

        if J >= 6 * NK:
            H4 = HKAS + (QA[J - 4 * NK - 1] - QB[J - 6 * NK - 1]) / (Dict_inv['BKAS'] * CK)
            H6 = HKAS + (QA[J - 6 * NK - 1] - QB[J - 4 * NK - 1]) / (Dict_inv['BKAS'] * CK)
        elif J >= 4 * NK:
            H4 = HKAS + QA[J - 4 * NK - 1] / (Dict_inv['BKAS'] * CK)
            H6 = HKAS - QB[J - 4 * NK - 1] / (Dict_inv['BKAS'] * CK)
        else:
            H4 = HKAS
            H6 = HKAS

        if J >= 5*NK:
            H5 = HKAS + (QA[J - 5 * NK - 1] - QB[J - 5 * NK - 1]) / (Dict_inv['BKAS'] * CK)
        else:
            H5 = HKAS

        HB = HKAS + NB + NBT
        HW = Dict_inv['HKI'] + NW

        HGEM = (0.5*HA+H1 + H2 + H3 + H4 + H5 + H6 + H7 + H8 + H9+0.5*HB) / 10
        GGEM = (0.5*NV+H1 + H2 + H3 + H4 + H5 + H6 + H7 + H8 + H9+0.5*NW) / 10

        QAA = QA[J] + QAT
        QBB = QB[J] + QBT        


    #De lengte array van de golf is al voorbij
    else:


        print('T=',T,QBT, 'NBT=',NBT, 'NB=',NB, QB[len(QB)-1])
        if T == 12.92:
            break
        QAT = QB[N-NKAS] #N-NKAS is 1 hele golflengte geleden (door ck komt debiet van B ten tijde van (N-NKAS) nu aan bij A)
        QBT = QA[N-NKAS]
        #Inkomende golfhoogte door translatiegolf
        NAT = -QAT / (Dict_inv['BKAS']*CK)
        NBT = QBT / (Dict_inv['BKAS']*CK)

        #if QBT > 0:
        #    break

        for L in range(0,N):
            #Alles debieten schuiven een stapje verder, op locatie N komt het nieuwe debiet
            QA[L] = QA[L+1]
            QB[L] = QB[L+1]
        
        P = 0
        #Itereren tot juist benadering golfhoogte
        while True:
            P = P+1
            NAO = NA
            NBO = NB

            #
            QA[N] = (Dict_inv['MU'] * Dict_inv['BA'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                     math.copysign(1, NV - NA - NAT) * np.sqrt(2 * G * abs(NV - NA - NAT)) - QAT) 
            QB[N] = (-Dict_inv['MU'] * Dict_inv['BB'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                     math.copysign(1, (NW-NB-NBT)) * np.sqrt(2 * G * abs(NW-NB-NBT)) - QBT)
            NAN = QA[N] / (Dict_inv['BKAS']*CK)
            NBN = -QB[N] / (Dict_inv['BKAS']*CK)
            NA = (1.8 * NAO + 0.2 * NAN) / 2
            NB = (1.8 * NBO + 0.2 * NBN) / 2

            if P >= 1000 or (abs(NAO-NA) <= 0.001 and abs(NBO-NB) <= 0.001):
                break

        HV = Dict_inv['HKI'] + NV #waterstand in de kolk
        HA = HKAS + NA + NAT #waterstand bij spleet A

        if J >= 9 * NK:
            H1 = HKAS + (QA[N - NK] - QB[N - 9 * NK]) / (Dict_inv['BKAS'] * CK)
            H9 = HKAS + (QA[N - 9 * NK] - QB[N - NK]) / (Dict_inv['BKAS'] * CK)
        elif J >= NK:
            H1 = HKAS + QA[N - NK] / (Dict_inv['BKAS'] * CK)
            H9 = HKAS - QB[N - NK] / (Dict_inv['BKAS'] * CK)
        else:
            H1 = HKAS
            H9 = HKAS

        if J >= 8 * NK:
            H2 = HKAS + (QA[N - 2 * NK] - QB[N - 8 * NK]) / (Dict_inv['BKAS'] * CK)
            H8 = HKAS + (QA[N - 8 * NK] - QB[N - 2 * NK]) / (Dict_inv['BKAS'] * CK)
        elif J >= 2 * NK:
            H2 = HKAS + QA[N - 2 * NK] / (Dict_inv['BKAS'] * CK)
            H8 = HKAS - QB[N - 2 * NK] / (Dict_inv['BKAS'] * CK)
        else:
            H2 = HKAS
            H8 = HKAS

        if J >= 7 * NK:
            H3 = HKAS + (QA[N - 3 * NK ] - QB[N - 7 * NK]) / (Dict_inv['BKAS'] * CK)
            H7 = HKAS + (QA[N - 7 * NK ] - QB[N - 3 * NK]) / (Dict_inv['BKAS'] * CK)
        elif J >= 3 * NK:
            H3 = HKAS + QA[N - 3 * NK ] / (Dict_inv['BKAS'] * CK)
            H7 = HKAS - QB[N - 3 * NK ] / (Dict_inv['BKAS'] * CK)
        else:
            H3 = HKAS
            H7 = HKAS

        if J >= 6 * NK:
            H4 = HKAS + (QA[N - 4 * NK] - QB[N - 6 * NK]) / (Dict_inv['BKAS'] * CK)
            H6 = HKAS + (QA[N - 6 * NK ] - QB[N - 4 * NK]) / (Dict_inv['BKAS'] * CK)
        elif J >= 4 * NK:
            H4 = HKAS + QA[N - 4 * NK] / (Dict_inv['BKAS'] * CK)
            H6 = HKAS - QB[N - 4 * NK] / (Dict_inv['BKAS'] * CK)
        else:
            H4 = HKAS
            H6 = HKAS

        if J >= 5*NK:
            H5 = HKAS + (QA[N - 5 * NK] - QB[N - 5 * NK]) / (Dict_inv['BKAS'] * CK)
        else:
            H5 = HKAS

        HB = HKAS + NB + NBT
        HW = Dict_inv['HKI'] + NW

        HGEM = HKAS+(0.5*HA+H1 + H2 + H3 + H4 + H5 + H6 + H7 + H8 + H9+0.5*HB) / 10

        QAA = QA[N] + QAT
        QBB = QB[N] + QBT        

    # Constants
    DTT = DTG / 10

    # Calling the inter function for water levels at the lock side
    G1 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 1 * DTT)
    G2 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 2 * DTT)
    G3 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 3 * DTT)
    G4 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 4 * DTT)
    G5 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 5 * DTT)
    G6 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 6 * DTT)
    G7 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 7 * DTT)
    G8 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 8 * DTT)
    G9 = inter(Dict_inv['NT1'], Dict_inv['T1'], Dict_inv['N1'], T - 9 * DTT)

    # Calculating the average water level in kolk
    GGEM = Dict_inv['HKI'] + (0.5 * NV + G1 + G2 + G3 + G4 + G5 + G6 + G7 + G8 + G9 + 0.5 * NW) / 10 

    # Water level at the kas side of the door
    HKAS = HKAS - (Dict_inv['MU'] * Tot_A * np.sign(HGEM - GGEM) *
                    np.sqrt(2 * G * abs(HGEM - GGEM)) / (Dict_inv['BKAS'] * Dict_inv['LKAS'])) * Dict_inv['DT']

    dH = GGEM-HGEM

    #Toeschrijven uitvoer
    L_NAT.append(NAT)
    L_NBT.append(NBT)
    L_T.append(T)
    L_HKAS.append(HKAS)
    L_HV.append(HV)
    L_HA.append(HA)
    L_H5.append(H5)
    L_HB.append(HB)
    L_HW.append(HW)
    L_HGEM.append(HGEM)
    L_GGEM.append(GGEM)
    L_NV.append(NV)
    L_dH.append(dH)
    L_H1.append(H1)
    L_H2.append(H2)
    L_H3.append(H3)
    L_H4.append(H4)
    L_H6.append(H6)
    L_H7.append(H7)
    L_H8.append(H8)
    L_H9.append(H9)


    # Calculation up to end time
    if T >= Dict_inv['TEND']:
        break

    J += 1
    T = round(T+Dict_inv['DT'],2)

print(T)
print('NAT',NAT,'NBT',NBT,'NV',NV,'NW',NW,'NA',NA,'NB',NB)
plt.plot(L_T,L_HA,label='HA kas')
plt.plot(L_T,L_HB,label='HB kas')
plt.plot(L_T,L_HV,label='Spleet A kolk')
plt.plot(L_T,L_HW,label='Spleet B kolk')
plt.plot(L_T,L_H5,label='H5')
plt.legend()
#plt.xlim([-1,6])
plt.figure()    
plt.plot(L_T,L_HGEM,label='HGEM')
plt.plot(L_T,L_GGEM,label='GGEM')
plt.plot(L_T,L_HKAS,label='HKAS')
plt.plot(L_T,L_dH,label='Verval')
plt.plot(L_T,L_HW,label='WL Kolk spleet B')
plt.plot(L_T,L_HV,label='WL Kolk spleet A')
plt.legend()
#plt.xlim([-1,6])

plt.figure()
plt.plot(L_T,L_HV,label='Wl kolk tpv A')
plt.plot(L_T,L_H5,label='H midden deurkas')
plt.plot(L_T,L_HW,label='Wl kolk tpv B')
plt.ylim([-0.4,1.2])
plt.grid()
plt.xticks([-6,0,6,12,18,24,30])

plt.figure()
plt.plot(L_T,L_dH)
plt.ylim([-0.8,0.8])
plt.grid()
plt.xticks([-6,0,6,12,18,24,30])


#Uitvoer
# T = tijd [s]
# HV = waterstand kolkzijde voor spleet A [mNAP]
# HA = waterstand kaszijde voor spleet A [mNAP]
# H5 = waterstand kaszijde midden kas [mNAP]
# HB = waterstand kaszijde voor spleet B [mNAP]
# HW = waterstand kolkzijde voor spleet B [mNAP]
# HGEM = gemiddelde waterstand in kas ter plaatse van de deur [mNAP]
# GGEM = gemiddelde waterstand in kolk ter plaatse van de deur [mNAP]
# GGEM - HGEM = gemiddeld verval over de deur [m]


# =====EINDE=======================================================


#OPmerking 27-09-24
#Het lijkt mij vreemd dat spleet B meegroeit met H5. Met name het moment dat de golf spleet B bereiekt is gek. Er lijkt iets fout in NB in de eerste loop (ook de tweede)