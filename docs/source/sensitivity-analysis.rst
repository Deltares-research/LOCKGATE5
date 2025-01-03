Sensitivity Analysis
===========
In this sensitivity analysis, parameters in the model are varied with respect to the example calculation in `example <https://lockgate5-branch2.readthedocs.io/en/latest/example.html>`_ which includes a negative wave from the drop in water level alongside a ship that exits a lock. The input file for this simulation has been presented in `tutorial <https://lockgate5-branch2.readthedocs.io/en/latest/tutorial>`.

The use of sailing velocity (M0=0)
--------------------------------
As mentioned in `getting started <https://lockgate5-branch2.readthedocs.io/en/latest/theory.html>`_, the user can choose to define the propagation velocity of the wave in the lock according to the shallow wave theory (M0=0 with c = +/- 6.27 [m/s]). Note that a negative wave (as used in this example) caused by a ship always propagates with the velocity of the ship and that this calculation is hypothetical to indicate the effect of this parameter.

.. image:: ../images/Test_1.png

As can be seen in the figure, for a propagation velocity of the wave in the lock chamber based on linear wave theory (equal to that in the gate recess) results in a significantly different shape. The peak negative head difference occurs earlier since the wave in the lock chamber reaches the second vertical opening at location W earlier. The peak itself is lowered since the translatory waves in the lock chamber and gate recess meet at location B. This is similar for the positive head difference peak. The numerical instability occurs at an earlier time step.

Spacing between gate and gate recess wall
--------------------------------

A space is present between the gate and gate recess wall, referred to as 'channel'. The width of this channel is varied and the result is shown in the figure below.

.. image:: ../images/Test_2.png

As the figure shows, reducing the width of the channel increases the influence of the numerical instability and causes the instability to occur earlier in the simulation (even before the wave in the lock chamber reaches the second vertical opening at location W). This effect is reduced for a wider channel and therefore seems to be less sensitive.

Width of the vertical opening 
--------------------------------

Two vertical openings are present on the sides of the gate, which can differ in spacing. In the figure below, the spacing of the vertical opening at location A (BA, the first that is reached by the incoming wave) is varied.

.. image:: ../images/Test_3.png

From the figure it can be seen that the head difference is highly sensitive to the width of the opening at A (BA). A wider channel results in faster response of the waterlevel in the channel creating a positive peak in head difference immediatly after the wave arrives at location A. As a result, the negative peak is reduced. For the simulation in which BA (=0.70 [m]) exceeds BB (=0.50 [m]) a positive peak forms after the negative peak, whereas this is not the case for the simulation with BA=0.30 [m]. The numerical instability does not seem to have a clear relation to BA.

Horizontal opening underneath the gate
--------------------------------

In addition to vertical openings at the sides of the gate, also a horizontal opening can be present underneath the gate. This variable is given as the area of this opening (AO) in [m2]. In previous runs, no horizontal opening was present. In the figure below this opening is implemented with varying area.

.. image:: ../images/Test_4.png

As can be seen in the figure, response in head difference is somewhat different when a horizontal gap is present. This is related to the response of the waterlevel in the gate recess. Additionally, an opening underneath the gate lowers the extremes in head difference, which is strongest for the negative head difference. The numerical instability seems to occur at the same moment in time during the simulation.

Different wave shape
--------------------------------

In previous examples, a wave is used that is described as an instant change in waterlevel (within 1 timestep). In reality a wave has a smoother profile. The figure below shows the original steep wave profile and a smoother configuration. Note that the time span on the x-axis is altered compared to other figures. The second figure shows the head difference as calculated with this smoother wave (for result of the steep wave, see the blue line in the first figure).

.. image:: ../images/Test_6_golf.png

.. image:: ../images/Test_6.png

As can be seen in the second figure above, the head difference output graph shows a smoother response. However, the extremes show similar values indicating that an instant wave can be used for this purpose. 