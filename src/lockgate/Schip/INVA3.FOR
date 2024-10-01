      PROGRAM INVA3

C     - INVAREN SLUIS
C     - Schematische berekening van vaarsnelheid in voorhaven en sluis bij:
C       . gegeven initiele, eenparige vaarsnelheid
C       . gegeven schroefvermogen
C       . schroefkracht constant tot de gegeven plaats van schroefuitval
C     - Voor berekening van vaarsnelheid en kin. energie bij 2e sluisdeur
C     - Versie 1.00, zelfde als INVA4, wegschrijven tijd- en einduitvoer
C     - Waterloopkundig Laboratorium Delft
C     - A. Vrijburcht, 19 november 1991


C=====DECLARATIES========================================

      real hv, bv, hk, bk 
      real ms, ls, bs, ds, Ps
      real Cp, Cf, Cz, Ck, Cr, alfa
      real xi, xo, xe, xu, vsi
      real rho, g
      real Av, Ak, As, Ss, Fr, x, dx
      real Xw1, Xw2, p, vs, dvs, t, dt, pu, vsu
      real A, B, C, uk, nk, uv, zv, Ee
      real uvi, zvi


C=====INVOER============================================

      open (1,file=' ')

      read (1,*) hv, bv, hk, bk 
      read (1,*) ms, ls, bs, ds, Ps
      read (1,*) Cp, Cf, Cz, Ck, Cr
      read (1,*) xi, xo, xe, xu, vsi

C.....Toelichting Invoer
C     hv  = waterdiepte voorhaven [m]
c     bv  = breedte voorhaven [m]
c     hk  = waterdiepte kolk [m]
c     bk  = breedte kolk [m]
C     ms  = massa schip [kg]
c     ls  = lengte schip [m]
c     bs  = breedte schip [m]
c     ds  = diepgang schip [m]
c     Ps  = motorvermogen schip [W]
C     Cp  = coefficient drukweerstand schip, stel 0.2 [-]
c     Cf  = coefficient wrijvingsweerstand schip, stel 0.002 [-]
c     Cz  = coefficient hekvertraging schip, stel voor duweenheden 0.6
c                           en stel voor overige schepen 0.25 [-]
c     Ck  = coefficient kolkgolf schip, stel 1.00 [-]
c     Cr  = omrekenfactor schroefkracht, stel voor duweenheden 5.5
c                           en stel voor overige schepen 7.35 [W/N]
C     xi  = initiele x van boeg [m]
c     xo  = x van sluisingang [m]
c     xe  = x van beschouwde deur [m]
c     xu  = x van afslaan motor [m]
c     vsi = initiele snelheid schip [m/s]

      close (1)
      open  (2,file=' ')


C=====BEREKENING=========================================

c     Vaste waarden
      rho = 1000
      g   = 9.81

c     Doorsneden, ed.
      Av = bv*hv
      Ak = bk*hk
      As = bs*ds
      Ss = (bs+2*ds)*ls
      Fr = Ps/Cr

c     Lopende variabelen:
c     t  = tijd [s]
c     x  = plaats boeg in x-assenstelsel [m]
c     vs = vaarsnelheid [m/s]

c     Startwaarden:
      t   = 0
      x  = xi
      if (vsi .le. .01) vsi = .01
      vs = vsi
      A   = 3*vsi
      B   = 2*vsi**2 - 2*g*(Av-As)/bv
      C   = 2*g*vsi*As/bv
      uvi  = (-B-sqrt(abs(B**2-4*A*C)))/(2*A)
      zvi  = (uvi**2 + 2*vsi*uvi) / (2*g)
      write (2,150) t, x, vsi, -zvi 

      if (xi .lt. (xo+.5*bs)) then
        goto 100
      else 
        goto 200
      endif


C=====Snelheid in voorhaven========================================
  100 continue

c     lengtestap in voorhaven is 1 m
      dx  = 1
      if (vs .le. .01) vs = .01

  110 continue

      if (vs .le. .25) then
        dx = .10
      else 
        dx = 1.00
      endif
      dt = dx/vs 
      x  = x + dx

c     schroef valt eventueel uit na xu
      if (x .lt. xu) then 
        Fr = Fr
      else
        Fr = 0
      endif

c     vereenv. oplossing van waterpiegelafzinking uit Schijf:
c          vs*Av = (vs+uv)*(Av-As-bv*zv)  en
c          2*g*zv + (vs+uv)**2 = vs**2 
      A   = 3*vs
      B   = 2*vs**2 - 2*g*(Av-As)/bv
      C   = 2*g*vs*As/bv
      uv  = (-B-sqrt(abs(B**2-4*A*C)))/(2*A)
      zv  = (uv**2 + 2*vs*uv) / (2*g)

