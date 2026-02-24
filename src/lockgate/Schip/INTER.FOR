      SUBROUTINE INTER (n,x,y,x1,y1)

C**********************************************************************
c     interpoleert lineair tussen de punten in de tabel
c     als x1.lt.x(1) dan y1=x(1); als x1.gt.x(n) dan y1=x(n)
c     de tabel moet stijgend zijn
c     n   : aantal waarden in de tabel (in)
c     x(n): array met x-waarden (in)
c     y(n): array met y-waarden (in)
c     x1  : x waarvoor functiewaarde gezocht wordt (in)
c     y1  : bevat bij return y(x1) (uit)
C**********************************************************************

      Integer  n, i, j
      Real     x(1:500), y(1:500), x1, y1

      j=0
      do 10 i=1,n
  10  if (x1 .gt. x(i)) j=i

      if (j .le. 0) then
        y1 = y(1)
      else if (j .ge. n) then
        y1 = y(n)
      else
        y1 = (y(j)*(x(j+1)-x1)+y(j+1)*(x1-x(j)))/(x(j+1)-x(j))
      endif

      end


