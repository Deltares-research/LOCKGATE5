import math
import os

def gate7(fileName):
  #     Waterstanden en krachten op deuren nabij de deurkas veroorzaakt
  #        door sluiten of openen van enkele draai- en puntdeuren
  #     Waterloopkundig Laboratorium Delft
  #     Versie 1.00 
  #     A. Vrijburcht, 12 oktober 1992
  
  # Open files
  outputName = fileName
  if os.path.exists(outputName + ".out"):
      os.remove(outputName+".out")

  file = open(fileName + ".in", "r")
  lines = [n for n in file.readlines() if not n.startswith('**')]
  lines = [x.replace('\n', '') for x in lines]
  #   ÄÄÄÄÄÄÄÄÄÄÄÄÄÄ¿   Ú<         bd                  >ÚÄÄÄÄÄÄÄÄÄÄÄ
  #                 ³bb ÃÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄ.³
  #          ba     ³   À            bc                 ³
  #                 ÀÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÄÙ
  #                  <              la                  >
  #.....1e regel: geometrie kolk k
  #     zk  = bodemniveau kolk k [mNAP]
  #     bk  = breedte kolk k [m]
  #.....2e regel: geometrie deur d
  #     zd  = niveau onderkant deur d [mNAP]
  #     bd  = breedte deur d [m]
  #     bb  = afstand deurtip tot kaswand (geopende stand) [m]
  #     bc  = afstand deur tot kaswand (geopende stand) [m]
  #     Ao  = totaal oppervlak deuropeningen [m2]
  #.....3e regel: geomtrie deurkas
  #     la  = lengte kas [m]
  #     ba  = diepte kas [m]
  #.....4e regel: coefficienten
  #     cs   = contractiecoeff. verticale spleet bij sluiten deur [-]
  #     mus  = afvoercoeff. openingen deur bij sluiten deur [-]
  #     co   = contractiecoeff. verticale spleet bij openen deur [-]
  #     muo  = afvoercoeff. openingen deur bij openen deur [-]
  #.....5e regel: beginvoorwaarde
  #     hk  = beginwaterstand kolk k [mNAP]
  #.....6e regel: div.
  #     rho = dichtheid water [kg/m3]
  #     dt  = rekentijdstap [s]
  #.....7e regel: 
  #     wd  = deursnelheid positief = sluiten [rad/s]
  #     wd  = deursnelheid negatief = openen [rad/s]

  zk, bk = list(map(float, lines[0].split()))
  lines.remove(lines[0])
  zd, bd, bb, bc, Ao = list(map(float, lines[0].split()))
  lines.remove(lines[0])
  la, ba = list(map(float, lines[0].split()))
  lines.remove(lines[0])
  cs, mus, co, muo = list(map(float, lines[0].split()))
  lines.remove(lines[0])
  hk = float(lines[0])
  lines.remove(lines[0])
  rho, dt = list(map(float, lines[0].split()))
  lines.remove(lines[0])
  wd = float(lines[0])
  lines.remove(lines[0])
  file.close()

  # Physical constants
  g = 9.81

  # Output file
  fileout = open(outputName+".out", 'a')
  format_99006 = '   {:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}{:10}\n'
  format_990061 = '{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}\n'
  fileout.write(format_99006.format("t", "alfa", "wdo", "bs", "Aa", "ha", "hb", "Fd [kN]", "Md [kNm]"))

  if wd > 0:
      # Closing calculation
      wds = wd
      tp = (ba - bb) / (wds * bd)
      j = 0
      t = 0
      ha = hk

      while t < 3 * tp:
        t += dt
        j += 1

        # Calculation doordebit
        Qd = 0.5 * wds* bd *(bd*(ha-zd))
        # Calculation minimal vertical size bs
        if t < tp:
          bs = bb+wds*t*bd
          if bs > (la-bd):
            bs = la-bd
        else:
          bs =  math.sqrt((la-bd)**2+(wds*(t-tp)*bd)**2)
          if bs > (bb+wds*t*bd):
            bs = bb+wds*t*bd
        # Calculation debit through vertical Qs
        csa  = cs*bs/bk
        csb  = cs*bs/(bc+wds*t*bd)
        csc  = 1-csa**2+2*csb**2-2*csb
        csv   = 1/math.sqrt(csc)
        if (hk-ha) >= 0:
          Qs = cs*bs*(hk-zk)*math.sqrt(abs(2*g*(hk-ha)/csc))
        else:
          Qs = -cs*bs*(hk-zk)*math.sqrt(abs(2*g*(ha-hk)/csc))

        # Calculation debit through openings Qg
        if (hk - ha) >= 0:
          Qg = mus*(Ao+(zd-zk)*bd)*math.sqrt(abs(2*g*(hk-ha)))
        else:
          Qg = -mus*(Ao+(zd-zk)*bd)*math.sqrt(abs(2*g*(ha-hk)))
    
        # Calculation momental area door Aa
        Aa = bd*bc + .5*wds*t*bd**2
        # Calculation water level door Aa
        dhat = (-Qd+Qs+Qg)/Aa
        ha   = ha + dhat*dt
        # Calculation water level chamber side
        hb   = hk + (Qd-Qs-Qg)/(2*bk*math.sqrt(g*(hk-zk)))
        # Calculation door corner 
        alfa = wds*t
        # Calculation door force
        Fd = .5*rho*g*bd*((ha-zd)**2-(hb-zd)**2)
        Md = .5*bd*Fd
        # Writing results
        if j == 5:
            fileout.write(f"{t:.3f} {alfa:.3f} {wds:.3f} {bs:.3f} {Aa:.3f} {ha:.3f} {hb:.3f} {Fd / 1000:.3f} {Md / 1000:.3f}\n")
            j = 0
  else:
      # Opening calculation
      wdo = wd
      ta = -(ba - bb) / (wdo * bd)
      tp = -ta
      te = 0
      j = 0
      t = -4 * ta
      ha = hk

      while t < te + 0.5 * ta:
        t += dt
        j += 1
        # Calculate door debit Qd
        if t < te:
          Qd = .5 * wdo * bd * (bd * (ha - zd))
        else:
          Qd = 0
          wdo = 0
        # Calculate minimum vertical gap size bs
        if t < tp:
          bs = math.sqrt((la-bd)**2+(wdo*(t-tp)*bd)**2) 
          if bs > (bb+wdo*(t-te)*bd):
            bs = (bb+wdo*(t-te)*bd)
        elif t < te:
          bs = la-bd
          if bs > (bb+wdo*(t-te)*bd):
            bs = (bb+wdo*(t-te)*bd)
        else:
          bs = la-bd
          if bs > bb:
            bs = bb
        
        # Calculate flow rate through vertical gap Qs
        if t < te:
          coa  = co*bs/(bc+wdo*(t-te)*bd)
        else: 
          coa  = co*bs/bc
        
        cob  = co*bs/bk
        coc  = 1-coa**2+2*cob**2-2*cob
        cov   = 1/math.sqrt(coc)
        if (ha-hk) >= 0:
          Qs  =  co*bs*(hk-zk)*math.sqrt(abs(2*g*(ha-hk)/coc))
        else:
          Qs  = -co*bs*(hk-zk)*math.sqrt(abs(2*g*(hk-ha)/coc))
        # Calculate flow rate through vertical gap Qs
        if (ha-hk) >= 0:
          Qg =  muo*(Ao+(zd-zk)*bd)*math.sqrt(abs(2*g*(ha-hk)))
        else:
          Qg = -muo*(Ao+(zd-zk)*bd)*math.sqrt(abs(2*g*(hk-ha)))
        
        # Calculate the instantaneous surface of the door box Aa
        if t < te:
          Aa  = bd*bc + .5*wdo*(t-te)*bd**2
        else: 
          Aa  = bd*bc
        # Calculate water level door greenhouse
        dhat = (-Qd-Qs-Qg)/Aa
        ha   = ha + dhat*dt
        # Calculate water level on the chamber side
        hb   = hk + (Qd+Qs+Qg)/(bk*math.sqrt(g*(hk-zk)))
        # Calculate door angle
        if t < te:
          alfa = wdo*t
        else:
          alfa  = 0
        # Calculate door force
        Fd = .5*rho*g*bd*((ha-zd)**2-(hb-zd)**2)
        Md = .5*bd*Fd

        # Writing results
        if j == 5:
          fileout.write(format_990061.format(t, alfa, wdo, bs, Aa, ha, hb, Fd / 1000, Md / 1000))
          j = 0
  fileout.close()

if __name__ == "__main__":
    filename = 'B001'
    gate7(filename)
