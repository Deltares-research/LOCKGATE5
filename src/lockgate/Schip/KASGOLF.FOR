      PROGRAM KASGOLF

C     Doordringen van golf van langsvarend schip in de deurkas
C     Versie 1.00
C     Waterloopkundig Laboratorium Delft
C     A. Vrijburcht, 7 september 1993


C=====DECLARATIES========================================

      INTEGER I, J, K, N, L, P, NT1, M1, NT2, M2
      INTEGER NKAS, NK, M0

      REAL T, TINIT, TEND, DT, G
      REAL HKI, ZK, LKK, VS
      REAL LKAS, BKAS, BA, BB, AO, MU
      REAL T1(0:20), N1(0:20)
      REAL T2(0:20), N2(0:20)

      REAL CK, DTT, DTG
      REAL NKASR, HKAS
      REAL NV, NW, NA, NB, NAO, NBO, NAN, NBN 
      REAL NAT, NBT
      REAL QAT, QBT
      REAL HV, HW, HA, HB
      REAL G1, G2, G3, G4, G5, G6, G7, G8, G9, GGEM
      REAL H1, H2, H3, H4, H5, H6, H7, H8, H9, HGEM
      REAL QA(0:1000), QB(0:1000), QAA, QBB


C=====INVOER=====================================================

      OPEN (1,FILE=' ')
      READ (1,*) HKI, ZK
      READ (1,*) LKK
      READ (1,*) LKAS, BKAS, BA, BB, AO, MU
      READ (1,*) DT, TINIT, TEND
      READ (1,*) M0, VS
      READ (1,*) NT1
      DO 30  M1 = 1, NT1
        READ (1,*) T1(M1), N1(M1)
   30 CONTINUE
      CLOSE (1)

c.....TOELICHTING INVOER
c     HKI  = initiele waterstand [mNAP]
c     ZK   = niveau kolk- en deurkasbodem [mNAP]
c     LKK  = lengte deurkas kolkzijde [m]
c     LKAS = lengte deurkas kaszijde [m]
c     BKAS = breedte deurkas kaszijde [m]
c     BA   = breedte verticale spleet A [m]
c     BB   = breedte verticale spleet B [m]
c     AO   = oppervlakte deuropeningen incl. onderzijde deur [m2]
c     MU   = afvoercoeff. verticale spleten A en B [-]
c     DT   = tijdstap [s]
c     TINIT = begintijd [s]
c     TEND  = eindtijd [s]
c     M0   = keuze golf met translatiegolfsnelheid (=0)
c                       of vaarsnelheid (=1) (integer!)
c     VS   = vaarsnelheid [m/s]
c     M1   = aantal op te geven punten tabel (integer!)
c     T1   = tijd tabel [s]
c     N1   = golfhoogte kolkzijde tpv spleet A [m]

      G = 9.81

      OPEN (2,FILE=' ')


C=====INITITALISATIE===============================================

C.....STARTWAARDEN VOOR GOLVEN
      J = 0
      K = 0
      T = TINIT
      HKAS = HKI
      DO 100 I = 0,1000
         QA(I) = 0
         QB(I) = 0
  100 CONTINUE
      QAT   = 0
      QBT   = 0
      NA    = 0
      NB    = 0
      NAT   = 0
      NBT   = 0

c.....LENGTE ARRAY VOOR GOLVEN
      CK    = SQRT(G*(HKI-ZK))
      IF (M0 .EQ. 0) THEN
        DTG = LKK/CK
      ELSE
        DTG = LKK/VS
      ENDIF
      NKASR = LKAS/CK/DT
      NKAS  = NINT (NKASR)
      NK    = NINT (NKAS/10)
      N     = INT(1.1*NKAS)
      IF (N .GE. 1000) THEN
        WRITE (*,*) 'VERGROOT TIJDSTAP'
        STOP
      ENDIF


