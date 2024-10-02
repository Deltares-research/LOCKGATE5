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

# Length of array for waves
CK = np.sqrt(G * (Dict_inv['HKI'] - Dict_inv['ZK'])) #snelheid golf
if Dict_inv['M0'] == 0:
    DTG = Dict_inv['LKK'] / CK                       #looptijd golf in kas bij golfsnelheid (M0 == 0)
else:
    DTG = Dict_inv['LKK'] / Dict_inv['VS']           #looptijd golf in kas bij vaarsnelheid (M0 == 1)

NKASR = Dict_inv['LKAS'] / CK / Dict_inv['DT']
NKAS = int(round(NKASR))
NK = int(round(NKAS / 10))
N = (Dict_inv['TEND'] - Dict_inv['TINIT'])/Dict_inv['DT']#int(1.1 * NKAS)

# =====BEREKENING TRANSLATIEGOLVEN IN DEURKAS=====================
T_list = []
HV_list = []
HA_list = []
H5_list = []
HB_list = []
HW_list = []
HGEM_list = []
GGEM_list = []
NV_list = []
HKAS_list= []

#Deze while loop stopt als Teind is bereikt
while True:
    J += 1
    K += 1
    T = round(T+Dict_inv['DT'],2)

    #Berekenen waterstanden Spleet 1 (NV) en spleet 2 (NW)
    NV = inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T)
    NW = inter(Dict_inv['NT1'],Dict_inv['T1'],Dict_inv['N1'],T-DTG)

    # Berekening uitvoeren tot duur van langstrekkende golf over is.
    if J <= N:

        P = 0
        # inkomende debieten
        if J >= NKAS:
            QAT = QB[J - NKAS]
            QBT = QA[J - NKAS]

        # inkomende golfhoogtes
        NAT = -QAT / (Dict_inv['BKAS'] * CK)
        NBT = QBT / (Dict_inv['BKAS'] * CK)

        while True:
            P += 1

            # oude gegenereerde golfhoogten
            NAO = NA
            NBO = NB

            # nieuwe gegenereerde debieten 
            QA[J] = (Dict_inv['MU'] * Dict_inv['BA'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                     math.copysign(1, NV - NA - NAT) * np.sqrt(2 * G * abs(NV - NA - NAT)) - QAT) 

            QB[J] = (Dict_inv['MU'] * Dict_inv['BB'] * (Dict_inv['HKI'] - Dict_inv['ZK']) *
                     math.copysign(1, (NB + NBT - NW)) * np.sqrt(2 * G * abs(NB + NBT - NW)) - QBT)

            # nieuwe gegenereerde golfhoogten 
            NAN = QA[J] / (Dict_inv['BKAS'] * CK)
            NBN = -QB[J] / (Dict_inv['BKAS'] * CK)

            # gecorrigeerde gegenereerde golfhoogten 
            NA = (1.8 * NAO + 0.2 * NAN) / 2
            NB = (1.8 * NBO + 0.2 * NBN) / 2

            # test voldoende nauwkeurige gegenereerde golfhoogten 
            if P > 1000 or abs(NAO - NA) < 0.001 and abs(NBO - NB) < 0.001:
                break

        # waterstanden deurkas
        HV = Dict_inv['HKI'] + NV #waterstand in de kolk
        HA = HKAS + NA + NAT #waterstand bij spleet A

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
        # gemiddelde waterniveau in deurkas
        HB = HKAS + NB + NBT
        HW = Dict_inv['HKI'] + NW

        HGEM = (0.5*HA+H1 + H2 + H3 + H4 + H5 + H6 + H7 + H8 + H9+0.5*HB) / 10
        GGEM = (0.5*NV+H1 + H2 + H3 + H4 + H5 + H6 + H7 + H8 + H9+0.5*NW) / 10

        QAA = QA[N] + QAT
        QBB = QB[N] + QBT

        #Waterstand deurkas zijde
        HKAS = HKAS - Dict_inv['MU'] * Dict_inv['AO'] * math.copysign(1, (HGEM - GGEM)) * \
        math.sqrt(2 * G * abs(HGEM - GGEM)) / Dict_inv['BKAS'] / Dict_inv['LKAS'] * Dict_inv['DT']
        # Outputs are calculated and saved here

        #Toeschrijven uitvoer
        HKAS_list.append(HKAS)
        T_list.append(T)
        HV_list.append(HV)
        HA_list.append(HV)
        H5_list.append(H5)
        HB_list.append(HB)
        HW_list.append(HW)
        HGEM_list.append(HGEM)
        GGEM_list.append(GGEM)
        NV_list.append(NV)
    # Calculation up to end time
    if T >= Dict_inv['TEND']:
        break

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