c     Xw1 = weerstand in voorhaven tgv. drukweerstand,
c              wrijvingsweerstand en vertragingsverlies hek 
      Xw1 = .5*rho*(Cp*As +Cf*Ss*((vs+uv)/vs)**2)
     &                    +Cz*rho*g*As*zv/vs**2

      dvs = (-Xw1*vs**2+Fr)/(1.2*ms)
      vs  = vs + dvs*dt
      t   = t + dt
      write (2,150) t, x, vs, -zv 

      if (vs .le. 0.01) then 
         goto 310
      else 
         goto 130
      endif

  130 continue
c     testen op einde vaarweg
      if (x .lt. (xe-dx)) then 
        goto 140
      else
        goto 300
      endif

  140 continue 
c     testen op overgang voorhaven/sluis
      if (x .lt. (xo+.5*bs)) then 
        goto 110
      else
        goto 200
      endif


C=====Snelheid in kolk====================================
  200 continue

c     lengtestap in sluis is 1 m
      dx  = 1
c     alfa is contractie stroming na boeg schip,
c        is gesteld op 1 (geen contractie)
      alfa= 1
      if (vs .le. 0) vs = .01

  210 continue
      x  = x + dx
      dt = dx/vs 
c     schroef valt eventueel uit na xu
      if (x .lt. xu) then 
        Fr = Fr
      else
        Fr = 0
      endif

c     vereenv. oplossing van waterpiegelafzinking uit Schijf:
c          vs*Av = (vs+uv)*(Ak-As-bv*zv)  en
c          2*g*zv + (vs+uv)**2 = vs**2 
      A   = 3*vs
      B   = 2*vs**2 - 2*g*(Av-As)/bv
      C   = 2*g*vs*As/bv
      uv  = (-B-sqrt(abs(B**2-4*A*C)))/(2*A)
      zv  = (uv**2 + 2*vs*uv) / (2*g)

c     oplossing van golfhoogte kolk uit:
c          vs*(As+bk*nk) = nk*sqrt(g*hk) + (Ak-As)*uk  en
c          2*g*nk + vs**2 = (vs+uk)**2 
      A   = bk*   (sqrt(g*hk)-vs)/(2*g)
      B   = bk*vs*(sqrt(g*hk)-vs)/g    +alfa*(Ak-As)
      C   = -vs*As
      uk  = (-B+sqrt(abs(B**2-4*A*C)))/(2*A)
      nk  = uk**2/(2*g) +vs*uk/g

c     Xw2 = weerstand in sluis tgv. drukweerstand in kolk,
c             wrijvingsweerstand in kolk, vertragingsverlies 
c             hek in voorhaven en translatiegolf in sluis
      Xw2 =.5*rho*(Cp*As +Cf*Ss*((vs+uk)/vs)**2)
     &                   +Cz*rho*g*As*zv/vs**2
     &                   +Ck*rho*g*As*nk/vs**2

      dvs = (-Xw2*vs**2+Fr)/(1.2*ms)
      vs  = vs + dvs*dt
      t   = t + dt
      write (2,160) t, x, vs, -zv, nk 

      if (vs .le. 0.01) then 
         goto 310
      else 
         goto 230
      endif

  230 continue
      if (x .lt. (xe-dx)) then 
        goto 210
      else
        goto 300
      endif


C=====EINDUITVOER===============================================

  300 continue
c     Ee = energie bij beschouwde deur, toeg.watermassa 20 %
      Ee = 0.5*1.2*ms*vs**2
      write (2,250) hv, bv, hk, bk, ms, ls, bs, ds, Ps,
     &              xi, xo, xe, xu, vsi, vs, Ee 
      goto 400

  310 continue
      write (2,250) hv, bv, hk, bk, ms, ls, bs, ds, Ps,
     &              xi, xo, xe, xu, vsi, .0, .0 
      goto 400

  150 format (F8.2,', ',F8.2,', ',F8.4,', ',F8.4)
  160 format (F8.2,', ',F8.2,', ',F8.4,', ',F8.4,', ',F8.4)
  250 format (4(F7.2,','),F10.0,',',
     &        3(F7.2,','),F10.0,',',
     &        4(F9.2,','),2(F8.3,','),F10.0)

  400 continue
      close (2)
      end




