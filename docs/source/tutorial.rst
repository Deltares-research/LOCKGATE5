Tutorial
===========

This tutorial will guide you through the steps that are required to set up an input (``.in``) file. The step to use the input file for a KASGOLF simulation can be found in the  `getting started <https://lockgate5-branch2.readthedocs.io/en/latest/getting-started.html>`_ chapter of the documentation.

Defining the wave characteristics
--------------------------------

The wave enforces the change in the system, leading to hydraulic head over the lock gate. This wave is defined by two characteristics: the wave height and the wave propagation velocity. 

The wave height needs to be provided as an array that describes the height of the wave at location A (see `example <https://lockgate5-branch2.readthedocs.io/en/latest/example.html>`_) throughout time. For example, the wave heights at location V are [0.0, 0.0, -0.37, -0.37, -0.37, -0.37] at times [-20.00, 0.00, 0.02, 35.00, 35.01, 100.00]. Through linear interpolation, the wave height at times in-between two indicated moments is determined. That means that in this example the wave heights between arrival of the wave (t=0.0 [s]) and arrival of the crest (t=1.0 [s]) are determined through linear interpolation. Note that the values in the time and wave height arrays do not need to be defined at discrete intervals.

.. code-block:: none
    
    **Time array for the wave
    T1 = -20.00, 0.00, 0.02, 35.00, 35.01, 100.00
    
    **Wave height array for the wave
    N1 = 0.00, 0.00, -0.37, -0.37, -0.37, -0.37

Additionally, KASGOLF allows the user to choose between two options for the delay in the arrival of the wave in the lock chamber between location V and W. The first option calculates this delay based on the propagation velocity from shallow wave theory (M0=0), which depends on the water depth. The second option is to calculate this delay based on the sailing velocity of a ship in the lock (M0=1). In the latter case, a value needs to provided to the parameter for ship sailing velocity (VS).

.. code-block:: none

    **Choice for delay wave arrival between location V and W (translatory wave (0) or sailing velocity ship (1))
    M0 = 0

    **Sailing velocity of a ship when M0=1
    VS = 1.40  

Creating the input file
--------------------------------
The input file (``.in``) can now be created. The standard format for input files contains comments (``**``) to help the user with the set-up. A completed input file, with the examples used above, is shown below. This file can be copied and re-used to create your own schematization.

.. code-block:: none

    **###########################################################
    **Date		: 20-11-2024                                
    **Filename	: tutorial.in                                
    **Lock	    : Example                      	
    **
    **Input file for program KASGOLF version 1994.	
    **Calculation of wave driven hydraulic head over an opened lock gate.
    **
    **Remark : Lines starting with '**' are for comments. 		
    **###########################################################

    **Initial water level in gate recess (in Dutch: 'deurkas') [mNAP]
    HKI = 0.00	
    
    **Position of the lock bottom [mNAP]
    ZK = -4.00

    **Length of the lock gate at the side of the lock chamber [m]
    LKK = 10.00

    **Length of the lock gate at the side of the gate recess [m]
    LKAS = 10.00	

    **Width of the channel (section) between the wall of the gate recess and lock gate [m]
    BKAS = 1.00	

    **Width of the vertical opening between locations V and A [m]
    BA = 0.05	

    **Width of the vertical opening between locations W and B [m]
    BB = 0.50	

    **Area of the horizontal opening underneath the lock gate [m2]
    AO = 0	

    **Friction coefficient for the discharge through both vertical openings at the sides and the horizontal opening underneath the gate [-]
    MU = 0.70

    **Time step [s]
    DT = 0.02	

    **Start time of the simulation [s]
    TINIT = -6.0
    
    **End time of the simulation [s]
    TEND = 30.00

    **Choice for delay wave arrival between location V and W (translatory wave (0) or sailing velocity ship (1))
    M0 = 0

    **Sailing velocity of a ship when M0=1
    VS = 1.40

    **Time array for the wave
    T1 = -20.00, 0.00, 0.02, 35.00, 35.01, 100.00

    **Wave height array for the wave
    N1 = 0.00, 0.00, -0.37, -0.37, -0.37, -0.37

