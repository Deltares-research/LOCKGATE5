KASGOLF
---------  

**KASGOLF** is a 1D `Deltares <https://www.deltares.nl/>`_ tool for calculating the effect of a wave originating from a ship sailing by on an opened lock gate (when the gate is located in the gate recess (in dutch this word is 'deurkas')).  KASGOLF is able to calculate the head difference over time for a gate with vertical openings at the sides as well as for a horizontal opening underneath the gate. KASGOLF was originally developed by Delft Hydraulics in 1994 as part of LOCKGATE2 [1]. The code has been converted from the original Fortran code to the currently available Python code in 2024 and contains the same functionality as version KASGOLF 1994. 

The KASGOLF code has been explained in the report ‘Krachten op puntdeuren en enkele draaideuren’ [3] and examples of simulation results from the code are presented [1] & [3]. The code and its simulation results have never been validated with measurement data since the code has been setup to make quick and rough estimations [2]. 

The KASGOLF documentation covers the following topics:
1. The theory on which KASGOLF is based,
2. An example calculation,
3. A tutorial for setting up a KASGOLF schematization,
4. Instructions for running KASGOLF on your computer,
5. An overview of the Python code and the functionality of each subroutine.
6. A sensitivity analysis that investigates the response of the simulation result to adjustments in a selection of parameters

Literature
----------
[1] WL | Delft Hydraulics (1994). ‘Krachten op puntdeuren en enkele draaideuren’ Report Q1442.
[2] WL | Delft Hydraulics (1997). ‘Sluisprogrammatuur REN’ Report Q2317.
[3] Ministerie van Verkeer en Waterstaat, Rijkswaterstaat, Bouwdienst (RWS, BD) (2000). ‘Handboek voor het ontwerpen van schutsluizen’.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   theory 
   getting-started
   example
   tutorial
   code
   sensitivity-analysis
   support

##################