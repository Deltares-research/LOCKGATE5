      PROGRAM KOOM1

C     - INVAREN SLUIS
C     - Schematische berekening van max. golfhoogten in sluiskolk tijdens 
C       invaart volgens Kooman
C     - Versie 1.00
C     - Waterloopkundig Laboratorium Delft
C     - A. Vrijburcht, 13 september 1993


      integer i, j
      real hk, bk 
      real bs, ds, vs
      real g
      real Ak, As
      real dhk, dvs
      real alfa1, alf1


      open (1,file=' ')
      read (1,*) hk, bk 
      read (1,*) bs, ds, vs
      close (1)

      open  (2,file=' ')

      g   = 9.81
      As = bs*ds
      dhk = (hk-ds)/22
      dvs = vs/22

      do 500 i = 1,20
      hk = hk - dhk
      Ak = bk*hk
      vs = 0.

      do 400 j = 1,20
      vs = vs + dvs

      alf1  = .7*vs**2/(g*hk)*(As/Ak)/(1-(As/Ak))*hk
      alfa1 = alf1*bk*sqrt(g*hk)/(vs*As)

      write (2,252) vs/sqrt(g*hk), As/Ak, alfa1

  400 continue

  500 continue

  252 format (3(F7.4,','))

      close (2)
      end

