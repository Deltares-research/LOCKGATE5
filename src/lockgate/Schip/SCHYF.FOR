      PROGRAM SCHYF

C     - VAREN IN KANAAL
C     - Berekening grenssnelheid, inzinking en retourstroomsnelheid in 
C       prismatisch kanaal
C     - Versie 1.00
C     - Waterloopkundig Laboratorium Delft
C     - A. Vrijburcht, 10 september 1993


C.....DECLARATIES......................................

      integer i, j

      real hv, bv, dhv
      real bs, ds, vs
      real alfa
      real rho, g
      real Av, As
      real c0, c1, c2, c3, c4, c5
      real y1, p1, vg, vgd
      real u1, u5, u
      real x1, x5, x
      real zv, zvd, ud
      real dvg, vsd


C.....INVOER.............................................

      open (1,file=' ')
      read (1,*) hv, bv
      read (1,*) ds, bs
      read (1,*) alfa
      close (1)

      open (2,file=' ')
      open (3,file=' ')


C.....VASTE WAARDEN.....................................
      g  = 9.81
      As = bs*ds


c.....LUS VOOR WATERDIEPTE
      dhv = (hv-ds)/21
      do 300  i = 1,20
      hv = hv - dhv
      Av = bv*hv


C.....GRENSBEREKENING....................................

c.....startwaarde
      y1 =.6*(1-As/Av)**2*sqrt(g*hv)

  100 continue
      c0 = ((alfa-1)*y1**3 + 2*g*As/bv*y1) / alfa
      c1 = ((3*alfa-1)*y1**2 - 2*g*(Av-As)/bv) / alfa
      c2 = 3*y1 
      c3 = (3*alfa-1)*y1**2 - 2*g*(Av-As)/bv
      c4 = 6*y1
      c5 = 3*alfa
      u  = (-c4 + sqrt(c4**2-4*c3*c5)) / (2*c5)
      p1 = u**3 + c2*u**2 + c1*u + c0
      if (abs(p1) .lt. .5) then
        vg  = y1
        vgd = vg/sqrt(g*hv)
      else
        y1 = y1 + .001
        goto 100
      endif
      write (2,210) As/Av, vgd, ds/hv


C.....SCHIJFBEREKENING...................................

C.....LUS VOOR VAARSNELHEID
      vs = .0
      dvg = vg/41
      do 200  j = 1,40
      vs = vs + dvg

      c0 = ((alfa-1)*vs**3 + 2*g*As/bv*vs) / alfa
      c1 = ((3*alfa-1)*vs**2 - 2*g*(Av-As)/bv) / alfa
      c2 = 3*vs 
      u1 = -1.5*c0/c1
      x1 = u1**3+c2*u1**2+c1*u1+c0
      u5 = -c0/c1
      x5 = u5**3+c2*u5**2+c1*u5+c0
      if ((x1*x5) .lt. 0) then
        goto 205
      else
        stop
      endif
  205 continue
      u = (u1*x5-u5*x1)/(x5-x1)
      x = u**3+c2*u**2+c1*u+c0
      if ((x*x5) .lt. 0) then
        u1 = u
        x1 = x
      else
        u5 = u
        x5 = x
      endif
      if (abs(x) .ge. .00001) goto 205

      vsd = vs/sqrt(g*hv)
      ud = u/sqrt(g*hv)
      zv = (alfa*(vs+u)**2-vs**2)/(2*g)
      zvd = zv/hv
      write (3,211) vsd, As/Av, zvd, ud

  210 format (3(F7.4,','))
  211 format (4(F7.4,','))

  200 continue

  300 continue

      close (2)
      close (3)

      END

