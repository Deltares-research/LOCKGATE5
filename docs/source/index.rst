LOCKGATE2
===================================
The software LOCKGATE has a wide variety of programs that calculate forces or any other hydrodynamic effects on lock gates in various conditions, hence the name. LOCKGATE contains two sets of codes under the names LOCKGATE1 (closing or opening of lock gates while subjected to flow or hydraulic head) and LOCKGATE2 (effects on closed or opened gates caused by waves originating from sailing ships or wind). This documentation specifically adresses the codes that are available within the set LOCKGATE2.

LOCKGATE2 contains the codes KASGOLF and WINDGOLF. On this page information about both codes can be found. KASGOLF is extensively discussed in this readthedocs and a user guide to get started with the code is provided. WINDGOLF will shortly be addressed at the bottom of this page. Reason is that the theory behind WINDGOLF is outdated. Therefore, theory behind this code is limited to what is shown at the bottom of this page.  


.. note::

   Caution! Currently, the translation of the Fortran codes provided in this readthedocs to Python code is still under construction. That means that the codes is not yet ready to be openly published. This read the docs is written as if the code has been finalised and published by Deltares, but is not the case! The actual completion of this process is planned for the future.


##################

KASGOLF
==========

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

   KASGOLF
   wave_properties2

##################

