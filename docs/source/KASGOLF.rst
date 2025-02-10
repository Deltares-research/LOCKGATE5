KASGOLF
=============  

This documentation is for **KASGOLF**, a 1D `Deltares <https://www.deltares.nl/>`_ tool for calculating the effect of a wave originating from a ship sailing past an opened lockgate (when the gate is located in the gate recess ('deurkas' in Dutch)).  KASGOLF is able to calculate the head difference over time for a gate with vertical openings at the sides as well as for a horizontal opening underneath the gate. KASGOLF was originally developed by Delft Hydraulics in 1994 as part of LOCKGATE2 [1]. The code has been converted from the original Fortran code to the currently available Python code in 2024 and contains the same functionality as version KASGOLF 1994. 

The KASGOLF code has been explained in the report ‘Krachten op puntdeuren en enkele draaideuren’ [3] and examples of simulation results from the code are presented in [1] & [3]. The code and its simulation results have not yet been validated with measurement data since the code has been setup to make quick and rough estimations [2]. 

The KASGOLF documentation covers the following topics: The theory on which KASGOLF is based, an example calculation, a tutorial for setting up a KASGOLF schematization, instructions for running KASGOLF on your computer and a sensitivity analysis on a selection of parameters.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   theory 
   getting-started
   example
   tutorial
   sensitivity-analysis
   support

##################

----------
Literature
----------
[1] WL | Delft Hydraulics (1994). ‘Krachten op puntdeuren en enkele draaideuren’ Report Q1442.

[2] WL | Delft Hydraulics (1997). ‘Sluisprogrammatuur REN’ Report Q2317.

[3] Ministerie van Verkeer en Waterstaat, Rijkswaterstaat, Bouwdienst (RWS, BD) (2000). ‘Handboek voor het ontwerpen van schutsluizen’.