C=====BEREKENING TRANSLATIEGOLVEN IN DEURKAS=====================

 200  CONTINUE
      J = J+1
      K = K+1
      T = T+DT
      CALL INTER (NT1,T1,N1,T,NV)
      CALL INTER (NT1,T1,N1,T-DTG,NW)

c.....berekening tot array zijn maximum bereikt
      IF (J .LE. N) THEN

        P = 0
c.......inkomende debieten 
        IF (J .GE. NKAS) THEN 
          QAT = QB(J-NKAS) 
          QBT = QA(J-NKAS) 
        ENDIF 
c.......inkomende golfhoogten 
        NAT = -QAT / (BKAS*CK)
        NBT =  QBT / (BKAS*CK)
 201  CONTINUE
        P = P + 1
c.......oude gegenereerde golfhoogten 
        NAO  =  NA
        NBO  =  NB
c.......nieuwe gegenereerde debieten 
        QA(J) = MU*BA*(HKI-ZK)*
     &          SIGN(1,(NV-NA-NAT))*SQRT(2*G*ABS(NV-NA-NAT)) - QAT
        QB(J) = MU*BB*(HKI-ZK)*
     &          SIGN(1,(NB+NBT-NW))*SQRT(2*G*ABS(NB+NBT-NW)) - QBT
c.......nieuwe gegenereerde golfhoogten 
        NAN =  QA(J) / (BKAS*CK)
        NBN = -QB(J) / (BKAS*CK)
c.......gecorrigeerde gegenereerde golfhoogten 
        NA  =  (1.8*NAO+0.2*NAN)/2
        NB  =  (1.8*NBO+0.2*NBN)/2
c.......test voldoende nauwkeurige gegenereerde golfhoogten 
        IF (P . GT. 1000) GOTO 202 
        IF (ABS(NAO-NA) .GE. .001) GOTO 201 
        IF (ABS(NBO-NB) .GE. .001) GOTO 201 
  202   CONTINUE

c.....waterstanden deurkas
        HV = HKI + NV
        HA = HKAS + NA + NAT
        IF (J .GE. 9*NK) THEN 
          H1 = HKAS + (QA(J-NK)   - QB(J-9*NK)) / (BKAS*CK)
          H9 = HKAS + (QA(J-9*NK) - QB(J-NK))   / (BKAS*CK)
        ELSEIF (J .GE. NK) THEN 
          H1 = HKAS + QA(J-NK) / (BKAS*CK)
          H9 = HKAS - QB(J-NK) / (BKAS*CK)
        ELSE
          H1 = HKAS
          H9 = HKAS
        ENDIF
        IF (J .GE. 8*NK) THEN 
          H2 = HKAS + (QA(J-2*NK) - QB(J-8*NK)) / (BKAS*CK)
          H8 = HKAS + (QA(J-8*NK) - QB(J-2*NK)) / (BKAS*CK)
        ELSEIF (J .GE. 2*NK) THEN 
          H2 = HKAS + QA(J-2*NK) / (BKAS*CK)
          H8 = HKAS - QB(J-2*NK) / (BKAS*CK)
        ELSE
          H2 = HKAS
          H8 = HKAS
        ENDIF
        IF (J .GE. 7*NK) THEN 
          H3 = HKAS + (QA(J-3*NK) - QB(J-7*NK)) / (BKAS*CK)
          H7 = HKAS + (QA(J-7*NK) - QB(J-3*NK)) / (BKAS*CK)
        ELSEIF (J .GE. 3*NK) THEN 
          H3 = HKAS + QA(J-3*NK) / (BKAS*CK)
          H7 = HKAS - QB(J-3*NK) / (BKAS*CK)
        ELSE
          H3 = HKAS
          H7 = HKAS
        ENDIF
        IF (J .GE. 6*NK) THEN 
          H4 = HKAS + (QA(J-4*NK) - QB(J-6*NK)) / (BKAS*CK)
          H6 = HKAS + (QA(J-6*NK) - QB(J-4*NK)) / (BKAS*CK)
        ELSEIF (J .GE. 4*NK) THEN 
          H4 = HKAS + QA(J-4*NK) / (BKAS*CK)
          H6 = HKAS - QB(J-4*NK) / (BKAS*CK)
        ELSE
          H4 = HKAS
          H6 = HKAS
        ENDIF
        IF (J .GE. 5*NK) THEN 
          H5 = HKAS + (QA(J-5*NK) - QB(J-5*NK)) / (BKAS*CK)
        ELSE
          H5 = HKAS
        ENDIF
        HB = HKAS + NB + NBT
        HW = HKI + NW
        HGEM = HKAS+(.5*HA+H1+H2+H3+H4+H5+H6+H7+H8+H9+.5*HB)/10

        QAA = QA(J) + QAT
        QBB = QB(J) + QBT

