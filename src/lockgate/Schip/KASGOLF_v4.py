# PROGRAM KASGOLF

# Doordringen van golf van langsvarend schip in de deurkas
# Versie 1.00
# Waterloopkundig Laboratorium Delft
# A. Vrijburcht, 7 september 1993

# =====DECLARATIES========================================

import numpy as np
import os
import math
import matplotlib.pyplot as plt
import pandas as pd

Inv_naam = 'Inv_Sam_nz_OG.IN'

T1 = np.zeros(21) #Tijdstabel [s]
N1 = np.zeros(21) #golfhoogte kolkzijde ter plaatse van spleet A [m]
T2 = np.zeros(21) #Tijdtabel 2 (?) [s]
N2 = np.zeros(21) #golfhoogte kolkzijde ter plaatse van spleet ? [m]

NV=NW=0

QA = []#np.zeros(1001) #?
QB = []#np.zeros(1001) #?
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
QA_dum = 0      #Iteratie debiet door spleet A
QB_dum = 0      #Iteratie debiet door spleet B
Tot_A = Dict_inv['AO']#Oppervlak spleet onder deur (spleet 3)


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
    #NV = inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T)
    #NW = inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T-DTG)
    NV = np.interp(T,Dict_inv['T1'],Dict_inv['N1'])
    NW = np.interp(T-DTG,Dict_inv['T1'],Dict_inv['N1'])
    
    #Lengte van de golf array (vanaf het moment dat de golf langstrekt)
    if J <= (N):
        #Inkomend debiet via het kaskanaal
        if J >= (NKAS):
            QAT = QB[J-NKAS]
            QBT = QA[J-NKAS]
            
        NAT = -QAT / (Dict_inv['BKAS']*CK) #Inkomende golfhoogte locatie A
        NBT = QBT / (Dict_inv['BKAS']*CK) #Inkomende golfhoogte locatie B

    #De lengte array van de golf is al voorbij
    else:   
        #print('T=',T,QBT, 'NBT=',NBT, 'NB=',NB, QB[len(QB)-1],QB_dum)
        #if T == 12.90:
        #    break
        QAT = QB[len(QB)-NKAS] #N-NKAS is 1 hele golflengte geleden (door ck komt debiet van B ten tijde van (N-NKAS) nu aan bij A)
        QBT = QA[len(QA)-NKAS]

        #Inkomende golfhoogte door translatiegolf
        NAT = -QAT / (Dict_inv['BKAS']*CK)
        NBT = QBT / (Dict_inv['BKAS']*CK)

    
    max_iterations = 10000
    tolerance = 0.001

    NAO = 0
    NBO = 0
    
    #if T == 6.44:
    #    break
    #Itereren tot juist benadering golfhoogte 
    for P in range(0,max_iterations+1):
        QAO = QA_dum
        QBO = QB_dum
        NAO = NA
        NBO = NB
        QB_update = (-Dict_inv['MU'] * Dict_inv['BB'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                    math.copysign(1, NW - NB - NBT) * np.sqrt(2 * G * abs(NW - NB - NBT)) - QBT)
        QA_update = (Dict_inv['MU'] * Dict_inv['BA'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                    math.copysign(1, NV - NA - NAT) * np.sqrt(2 * G * abs(NV - NA - NAT)) - QAT) 
       
        QA_dum = QA_update#0.1*QA_update + 0.9*QAO
        QB_dum = QB_update#0.1*QB_update + 0.9*QBO

        NAN = QA_dum / (Dict_inv['BKAS']*CK)
        NA = 0.9 * NAO + 0.1 * NAN
        NBN = -QB_dum / (Dict_inv['BKAS']*CK)
        NB = 0.9 * NBO + 0.1 * NBN
        
        #if  abs(NB - NBO) <= tolerance and abs(QB_dum - QBO) <= tolerance and abs(NA - NAO) <= tolerance and abs(QA_dum - QAO) <= tolerance:
        if  (abs(NB - NBO) <= tolerance and abs(NA - NAO) <= tolerance):
            #print('Doet het nu')
            break

    else:
        print(f'T:{T}; No value found')
    
    #if T == 4:
    #    break

    QA.append(QA_dum)
    QB.append(QB_dum) 

    HV = Dict_inv['HKI'] + NV #waterstand in de kolk
    HA = HKAS + NA + NAT #waterstand bij spleet A. Waterstand KAS

    if J >= 9 * NK:
        H1 = HKAS + (QA[J - NK] - QB[J - 9 * NK]) / (Dict_inv['BKAS'] * CK)
        H9 = HKAS + (QA[J - 9 * NK] - QB[J - NK]) / (Dict_inv['BKAS'] * CK)
    elif J >= NK:
        H1 = HKAS + QA[J - NK] / (Dict_inv['BKAS'] * CK)
        H9 = HKAS - QB[J - NK] / (Dict_inv['BKAS'] * CK)
    else:
        H1 = HKAS
        H9 = HKAS

    if J >= 8 * NK:
        H2 = HKAS + (QA[J - 2 * NK] - QB[J - 8 * NK]) / (Dict_inv['BKAS'] * CK)
        H8 = HKAS + (QA[J - 8 * NK] - QB[J - 2 * NK]) / (Dict_inv['BKAS'] * CK)
    elif J >= 2 * NK:
        H2 = HKAS + QA[J - 2 * NK] / (Dict_inv['BKAS'] * CK)
        H8 = HKAS - QB[J - 2 * NK] / (Dict_inv['BKAS'] * CK)
    else:
        H2 = HKAS
        H8 = HKAS

    if J >= 7 * NK:
        H3 = HKAS + (QA[J - 3 * NK] - QB[J - 7 * NK]) / (Dict_inv['BKAS'] * CK)
        H7 = HKAS + (QA[J - 7 * NK] - QB[J - 3 * NK]) / (Dict_inv['BKAS'] * CK)
    elif J >= 3 * NK:
        H3 = HKAS + QA[J - 3 * NK] / (Dict_inv['BKAS'] * CK)
        H7 = HKAS - QB[J - 3 * NK] / (Dict_inv['BKAS'] * CK)
    else:
        H3 = HKAS
        H7 = HKAS

    if J >= 6 * NK:
        H4 = HKAS + (QA[J - 4 * NK] - QB[J - 6 * NK]) / (Dict_inv['BKAS'] * CK)
        H6 = HKAS + (QA[J - 6 * NK] - QB[J - 4 * NK]) / (Dict_inv['BKAS'] * CK)
    elif J >= 4 * NK:
        H4 = HKAS + QA[J - 4 * NK] / (Dict_inv['BKAS'] * CK)
        H6 = HKAS - QB[J - 4 * NK] / (Dict_inv['BKAS'] * CK)
    else:
        H4 = HKAS
        H6 = HKAS

    if J >= 5*NK:
        H5 = HKAS + (QA[J - 5 * NK] - QB[J - 5 * NK]) / (Dict_inv['BKAS'] * CK)
    else:
        H5 = HKAS

    HB = HKAS + NB + NBT
    HW = Dict_inv['HKI'] + NW

    HGEM = (0.5*HA+H1 + H2 + H3 + H4 + H5 + H6 + H7 + H8 + H9+0.5*HB) / 10

    QAA = QA[J] + QAT
    QBB = QB[J] + QBT     
    
    # Constants
    DTT = DTG / 10

    # Calling the inter function for water levels at the lock side
    G1 = np.interp(T - 1 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G2 = np.interp(T - 2 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G3 = np.interp(T - 3 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G4 = np.interp(T - 4 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G5 = np.interp(T - 5 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G6 = np.interp(T - 6 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G7 = np.interp(T - 7 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G8 = np.interp(T - 8 * DTT,Dict_inv['T1'], Dict_inv['N1'])
    G9 = np.interp(T - 9 * DTT,Dict_inv['T1'], Dict_inv['N1'])

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

    J += 1
    T = round(T+Dict_inv['DT'],2)

    # Calculation up to end time
    if T >= Dict_inv['TEND']:
        break

#%%
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
plt.legend()

plt.figure()
plt.plot(L_T,L_dH,label='Verval')
#plt.ylim([-0.4,0.2])
plt.xlim([0,40])
plt.grid()
plt.legend()
#plt.xticks([-6,0,6,12,18,24,30])
#%%
plt.figure()
plt.plot(L_T,L_HA,label='WL Kas zijde A')
plt.plot(L_T,L_HV,label='WL kolk zijde A')
plt.plot(L_T,L_HB,label='WL kaszijde B')
plt.plot(L_T,L_H2)
#plt.plot(L_T,L_H3)
#plt.plot(L_T,L_H4)
#plt.plot(L_T,L_H5)
#plt.plot(L_T,L_H6)
#plt.plot(L_T,L_H7)
#plt.plot(L_T,L_H8)
plt.plot(L_T,L_H9)
plt.legend()

#%% Read fortran uitvoer
column_names = ['T','HV','HA','H5','HB','HW','HGEM','GGEM','GGEM-HGEM']
dt_1 = pd.read_csv('Fort_uitv_1dt.out',names=column_names,index_col=False)
dt_10 = pd.read_csv('Fort_uitv_10dt.out',names=column_names,index_col=False)

plt.plot(dt_1["T"],dt_1["GGEM-HGEM"],label='Verval .FOR 1 dt')
#plt.plot(dt_10["T"],dt_10["GGEM-HGEM"],label='Verval .FOR 10 dt')
plt.plot(L_T,L_dH,label='Verval .py')
plt.legend()
#plt.ylim([-0.1,0.1])
plt.xlim([0,30])

#Readthedocs fig
#%% Read fortran uitvoer
plt.figure(figsize=(8, 4))
column_names = ['T','HV','HA','H5','HB','HW','HGEM','GGEM','GGEM-HGEM']
plt.plot(L_T,L_dH)
plt.legend()
plt.xlim([-6,30])
plt.grid()
plt.xticks([-6,0,6,12,18,24,30])
plt.ylabel('Verval [m]')
plt.xlabel('Tijd [s]')

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
# %%
