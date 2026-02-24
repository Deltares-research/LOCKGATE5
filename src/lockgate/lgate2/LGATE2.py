import math

def lgate2(filename):
  #     Waterstanden en krachten op deuren veroorzaakt door
  #         sluiten en openen van enkele draai-, punt- en roldeuren
  #     Waterloopkundig Laboratorium Delft
  #     Versie 2.00
  #     A. Vrijburcht, 4 maart 1994
  #     Deuren aan weerszijden van de kolk, met invloed reflecties
  #         van deuren en voorhavens
  #     Sluiten tijdens stroom, openen onder verval,
  #         sluiten en openen tijdens stilstaand water
  #     Wijziging met GATE6b: Deursnelheid als tabelinvoer
  from INTER import inter
  # Input
  outputName = fileName
  if os.path.exists(outputName + ".out"):
      os.remove(outputName+".out")

  file = open(fileName + ".in", "r")
  lines = [n for n in file.readlines() if not n.startswith('**')]
  lines = [x.replace('\n', '') for x in lines]

  #   �����������Ŀs1                                     s2�������������
  #               �spleet                             spleet�
  #               �������������������������������������������
  #   
  #   voorhaven   ��Ŀ                kolk               ��Ŀ     voorhaven
  #      v        �  �    k1                       k2    �  �       w
  #               �  �������������������������������������  �
  #               �deur                                 deur�
  #   �������������d1                                     d2�������������
  #
  #
  #.....1e regel: geometrie voorhaven v
  #     zv  = bodemniveau voorhaven v [mNAP]
  #     bv  = breedte voorhaven v [m]
  #.....2e regel: geometrie spleet 1
  #     zs1 = bodemniveau spleet 1 [mNAP]
  #.....3e regel: geometrie kolk
  #     zk  = bodemniveau kolk [mNAP]
  #     bk  = breedte kolk [m]
  #     lk  = lengte kolk [m]
  #     k   = ruwheid kolkwand [m]
  #.....4e regel: geometrie spleet 2
  #     zs1 = bodemniveau spleet 2 [mNAP]
  #.....5e regel: geometrie voorhaven w
  #     zw  = bodemniveau voorhaven w [mNAP]
  #     bw  = breedte voorhaven w [m]
  #.....6e regel: coefficienten
  #     c1or = contractiecoeff. geopende deur 1, stroming naar rechts [-]
  #     c1dr = contractiecoeff. gesloten deur 1, stroming naar rechts [-]
  #     c2or = contractiecoeff. geopende deur 2, stroming naar rechts [-]
  #     c2dr = contractiecoeff. gesloten deur 2, stroming naar rechts [-]
  #.....7e regel: coefficienten
  #     c1ol = contractiecoeff. geopende deur 1, stroming naar links [-]
  #     c1dl = contractiecoeff. gesloten deur 1, stroming naar links [-]
  #     c2ol = contractiecoeff. geopende deur 2, stroming naar links [-]
  #     c2dl = contractiecoeff. gesloten deur 2, stroming naar links [-]
  #.....8e regel: beginvoorwaarden
  #     hvi  = beginwaterstand voorhaven v [mNAP]
  #     dhi1= beginverval deur1 [m], positief is ws.voorh.v > ws.kolk1
  #     dhi2= beginverval deur2 [m], positief is ws.kolk2 > ws.voorh.w
  #     Qi  = initieel debiet [m3/s]
  #.....9e regel: div.
  #     rho = dichtheid water [kg/m3]
  #     dt  = rekentijdstap [s]
  #     te  = eindtijd berekening [s]  
  #.....10e regel: deurkeuze (p = integer)
  #     p = 1: enkele draaideuren
  #     p = 2: puntdeuren
  #     p = 3: roldeuren
  #.....11e regel: 
  #  -  enkele draaideur 1
  #     zd1  = niveau onderzijde deur1 [mNAP]
  #     alf1d= hoek waarbij deur1 sluiswandlijn raakt [rad]
  #     Ao   = totaal oppervlak deuropeningen [m2]
  #     bsni1= minimum breedte spleet1 tussen deurtip en -nis [m]
  #  -  puntdeur 1
  #     zd1  = niveau onderzijde deur1 [mNAP]
  #     alf1d= hoek waarbij deur1 sluisas raakt [rad]
  #     Ao   = totaal oppervlak deuropeningen [m2]
  #  -  roldeur 1
  #     zd1  = niveau onderzijde deur1 [mNAP]
  #     Ao   = totaal oppervlak deuropeningen [m2]
  #.....12e regel: 
  #     als 11e regel maar dan deur 2
  #.....13e regel:
  #  -  enkele draaideur1 en puntdeur1
  #     t1i  = start beweging deur1 [s]
  #     alf1i= starthoek deur1 [rad]
  #     alf1e= eindhoek deur1 [rad]
  #  -  roldeur
  #     t1i  = start beweging deur1 [s]
  #     bs10 = startopening deur1 [m]
  #     bs10 = eindopening deur1 [m]
  #.....14e regel: 
  #     als 13e regel maar dan deur 2
  #.....15e regel, etc: 
  #  -  enkele draaideur1 en puntdeur1
  #     nwd1  = aantal tabelwaarden deursnelheid 1 (p = integer)
  #     alf1t = deurhoek 1 tabel [rad] 
  #     wd1t  = deursnelheid 1 tabel [rad/s] 
  #  -  roldeur1
  #     nvd1  = aantal tabelwaarden deursnelheid 1 (p = integer)
  #     bs1t  = deurhoek 1 tabel [m] 
  #     vd1t  = deursnelheid 1 tabel [m/s] 
  #.....evenzo voor 2e deur

  g   = 9.81
  pi  = math.pi

  #     Initiele situatie
  #     Berekening van hk1i, hk2i en hwi bij gegeven hvi (=ws.voorh.v)
  #     dh1i = initieel verval over deur 1 bij Qi = o:
  #            ws.voorh.v hoger dan ws.kolk is positieve dh1i
  #     dh2i = initieel verval over deur 2 bij Qi = 0:
  #            ws.kolk hoger dan ws.voorh.w is positieve dh2i
  #     Qi   = initieel debiet bij dh1i en dh2i = 0:
  #            stroming naar rechts is positieve Qi
  #     Invloed vernauwing, verwijding en wrijving
  #     
  #        �����������Ŀs1                      s2�������������
  #                    �                          �
  #                    ����������������������������
  #           Qi       .            Qi            .       Qi
  #           v        s1  k1      kolk      k2  s2       w    
  #        voorhaven   .            k             .     voorhaven
  #                    ��������������������������Ŀ
  #                    �deur                  deur�
  #        �������������1                        2�������������
  
  # Calculation of initial situation
  if Qi == 0.0:
    # Initial debit for still water
    # Initial debit is zero
    # Initial decay over doors only with completely closed doors
    hk1i = hvi - dh1i
    hk2i = hk1i
    hwi  = hk2i - dh2i
    if (hk1i > hvi): Qs1 = -.000001
    if (hwi > hk2i): Qs2 = -.000001
  elif Qi > 0.0:
    # Initial debit larger than 0 stream from the right
    # Completely open doors
    vv    = Qi/(bv*(hvi-zv))
    c1a   = c1or*bk*(hvi-zs1)/(bv*(hvi-zv))
    c1b   = c1or*bk*(hvi-zs1)/(bk*(hvi-zk))
    c1c   = 1-c1a**2+2*c1b**2-2*c1b
    vs1   = Qi/(c1or*(hvi-zs1)*bk)
    hs1   = hvi + vv**2/(2*g) - vs1**2/(2*g)
    hk1i  = hvi - c1c*Qi**2/(2*g)/(c1or*bk*(hs1-zs1))**2
    vk1   = Qi/(bk*(hk1i-zk))
    Qs1   = Qi 
    R     = bk*(hk1i-zk)/(bk+2*(hk1i-zk))
    Cz    = 18*math.log10(12*R/k)
    kw    = 2*g*lk/(Cz**2*R)
    hk2i  = hk1i - kw*vk1**2/(2*g)
    vk2   = Qi/(bk*(hk2i-zk))
    c2a   = c2or*bk*(hk2i-zs2)/(bk*(hk2i-zk))
    c2b   = c2or*bk*(hk2i-zs2)/(bw*(hk2i-zw))
    c2c   = 1-c2a**2+2*c2b**2-2*c2b
    vs2   = Qi/(c2or*bk*(hk2i-zs2))
    hs2   = hk2i + vk2**2/(2*g) - vs2**2/(2*g)
    hwi   = hk2i - c2c*Qi**2/(2*g)/(c2or*bk*(hs2-zs2))**2
    Qs2   = Qi 
  else:
    # Initial debit lower than zero (stream to the left)
    hwi = hvi
    while abs(hvt-hvi) >= .01:
      vw    = Qi/(bw*(hwi-zw))
      c2a   = c2ol*bk*(hwi-zs2)/(bw*(hwi-zw))
      c2b   = c2ol*bk*(hwi-zs2)/(bk*(hwi-zk))
      c2c   = 1-c2a**2+2*c2b**2-2*c2b
      vs2   = Qi/(c2ol*(hwi-zs2)*bk)
      hs2   = hwi + vw**2/(2*g) - vs2**2/(2*g)
      hk2i  = hwi - c2c*Qi**2/(2*g)/(c2ol*bk*(hs2-zs2))**2
      vk2   = Qi/(bk*(hk2i-zk))
      Qs2   = Qi 
      R     = bk*(hk2i-zk)/(bk+2*(hk2i-zk))
      Cz    = 18*math.log10(12*R/k)
      kw    = 2*g*lk/(Cz**2*R)
      hk1i  = hk2i - kw*vk2**2/(2*g)
      vk1   = Qi/(bk*(hk1i-zk))
      c1a   = c1ol*bk*(hk1i-zs1)/(bk*(hk1i-zk))
      c1b   = c1ol*bk*(hk1i-zs1)/(bv*(hk1i-zv))
      c1c   = 1-c1a**2+2*c1b**2-2*c1b
      vs1   = Qi/(c1ol*bk*(hk1i-zs1)*bk)
      hs1   = hk1i + vk1**2/(2*g) - vs1**2/(2*g)
      hvt   = hk1i - c1c*Qi**2/(2*g)/(c1ol*bk*(hs1-zs1))**2
      Qs1   = Qi 
      hwi    = hwi + .005
    hvi = hvt

  # Output initial conditions
  fileout = open(outputName+".out", 'a')
  format_99006 = '*    t       alf1     wd1      bs1      alf2     wd2          bs2       hv\
         hk1      hk2      hw       F1/1000     M1/1000     F2/1000     M2/1000     Qs1\
                  Qs2 '
  format_990061 = '{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}{:10.3f}\n'
  format_9000 = '{:9.4f}{:9.4f}{:9.4f}{:9.4f}\n'
  format_9002 = '{:9.2f}{:9.4f}{:9.4f}{:9.4f}{:9.4f}{:9.4f}{:9.4f}{:9.3f}{:9.3f}{:9.3f}{:9.3f}{:12.3f}{:12.3f}{:12.3f}{:12.3f}{:12.3f}{:12.3f}\n'
  fileout.write(format_99006)
  fileout.write("AAAA")
  fileout.write("%d, %d" %(int(round(te/dt/5)), 17))
  fileout.write(format_9000.format(hvi, hk1i, hk2i, hwi))

  # Calculation door width
  if p == 1:
    bd = bk/math.sin(alf1d)
  elif p == 2:
    bd = bk/math.sin(alf1d)/2
  else:
    bd = bk

  # Calculation in time
  F1min, F2min, F1max, F2max = 0.0, 0.0, 0.0, 0.0
  t, i, j = 0.0, 0, 0

  while t <= te:
    t = t + dt
    i = i + 1
    j = j + 1

    # Calculation door corner, door corner speed, door debit

    # Calculation only for one turning door or point door
    if p <= 2:
      if t < t1i:
        alf1 = alf1i
        wd1 = 0.0
      else:
        wd1 = inter(nwd1, alf1t, wd1t, alf1)
        alf1 = alf1 + wd1*dt
        if wd1 > .0:
          if alf1 >= alf1e:
            wd1  = .0
            alf1 = alf1e
        else:
          if alf1 >= alf1e:
            wd1  = .0
            alf1 = alf1e
      # Door debit for single turning door 1 or point door 1      
      # Calculation Qd1
      if p == 1:
        Qd1 = .5*wd1*bd*(bd*(hvi-zd1)-Ao1)
      else:
        Qd1 = wd1*bd*(bd*(hvi-zd1)-Ao1)

      # Door corner and door speed for single turning door 2 and point door 2
      # Calculation alf2 and wd2
      if t < t2i: 
        alf2 = alf2i
        wd2   = .0
      else:
        wd2 = inter(nwd2,alf2t,wd2t,alf2)
        alf2 = alf2 + wd2*dt
        if wd2 > .0:
          if alf2 >= alf2e:
            wd2  = .0
            alf2 = alf2e
        else:
          if alf2 <= alf2e:
            wd2  = .0
            alf2 = alf2e
      # Door debit for single turning door 2 or point doors 2
      # Calculation Qd2
      if p == 1:
        Qd2 = .5*wd2*bd*(bd*(hwi-zd2)-Ao2)
      else:
        Qd2 = wd2*bd*(bd*(hwi-zd2)-Ao2)
    
    if p == 1:
      bs1 = bk - bd*math.sin(alf1)
      if bs1 < bsni1: bs1 = bsni1
      if alf1 > pi/2-.005:
        if alf1 < (pi/2+.005:
          bs1 = .00001
          Qd1 = .0
          wd1 = .0

      # Calculation bs2 at door 2
      bs2 = bk - bd*math.sin(alf2)
      if bs2 < bsni2: bs2 = bsni2
      if alf2 > (pi/2-.005):
        if alf2 < (pi/2+.005):
          bs2 = .00001
          Qd2 = .0
          wd2 = .0
    elif p == 2:
      bs1 = bk - 2*bd*math.sin(alf1)
      if bs1 <= .0:
        bs1 = .000001
        Qd1 = .0
        wd1 = .0

      # Calculation bs2 at door 2
      bs2 = bk - 2*bd*math.sin(alf2)
      if bs2 <= .0:
        bs2 = .000001
        Qd2 = .0
        wd2 = .0
    else:
      # Rolling door
      # Calculation bs1 by door 1
      if t < t1i:
        bs1 = bs1i
        vd1   = .0
      else:
        vd1 = inter(nvd1,bs1t,vd1t,bs1)
        bs1 = bs1 + vd1*dt
        if vd1 > .0:
          if bs1 >= bs1e:
            vd1  = .0
            bs1 = bs1e
        else:
          if bs1 <= bs1e:
            vd1  = .0
            bs1 = bs1e
      if bs1 <= .0: 
        bs1 = .000001
        vd1 = .0
      Qd1 = .0
      # Calculation bs2 with door 2
      if t < t2i:
        bs2 = bs2i
        vd2   = .0
      else:
        vd2 = inter(nvd2,bs2t,vd2t,bs2)
        bs2 = bs2 + vd2*dt
        if vd2 > .0:
          if bs2 >= bs2e:
            vd2 = .0
            bs2 = bs2e
        else:
          if bs2 <= bs2e:
            vd2 = .0
            bs2 = bs2e
      if bs2 <= .0: 
        bs2 = .000001
        vd2 = .0
      Qd2 = .0

    # Calculation contraction coefficients
    c1r = (c1or-c1dr)*bs1/bk + c1dr
    c2r = (c2or-c2dr)*bs2/bk + c2dr
    c1l = (c1ol-c1dl)*bs1/bk + c1dl
    c2l = (c2ol-c2dl)*bs2/bk + c2dl      

    # Calculation debit and height translation waves
    # Calculation period Tk
    Tk = 2*lk/math.sqrt(g*((hk1i+hk2i)/2-zk))
    nt = Tk/dt/2
    ni = int(round(nt))

    # Calculation nt1, hk1, Qt1, nt2, hk2 and Qt2
    if j == 1:
      # v reflection
      hv   = hvi
      Qt1  = .0
      nt1  = .0
      hk1  = hk1i
      Qt2  = .0
      nt2  = .0
      hk2  = hk2i
      hw   = hwi
    elif j < ni:
      # v reflection
      Qt1  = .0
      nt1  = .0
      Qt2  = .0
      nt2  = .0
    else:
      # n reflection
      Qt1  = Qk2l[j-ni]
      nt1  = -Qt1/(bk*math.sqrt(g*(hk1i-zk)))
      Qt2  = Qk1l[j-ni]
      nt2  =  Qt2/(bk*math.sqrt(g*(hk2i-zk)))
    
    # Calculation Wave heights
    if Qs1 >= 0:
      # Stream to right through vertical gap 1 (Qs1 > 0)
      c1a  = c1r*bs1*(hk1-zs1)/(bv*(hv -zv))
      c1b  = c1r*bs1*(hk1-zs1)/(bk*(hk1-zk))
      c1c  = 1-c1a**2+2*c1b**2-2*c1b
      A    = c1c/(2*g*(c1r*bs1*((hvi+hk1i)/2-zs1))**2)
      B    = 1/(bv*math.sqrt(g*(hvi-zv))) + 1/(bk*math.sqrt(g*(hk1i-zk)))
      C    = -(hvi-hk1+nk1)-(Qi-Qd1)    /(bv*sqrt(g*(hvi-zv))) - (Qi-Qd1+Qt1)/(bk*math.sqrt(g*(hk1i-zk)))
      Qs1  = (-B+math.sqrt(abs(B**2-4*A*C)))/(2*A)
      nv   =  (Qi-Qd1-Qs1)    /(bv*math.sqrt(g*(hvi-zv)))
      hv   = hvi + nv
      nk1  = -(Qi-Qd1+Qt1-Qs1)/(bk*math.sqrt(g*(hk1i-zk)))
      hk1  = hk1i + nt1 + nk1
      vs1  = Qs1/(c1r*(hk1-zs1)*bs1)
      hs1  = hv - vs1**2/(2*g)
      dh1  = hv - hk1
      dh1a = hv - (hs1+hk1)/2
      Qk1l[j] = -(Qi-Qd1+Qt1-Qs1)
    else:
      # Stream to left through vertical gap 1 (Qs1 < 0)
      c1a  = c1l*bs1*(hk1-zs1)/(bk*(hk1-zk))
      c1b  = c1l*bs1*(hk1-zs1)/(bv*(hv-zv))
      c1c  = 1-c1a**2+2*c1b**2-2*c1b
      A    = c1c/(2*g*(c1l*bs1*((hvi+hk1i)/2-zs1))**2)
      B    = -1/(bv*math.sqrt(g*(hvi-zv))) - 1/(bk*math.sqrt(g*(hk1i-zk)))
      C    = (hvi-hk1+nk1) +(Qi-Qd1) /(bv*math.sqrt(g*(hvi-zv))) + (Qi-Qd1+Qt1)/(bk*math.sqrt(g*(hk1i-zk)))
      Qs1  = (-B-math.sqrt(abs(B**2-4*A*C)))/(2*A)
      nv   =  (Qi-Qd1-Qs1)/(bv*math.sqrt(g*(hvi-zv)))
      hv   = hvi + nv
      nk1  = -(Qi-Qd1+Qt1-Qs1)/(bk*math.sqrt(g*(hk1i-zk)))
      hk1  = hk1i + nt1 + nk1
      vs1  = Qs1/(c1l*(hk1-zs1)*bs1)
      hs1  = hv - vs1**2/(2*g)
      dh1  = hv - hk1
      dh1a = (hs1+hv)/2 - hk1
      Qk1l[j] = -(Qi-Qd1+Qt1-Qs1)

    if Qs2 < 0:
      # Stream to left through vertical gap 2 (Qs2 < 0)
      c2a  = c2l*bs2*(hk2-zs2)/(bw*(hw-zw))
      c2b  = c2l*bs2*(hk2-zs2)/(bk*(hk2-zk))
      c2c  = 1-c2a**2+2*c2b**2-2*c2b
      A    = c2c/(2*g*(c2l*bs2*((hwi+hk2i)/2-zs2))**2)
      B    = 1/(bw*math.sqrt(g*(hwi-zw))) + 1/(bk*math.sqrt(g*(hk2i-zk)))
      C    = -(hwi-hk2+nk2)+(Qi-Qd2)/(bw*math.sqrt(g*(hwi-zw))) + (Qi-Qd2+Qt2)/(bk*math.sqrt(g*(hk2i-zk)))
      Qs2  = -(-B+math.sqrt(abs(B**2-4*A*C)))/(2*A)
      nk2  = (Qi-Qd2+Qt2-Qs2)/(bk*math.sqrt(g*(hk2i-zk)))
      hk2  = hk1i + dhk + nt2 + nk2
      nw   = -(Qi-Qd2-Qs2)/(bw*math.sqrt(g*(hwi-zw)))
      hw    = hwi + nw
      vs2  = Qs2/(c2l*(hk2-zs2)*bs2)
      hs2  = hw - vs2**2/(2*g)
      dh2  = hk2 - hw 
      dh2a = (hs2+hk2)/2 - hw 
      Qk2l[j] = -(Qi-Qd2+Qt2-Qs2)
    else:
      # Stream to right through vertical gap 2 (Qs2 < 0)
      c2a  = c2r*bs2*(hk2-zs2)/(bk*(hk2-zk))
      c2b  = c2r*bs2*(hk2-zs2)/(bw*(hw-zw))
      c2c  = 1-c2a**2+2*c2b**2-2*c2b
      A    = c2c/(2*g*(c2r*bs2*((hwi+hk2i)/2-zs2))**2)
      B    = -1/(bw*math.sqrt(g*(hwi-zw))) - 1/(bk*math.sqrt(g*(hk2i-zk)))
      C    = (hwi-hk2+nk2) -(Qi-Qd2)/(bw*math.sqrt(g*(hwi-zw))) - (Qi-Qd2+Qt2)/(bk*math.sqrt(g*(hk2i-zk)))
      Qs2  = -(-B-math.sqrt(abs(B**2-4*A*C)))/(2*A)
      nk2  = (Qi-Qd2+Qt2-Qs2)/(bk*math.sqrt(g*(hk2i-zk)))
      hk2  = hk1i + dhk + nt2 + nk2
      nw   = -(Qi-Qd2-Qs2)/(bw*math.sqrt(g*(hwi-zw)))
      hw   = hwi + nw
      vs2  = Qs2/(c2r*(hk2-zs2)*bs2)
      hs2  = hw - vs2**2/(2*g)
      dh2  = hk2 - hwi 
      dh2a = hk2 - (hs2+hwi)/2 
      Qk2l[j] = -(Qi-Qd2+Qt2-Qs2)

    # Calculation decrease through friction losses vortex
    Qsg   = (Qs1+Qs2)/2
    vk    = Qsg/(bk*((hk1+hk2)/2-zk))
    R     = bk*((hk1+hk2)/2-zk)/(bk+2*((hk1+hk2)/2-zk))
    Cz    = 18*math.log10(12*R/k)
    kw    = 2*g*lk/(Cz**2*R)
    if Qsg >= .0:
      dhk = -kw*vk**2/(2*g)
    else:
      dhk =  kw*vk**2/(2*g)

    # Calculation forces
    # Toelichting:
    # Kracht wordt steeds berekend voor de enkele deur: dus ook per puntdeur
    # Kracht wordt berekend over de gehele deurbreedte: ook voor roldeur
    # (waterstand in deurkas komt overeen met kolk en voorhaven)
    if p <= 2: 
      F1 = .5*rho*g*bd*((hv-zd1)**2-(hk1-zd1)**2)
      F2 = .5*rho*g*bd*((hk2-zd2)**2-(hw-zd2)**2)
      M1 = F1 * bd/2
      M2 = F2 * bd/2
    else:
      F1 = .5*rho*g*bd*((hv-zd1)**2-(hk1-zd1)**2)
      F2 = .5*rho*g*bd*((hk2-zd2)**2-(hw-zd2)**2)
      M1 = .0
      M2 = .0

    # Output results and extremes  
    if i == 5: # save every 5 steps
      if p <= 2:
        fileout.write(format_9002.format(t, alf1, wd1, bs1, alf2, wd2, bs2, hv, hk1, hk2, hw, F1/1000, M1/1000, F2/1000, M2/1000, Qs1, Qs2)) 
      else:
        fileout.write(format_9002.format(t, pi/2, vd1, bs1, pi/2, vd2, bs2, hv, hk1, hk2, hw, F1/1000, .0, F2/1000, .0, Qs1, Qs2))

      if F1 < F1min:
        F1min = F1
      if F2 < F2min:
        F2min = F2
      if F1 > F1max:
        F1max = F1
      if F2 > F2max:
        F2max = F2
      i = 0
    
  # Finalize output
  format_9005 = '{:12.3f}{:12.3f}{:12.3f}{:12.3f}\n'
  fileout.write(format_9005.format(F1min/1000, F1max/1000, F2min/1000, F2max/1000))
  fileout.close()