c.....berekening nadat array zijn maximum bereikt heeft
      ELSE

c.......inkomende debieten 
        QAT = QB(N-NKAS) 
        QBT = QA(N-NKAS) 
c.......inkomende golfhoogten 
        NAT = -QAT / (BKAS*CK)
        NBT =  QBT / (BKAS*CK)

c.......opschuiven gegenereerde debieten 
        DO 210 L = 1,(N-1)
        QA(L) = QA(L+1)
        QB(L) = QB(L+1)
  210 CONTINUE

        P = 0
  206 CONTINUE
        P = P + 1
c.......oude gegenereerde golfhoogten 
        NAO  =  NA
        NBO  =  NB
c.......nieuwe gegenereerde debieten 
        QA(N) = MU*BA*(HKI-ZK)*
     &           SIGN(1,(NV-NA-NAT))*SQRT(2*G*ABS(NV-NA-NAT)) - QAT
        QB(N) = -MU*BB*(HKI-ZK)*
     &           SIGN(1,(NW-NB-NBT))*SQRT(2*G*ABS(NW-NB-NBT)) - QBT
c.......nieuwe gegenereerde golfhoogten 
        NAN  =  QA(N) / (BKAS*CK)
        NBN  = -QB(N) / (BKAS*CK)
c.......gecorrigeerde gegenereerde golfhoogten 
        NA  =  (1.8*NAO+0.2*NAN)/2
        NB  =  (1.8*NBO+0.2*NBN)/2
c.......test voldoende nauwkeurige gegenereerde golfhoogten 
        IF (P . GT. 1000) GOTO 207 
        IF (ABS(NAO-NA) .GE. .001) GOTO 206 
        IF (ABS(NBO-NB) .GE. .001) GOTO 206 
  207   CONTINUE

