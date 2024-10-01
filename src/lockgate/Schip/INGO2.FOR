      PROGRAM INGO2

C     - INVAREN SLUIS
C     - Schematische berekening van max. golfhoogten in sluiskolk tijdens 
C       invaart / Constant schroefvermogen totdat boeg 1/3 van de
C       sluislengte ingevaren is
C     - Versie 1.00, rekenhart van INVA3
C     - Waterloopkundig Laboratorium Delft
C     - A. Vrijburcht, 13 september 1993


C=====DECLARATIES========================================

      integer i, j
      real hv, bv, hk, bk 
      real ms, ls, bs, ds, Ps
      real Cp, Cf, Cz, Ck, Cr, lamb
      real xi, xo, xe, lk
      real rho, g
      real Av, Ak, As, Ss, Fr, x, dx, dPs, dhk
      real Xw1, Xw2, p, vs, dvs, t, dt, vsi
      real A, B, C, uk, nk, uv, zv, Ee
      real vso, to, tfe, tff, xf, te, vse, ton
      real lamb1, lamb2, lamb3, lamb4
      real lam1, lam2, lam3


C=====INVOER============================================

      open (1,file=' ')

      read (1,*) hv, bv, lk, hk, bk 
      read (1,*) ms, ls, bs, ds, Ps
      read (1,*) Cp, Cf, Cz, Ck, Cr

C.....Toelichting Invoer
C     hv  = waterdiepte voorhaven [m]
c     bv  = breedte voorhaven [m]
c     lk  = lengte kolk [m]
c     hk  = maximum waterdiepte kolk [m]
c     bk  = breedte kolk [m]
C     ms  = massa schip [kg]
c     ls  = lengte schip [m]
c     bs  = breedte schip [m]
c     ds  = diepgang schip [m]
c     Ps  = maximum motorvermogen schip [W]
C     Cp  = coefficient drukweerstand schip, stel 0.2 [-]
c     Cf  = coefficient wrijvingsweerstand schip, stel 0.002 [-]
c     Cz  = coefficient hekvertraging schip, stel voor duweenheden 0.6
c                           en stel voor overige schepen 0.25 [-]
c     Ck  = coefficient kolkgolf schip, stel 1.00 [-]
c     Cr  = omrekenfactor schroefkracht, stel voor duweenheden 5.5
c                           en stel voor overige schepen 7.35 [W/N]

      close (1)
      open  (2,file=' ')
      open  (3,file=' ')


c     Vaste waarden
      rho = 1000.
      g   = 9.81
      xi  = -1000.
      Av = bv*hv
      As = bs*ds
      Ss = (bs+2*ds)*ls

      dhk = (hk-ds)/21
      dPs = .04*Ps


C=====BEREKENING=========================================

      do 500 i = 1,20
      hk = hk - dhk
      Ak = bk*hk
      Ps  = .0


      do 400 j = 1,25
      Ps = Ps + dPs
      Fr = Ps/Cr
      vsi = .9*sqrt(Fr/(.5*rho*(Cp*As+Cf*Ss)))

c     Lopende variabelen:
c     t  = tijd [s]
c     x  = plaats boeg in x-assenstelsel [m]
c     vs = vaarsnelheid [m/s]

c     Startwaarden:
      t  = 0
      x  = xi
      vs = vsi


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
c     write (2,150) t, x, vs, -zv 

c     testen op constante vaarsnelheid tbv. overgang voorhaven/sluis
      if (abs(dvs) .gt. .0001) then 
        goto 110
      else
        x   = .0
        xo  = .0
        t   = .0
        to  = t
        vso = vs
        xe  = lk
        xf  = x
        tfe = 10000.0
        tff = 10000.0
        goto 200
      endif


C=====Snelheid in kolk====================================
  200 continue

c     lengtestap in sluis is 1 m
      dx  = 1
c     lamb is contractie stroming na boeg schip,
c        is gesteld op 1 (geen contractie)
      lamb= 1
      if (vs .le. 0) vs = .01

  210 continue
      x  = x + dx
      dt = dx/vs 

      if (x .ge. (xo+bs/2) .and. x .lt. (xo+bs/2+dx)) ton = t

c     xf is voorzijde front transl. golf
      if (t .lt. tfe) then
        xf = xf + dt*sqrt(g*hk)
        if (xf .gt. xe) tfe = t
      elseif (t .lt. tff) then
        xf = xf - dt*sqrt(g*hk)
        if (xf .lt. x) tff = t
      else
        xf = xf - dt*sqrt(g*hk)
      endif

c     vereenv. oplossing van waterspiegelafzinking uit Schijf:
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
      B   = bk*vs*(sqrt(g*hk)-vs)/g    +lamb*(Ak-As)
      C   = -vs*As
      uk  = (-B+sqrt(abs(B**2-4*A*C)))/(2*A)
      nk  = uk**2/(2*g) + vs*uk/g

      if (t .eq. ton) lamb1 = nk/(vso*As/(bk*sqrt(g*hk)))
      if (t .eq. ton) lamb2 = (nk+zv)/(vso*As/(bk*sqrt(g*hk)))
      if (t .eq. tff) lamb3 = lamb1+(nk+zv)/(vso*As/(bk*sqrt(g*hk)))
      if (t .eq. ton) lam1  = nk
      if (t .eq. ton) lam2  = nk+zv
      if (t .eq. tff) lam3  = lam1+nk+zv

c     Xw2 = weerstand in sluis tgv. drukweerstand in kolk,
c             wrijvingsweerstand in kolk, vertragingsverlies 
c             hek in voorhaven en translatiegolf in sluis
      Xw2 =.5*rho*(Cp*As +Cf*Ss*((vs+uk)/vs)**2)
     &                   +Cz*rho*g*As*zv/vs**2
     &                   +Ck*rho*g*As*nk/vs**2

      if (x .gt. lk/3) Fr = .0
      dvs = (-Xw2*vs**2+Fr)/(1.2*ms)
      vs  = vs + dvs*dt
      if (vs .lt. .01) goto 300
      t   = t + dt
c     write (2,160) t, x, vs, -zv, nk, xf 

      if (x .lt. (xe-dx)) then 
        goto 210
      else
        te  = t
        vse = vs
        lamb4 = vse/vso
c       Ee = energie bij beschouwde deur, toeg.watermassa 20 %
c       Ee = 0.5*1.2*ms*vs**2
        goto 300
      endif


C=====EINDUITVOER===============================================

  300 continue
      write (2,252) vso/sqrt(g*hk),As/Ak,lamb1,lamb2,lamb3,lamb4
      write (3,253) vso, Ak, lam1, lam2, lam3, vse, tff, te

  400 continue

  500 continue

c 160 format (F8.2,', ',F8.2,', ',4(F8.3,', '))
  252 format (6(F7.4,','))
  253 format (6(F7.3,','),2(F7.1,','))

C     TOELICHTING UITVOER
c     vso  = snelheid bij invaart kolk     
c     lam1 = translatiegolfhoogte bij invaart     
c     lam2 = translatiegolfhoogte + waterspiegelafzinking bij invaart     
c     lam3 = translatiegolfhoogte + waterspiegelafzinking bij moment
c              dat front transl. golf de boeg bereikt
c     vse  = vaarsnelheid bij aanvaren gesloten deur
c     to  = moment invaren kolk
c     tff = moment front transl. golf bereikt boeg
c     te  = moment aanvaren gesloten deur


      close (2)
      close (3)
      end

