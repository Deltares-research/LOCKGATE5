LOCKGATE2
===================================
The software LOCKGATE has a wide variety of programs that calculate forces or any other hydrodynamic effects on lock gates in various conditions, hence the name. LOCKGATE contains two sets of codes under the names LOCKGATE1 (closing or opening of lock gates subjected to flow or hydraulic head) and LOCKGATE2 (effects related to sailing ships or windwaves). This documentation specifically adresses the codes that are available within the set LOCKGATE2.

LOCKGATE2 contains the codes KASGOLF and WINDGOLF. On this page information about both codes can be found. KASGOLF is extensively discussed in this readthedocs and a user guide to get started with the code is provided. WINDGOLF will shortly be addressed at the bottom of this page. Reason is that the theory behind WINDGOLF is outdated. Therefore, theory behind this code is limited to what is shown at the bottom of this page.  

KASGOLF
========================

.. note::

   Caution! Currently, the translation of the Fortran code of KASGOLF to Python code is still under construction. That means that the code of KASGOLF is not yet ready to be openly published. This read the docs is written as if the code has been finalised and published by Deltares. The actual completion of this process is planned for the future.


##################

This is the documentation for **KASGOLF**, a 1D `Deltares <https://www.deltares.nl/>`_ tool for calculating the effect of a wave originating from a ship sailing by on an opened lock gate (when the gate is located in the gate recess (in dutch this word is 'deurkas')).  KASGOLF is able to calculate the head difference over time for a gate with vertical openings at the sides as well as for a horizontal opening underneath the door. KASGOLF was originally developed by Delft Hydraulics in 1994 as part of LOCKGATE 2 [1]. The code was converted from the original Fortran code to the currently available Python code in 2024 and contains the same functionality as version KASGOLF 1994. 

.. note::

   Many version of LOCKGATE have been created and mentioned in literature [1], [2] en [3]. LOCKGATE 2 contains a set of codes that calculates the effects of waveforces on a lock gate as a result of a passing ship or wind generated waves. Part of LOCKGATE 2 is the code KASGOLF, also refered to as 'LOCKGATE5' in [3].


##################

The KASGOLF code has been explained in the ‘Krachten op puntdeuren en enkele draaideuren’ [3] and examples of simulation results with the code are presented [1] & [3]. The code and its simulation results have never been validated with measurement data since the code has been setup to make quick estimations [2]. 

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
   getting_started
   examples
   tutorial
   code
   support

   WINDGOLF
========================
