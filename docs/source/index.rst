LOCKGATE
===================================

This is the documentation for **KASGOLF**, a 1D `Deltares <https://www.deltares.nl/>`_ tool for calculating the head difference over an opened lock gate (when the gate is located in the gate recess).  KASGOLF is able to calculate the head difference over time for a gate with vertical openings at the sides as well as for a horizontal opening underneath the door. KASGOLF was originally developed by Delft Hydraulics in 1994 as part of LOCKGATE 2 [1]. The code was converted from the original Fortran code to the currently available Python code in 2024 and contains the same functionality as version KASGOLF 1994. 

.. note::

   Many version of LOCKGATE have been created and mentioned in literature [1], [2] en [3]. LOCKGATE 2 contains a set of codes that calculates the waveforces on a lock gate. Part of LOCKGATE 2 is the code KASGOLF, also refered to as LOCKGATE5 in [3].


##################

The KASGOLF code has been mentioned in the ‘Krachten op puntdeuren en enkele draaideuren’ [3] and examples of calculation results are shared [1] & [3]. Eventhough, the code has never been validated with measurement data [2]. 

The KASGOLF documentation covers the following topics:
1. The theory on which KASGOLF is based,
2. An example calculation,
3. A tutorial for setting up a KASGOLF schematization,
4. Instructions for running KASGOLF on your computer,
5. An overview of the Python code and the functionality of each subroutine.

Literature
-----------
[1] WL | Delft Hydraulics (1994). ‘Krachten op puntdeuren en enkele draaideuren’ Report Q1442.
[2] WL | Delft Hydraulics (1997). ‘Sluisprogrammatuur REN’ Report Q2317.
[3] Ministerie van Verkeer en Waterstaat, Rijkswaterstaat, Bouwdienst (RWS, BD) (2000). ‘Handboek voor het ontwerpen van schutsluizen’.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   theory 
   getting-started
   examples
   tutorial
   code
   support