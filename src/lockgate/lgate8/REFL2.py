import math
import os

import numpy as np

def refl(fileName, maxsteps):
    """
    REFLECTIE TRANSLATIEGOLVEN IN EEN GESLOTEN VOORHAVEN
    Versie 1.00
    Waterloopkundig Laboratorium Delft
    A. Vrijburcht, 23 augustus 1993

    TOELICHTING
    A = open linker eind met opgelegd debiet QM als functie van tijd
    L = gesloten rechter eind
    AB, CD, EF, GH, IJ, KL zijn de 6 secties
    BC, DE, FG, HI, JK  zijn de 5 knopen
    LAB, enz. zijn lengte secties
    BAB, enz. zijn breedte secties
    waterdiepte HV-ZK is constant
    berekening waterstanden als functie van tijd met invloed reflecties 

    uitvoer zijn waterstanden in de knopen
    """

    from INTER import inter

    #     HV   = waterstand voorhaven
    #     ZK   = bodem voorhaven
    #     LAB  = lengte sectie AB
    #     BAB  = breedte sectie AB
    #     DT   = tijdstap
    #     TINIT= initiele tijd
    #     TEND = eindtijd berekening
    #     NTM  = aantal opgegeven debietpunten
    #     TM   = tijdstip
    #     QM   = debiet

    # Open files
    outputName = fileName
    if os.path.exists(outputName + ".out"):
        os.remove(outputName+".out")

    file = open(fileName + ".in", "r")
    lines = [n for n in file.readlines() if not n.startswith('**')]
    lines = [x.replace('\n', '') for x in lines]

    # Read input
    hv, zk = list(map(float, lines[0].split()))
    lines.remove(lines[0])
    lab, lcd, lef, lgh, lij, lkl = list(map(float, lines[0].split()))
    lines.remove(lines[0])
    bab, bcd, bef, bgh, bij, bkl = list(map(float, lines[0].split()))
    lines.remove(lines[0])
    dt, tinit, tend = list(map(float, lines[0].split()))
    lines.remove(lines[0])
    ntm = int(lines[0])
    lines.remove(lines[0])
    file.close()

    # Time moment (tm) and debit (qm)
    tm = np.zeros(ntm)
    qm = np.zeros(ntm)
    for m in range(0, ntm):
        tm[m], qm[m] = list(map(float, lines[0].split()))
        lines.remove(lines[0])
    file.close()
    # Initialization
    g = 9.81
    j = 0
    k = 0
    t = tinit

    qat, qbt, qct, qdt, qet, qft, qgt, qht, qit, qjt, qkt, qlt, qbc, qde, qfg, qhi, qjk = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    
    # Length array for waves
    ck   = math.sqrt(g*(hv-zk)) # Phase/group speed wave
    nabr = lab/ck/dt
    ncdr = lcd/ck/dt
    nefr = lef/ck/dt
    nghr = lgh/ck/dt
    nijr = lij/ck/dt
    nklr = lkl/ck/dt
    nab  = int(round(nabr))
    ncd  = int(round(ncdr))
    nef  = int(round(nefr))
    ngh  = int(round(nghr))
    nij  = int(round(nijr))
    nkl  = int(round(nklr))
    nv   = np.max([nab, ncd, nef, ngh, nij, nkl])

    nv = int(1.2*nv)
    if (nv >= maxsteps):
      print('Increase timestep of amount of steps because now %d needed' %(maxsteps))
      exit()

    qv = inter(ntm,tm,qm,t)
    na0 = qv/bab/ck
    hlm = hv
    # Arrays
    qa = np.zeros(nv)
    qb = np.zeros(nv)
    qc = np.zeros(nv)
    qd = np.zeros(nv)
    qe = np.zeros(nv)
    qf = np.zeros(nv)
    qg = np.zeros(nv)
    qh = np.zeros(nv)
    qi = np.zeros(nv)
    qj = np.zeros(nv)
    qk = np.zeros(nv)
    ql = np.zeros(nv)

    nv = nv -1

    # Calculation translation waves
    fileout = open(outputName+".out", 'a')
    format_99006 = '   {:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}\n'
    format_990061 = '{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}\n'
    print(format_99006.format('Time', 'NA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL'))
    fileout.write(format_99006.format('Time', 'NA', 'HA', 'HB', 'HC', 'HD', 'HE', 'HF', 'HG', 'HH', 'HI', 'HJ', 'HK', 'HL'))

    while True:
        j += 1
        k += 1
        t += dt
        qv = inter(ntm,tm,qm,t)
        
        # Calculation until array reaches its maximum
        if j <= nv:
            # Generated debits
            qa[j] = qv
            qb[j] = qbc - qbt
            qc[j] = qbc - qct
            qd[j] = qde - qdt
            qe[j] = qde - qet
            qf[j] = qfg - qft
            qg[j] = qfg - qgt
            qh[j] = qhi - qht
            qi[j] = qhi - qit
            qj[j] = qjk - qjt
            qk[j] = qjk - qkt
            ql[j] = -qlt

            # Incoming debits
            if j >= nab:
                qat = qb[j - nab]
                qbt = qa[j - nab]
            if j >= ncd:
                qct = qd[j - ncd]
                qdt = qc[j - ncd]
            if j >= nef:
                qet = qf[j - nef]
                qft = qe[j - nef]
            if j >= ngh:
                qgt = qh[j - ngh]
                qht = qg[j - ngh]
            if j >= nij:
                qit = qj[j - nij]
                qjt = qi[j - nij]
            if j >= nkl:
                qkt = ql[j - nkl]
                qlt = qk[j - nkl]

            # Continuous debits
            qbc = 2 * (qbt / bab + qct / bcd) / (1 / bab + 1 / bcd)
            qde = 2 * (qdt / bcd + qet / bef) / (1 / bcd + 1 / bef)
            qfg = 2 * (qft / bef + qgt / bgh) / (1 / bef + 1 / bgh)
            qhi = 2 * (qht / bgh + qit / bij) / (1 / bgh + 1 / bij)
            qjk = 2 * (qjt / bij + qkt / bkl) / (1 / bij + 1 / bkl)

            # Generated wave heights
            na = qa[j] / (bab * ck)
            nb = -qb[j] / (bab * ck)
            nc = qc[j] / (bcd * ck)
            nd = -qd[j] / (bcd * ck)
            ne = qe[j] / (bef * ck)
            nf = -qf[j] / (bef * ck)
            ng = qg[j] / (bgh * ck)
            nh = -qh[j] / (bgh * ck)
            ni = qi[j] / (bij * ck)
            nj = -qj[j] / (bij * ck)
            nk = qk[j] / (bkl * ck)
            nl = -ql[j] / (bkl * ck)

        # Calculation after array has reached its maximum
        else:
            # Generated debits
            for l in range(1, nv):
                qa[l] = qa[l + 1]
                qb[l] = qb[l + 1]
                qc[l] = qc[l + 1]
                qd[l] = qd[l + 1]
                qe[l] = qe[l + 1]
                qf[l] = qf[l + 1]
                qg[l] = qg[l + 1]
                qh[l] = qh[l + 1]
                qi[l] = qi[l + 1]
                qj[l] = qj[l + 1]
                qk[l] = qk[l + 1]
                ql[l] = ql[l + 1]

            qa[nv] = qv
            qb[nv] = qbc - qbt
            qc[nv] = qbc - qct
            qd[nv] = qde - qdt
            qe[nv] = qde - qet
            qf[nv] = qfg - qft
            qg[nv] = qfg - qgt
            qh[nv] = qhi - qht
            qi[nv] = qhi - qit
            qj[nv] = qjk - qjt
            qk[nv] = qjk - qkt
            ql[nv] = -qlt

            # Incoming debits
            qat = qb[nv - nab]
            qbt = qa[nv - nab]
            qct = qd[nv - ncd]
            qdt = qc[nv - ncd]
            qet = qf[nv - nef]
            qft = qe[nv - nef]
            qgt = qh[nv - ngh]
            qht = qg[nv - ngh]
            qit = qj[nv - nij]
            qjt = qi[nv - nij]
            qkt = ql[nv - nkl]
            qlt = qk[nv - nkl]

            # Continuous debits
            qbc = 2 * (qbt / bab + qct / bcd) / (1 / bab + 1 / bcd)
            qde = 2 * (qdt / bcd + qet / bef) / (1 / bcd + 1 / bef)
            qfg = 2 * (qft / bef + qgt / bgh) / (1 / bef + 1 / bgh)
            qhi = 2 * (qht / bgh + qit / bij) / (1 / bgh + 1 / bij)
            qjk = 2 * (qjt / bij + qkt / bkl) / (1 / bij + 1 / bkl)

            # Generated wave heights
            na = qa[nv] / (bab * ck)
            nb = -qb[nv] / (bab * ck)
            nc = qc[nv] / (bcd * ck)
            nd = -qd[nv] / (bcd * ck)
            ne = qe[nv] / (bef * ck)
            nf = -qf[nv] / (bef * ck)
            ng = qg[nv] / (bgh * ck)
            nh = -qh[nv] / (bgh * ck)
            ni = qi[nv] / (bij * ck)
            nj = -qj[nv] / (bij * ck)
            nk = qk[nv] / (bkl * ck)
            nl = -ql[nv] / (bkl * ck)

        # Incoming wave heights 
        nat = -qat / (bab*ck)
        nbt =  qbt / (bab*ck)
        nct = -qct / (bcd*ck)
        ndt =  qdt / (bcd*ck)
        net = -qet / (bef*ck)
        nft =  qft / (bef*ck)
        ngt = -qgt / (bgh*ck)
        nht =  qht / (bgh*ck)
        nit = -qit / (bij*ck)
        njt =  qjt / (bij*ck)
        nkt = -qkt / (bkl*ck)
        nlt =  qlt / (bkl*ck)

        # Water heights (water height + generated wave height + incoming wave height)
        ha = hv + na + nat
        hb = hv + nb + nbt
        hc = hv + nc + nct
        hd = hv + nd + ndt
        he = hv + ne + net
        hf = hv + nf + nft
        hg = hv + ng + ngt
        hh = hv + nh + nht
        hi = hv + ni + nit
        hj = hv + nj + njt
        hk = hv + nk + nkt
        hl = hv + nl + nlt

        if hlm <= hl:
            hlm = hl

        # Check for end conditions
        if t > tend:
            break

        if k < 10:
            continue
        else:
            k = 0
            print(format_990061.format(t, na, ha, hb, hc, hd, he, hf, hg, hh, hi, hj, hk, hl))
            fileout.write(format_990061.format(t, na, ha, hb, hc, hd, he, hf, hg, hh, hi, hj, hk, hl))
    alfa = (hlm-hv)/na0
    print(alfa)
    fileout.close()


if __name__ == "__main__":
    maxsteps = 500 # Number of steps going over a period of wave between two sections
    filename = r'.\test_data\lockgate8\R21'
    refl(filename, maxsteps)
