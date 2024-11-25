.. |br| raw:: html

   <br />

.. _examples:

Example: Simple lock with schematized wave
===========
This example demonstrates the capability of the KASGOLF code by applying it to an hypothetical scenario. An overview of the lock and lockgate can be found in the figure below. The simulation starts at time t=-6.0 [s] with a time step of 0.02 [s]. A wave arrives at location A at time t=0 [s] and propagates to B with the propagation velocity of the translatory wave (M0=0) that is calculated using linear wave theory. It is assumed that there is no horizontal opening underneath the gate and the friction coefficient (:math:`\mu`) equals 0.70 [-]. 

.. image:: ../images/example_berekening.png

The result of schematizing the example lock will be generation by the code and shown in one figure. This figure shows the hydraulic head over the lock gate throughout time. The output png figure is stored in the same directory and with the same name of the input file. The output figure of the previously schematized example is shown in the figure below:

.. image:: ../images/example_uitvoer_code.png

.. note::

   As can be seen in the figure above, instability occurs in the calculated hydraulic head. This is numerical instability from the code caused by the iteration of the discharge and waterheight of the translatory wave. Later in this documentation this instability will be analysed.

##################

The input file that was used for the calculation of this example case is shown below.

.. literalinclude:: ../input/Inv_Sam_nz_OG.IN
   :language: none
   