c.....waterstanden in deurkas
        HV = HKI + NV
        HA = HKAS + NA + NAT
        IF (J .GE. 9*NK) THEN 
          H1 = HKAS + (QA(N-NK)   - QB(N-9*NK)) / (BKAS*CK)
          H9 = HKAS + (QA(N-9*NK) - QB(N-NK))   / (BKAS*CK)
        ELSEIF (J .GE. NK) THEN 
          H1 = HKAS + QA(N-NK) / (BKAS*CK)
          H9 = HKAS - QB(N-NK) / (BKAS*CK)
        ELSE
          H1 = HKAS
          H9 = HKAS
        ENDIF
        IF (J .GE. 8*NK) THEN 
          H2 = HKAS + (QA(N-2*NK) - QB(N-8*NK)) / (BKAS*CK)
          H8 = HKAS + (QA(N-8*NK) - QB(N-2*NK)) / (BKAS*CK)
        ELSEIF (J .GE. 2*NK) THEN 
          H2 = HKAS + QA(N-2*NK) / (BKAS*CK)
          H8 = HKAS - QB(N-2*NK) / (BKAS*CK)
        ELSE
          H2 = HKAS
          H8 = HKAS
        ENDIF
        IF (J .GE. 7*NK) THEN 
          H3 = HKAS + (QA(N-3*NK) - QB(N-7*NK)) / (BKAS*CK)
          H7 = HKAS + (QA(N-7*NK) - QB(N-3*NK)) / (BKAS*CK)
        ELSEIF (J .GE. 3*NK) THEN 
          H3 = HKAS + QA(N-3*NK) / (BKAS*CK)
          H7 = HKAS - QB(N-3*NK) / (BKAS*CK)
        ELSE
          H3 = HKAS
          H7 = HKAS
        ENDIF
        IF (J .GE. 6*NK) THEN 
          H4 = HKAS + (QA(N-4*NK) - QB(N-6*NK)) / (BKAS*CK)
          H6 = HKAS + (QA(N-6*NK) - QB(N-4*NK)) / (BKAS*CK)
        ELSEIF (J .GE. 4*NK) THEN 
          H4 = HKAS + QA(N-4*NK) / (BKAS*CK)
          H6 = HKAS - QB(N-4*NK) / (BKAS*CK)
        ELSE
          H4 = HKAS
          H6 = HKAS
        ENDIF
        IF (J .GE. 5*NK) THEN 
          H5 = HKAS + (QA(N-5*NK) - QB(N-5*NK)) / (BKAS*CK)
        ELSE
          H5 = HKAS
        ENDIF
        HB = HKAS + NB + NBT
        HW = HKI + NW
        HGEM = HKAS+(.5*HA+H1+H2+H3+H4+H5+H6+H7+H8+H9+.5*HB)/10

        QAA = QA(N) + QAT
        QBB = QB(N) + QBT

      ENDIF

c.....waterstand kolkzijde deur
      DTT = DTG/10
      CALL INTER (NT1,T1,N1,T-1*DTT,G1)
      CALL INTER (NT1,T1,N1,T-2*DTT,G2)
      CALL INTER (NT1,T1,N1,T-3*DTT,G3)
      CALL INTER (NT1,T1,N1,T-4*DTT,G4)
      CALL INTER (NT1,T1,N1,T-5*DTT,G5)
      CALL INTER (NT1,T1,N1,T-6*DTT,G6)
      CALL INTER (NT1,T1,N1,T-7*DTT,G7)
      CALL INTER (NT1,T1,N1,T-8*DTT,G8)
      CALL INTER (NT1,T1,N1,T-9*DTT,G9)
      GGEM  = HKI+(.5*NV+G1+G2+G3+G4+G5+G6+G7+G8+G9+.5*NW)/10 

c.....waterstand kaszijde deur
      HKAS = HKAS - MU*AO*SIGN(1,(HGEM-GGEM))*
     &           SQRT(2*G*ABS(HGEM-GGEM))/BKAS/LKAS*DT

c.....test einde berekening
      IF (T .GT. TEND) GOTO 300

c.....test einde binnenloop
      IF (K .LT. 10) THEN
        GOTO 200
      ELSE 
        K = 0
        WRITE (2,600) T,HV,HA,H5,HB,HW,HGEM,GGEM,GGEM-HGEM
        GOTO 200
      ENDIF

  300 CONTINUE

c.....TOELICHTING UITVOER
c     T = tijd [s]
c     HV = waterstand kolkzijde voor spleet A [mNAP]
c     HA = waterstand kaszijde voor spleet A [mNAP]
c     H5 = waterstand kaszijde midden kas [mNAP]
c     HB = waterstand kaszijde voor spleet B [mNAP]
c     HW = waterstand kolkzijde voor spleet B [mNAP]
c     HGEM = gemiddelde waterstand in kas tpv. de deur [mNAP]
c     GGEM = gemiddelde waterstand in kolk tpv. de deur [mNAP]
c     GGEM-HGEM = gemiddeld verval over deur [m]


  600 FORMAT (F7.3,',',8(F7.4,','))

      CLOSE (2)

      END

