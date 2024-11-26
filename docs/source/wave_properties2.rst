WINDGOLF
===========================  
This documentation describes the files present in windgolf and focuses on the program G75.

Fortran Files
------------------------------------

- **WGOLF.FOR**:
  
  - Computes wave periods (Ts) for various combinations of water depths and wave lengths.
  - Based on the 1975 Shore Protection Manual.

- **SIG.FOR**:

  - Calculates wave heights (Hg) and periods (Ts) for different depths, wind speeds, and fetch lengths.
  - Based on the 1975 Shore Protection Manual.

- **SIT.FOR**:

  - Determines the time required to reach the maximum wave height.
  - Based on the 1975 Shore Protection Manual.

- **SIH.FOR**:

  - Computes wave heights (Hg) and periods (Ts) for different depths, wind speeds, and fetch lengths.
  - Based on the 1984 Shore Protection Manual.

- **BREEK.FOR**:

  - Models wave breaking relationships using a hyperbolic tangent function and writes results to a file.

- **G50.FOR**:

  - Calculates wave properties and the forces acting on the wave.
  - Developed on June 18, 1991.

- **G60.FOR**:

  - Iteratively determines wave lengths within the code.
  - Developed on July 12, 1991.

- **G70.FOR**:

  - Introduces coefficients for wave troughs (golfdal) and crests (golftop).
  - Iterates over user-defined ranges of wave heights (Hg) and periods (Ts).
  - Developed on July 12, 1993.

- **G75.FOR**:

  - Includes a new formula to calculate hydrostatic forces.
  - Developed on July 12, 1993.

.. note::
   The following documentation focuses on explaining the code and methodology used in **G75.FOR** as this is assumed to be the most recent code developed in this collection.




The wave properties calculation process implemented in the `G75.py` program to calculate the Quasi-static loads against a vertical wall. his program is based on the G75.FOR program developed by A. Vrijburcht (1993).
The program reads input data from a specified file, performs various wave-related calculations, and writes the results to an output file. The calculation involves determining wave heights, mean water levels, pressures, and forces using linear wave theory and hydrostatic pressure formulations.

Function Overview
-----------------  
The `G75` program calculates wave properties based on input parameters provided in an input file. It reads data, performs the calculations, and saves the results to an output file.

Input parameters
^^^^^^^^^^  
- `fileName`: The name of the input file (without extension). The input file should be in the current directory with a `.IN` extension.

The function expects the input file (`<fileName>.IN`) to follow a specific order of the input parameters, structured as follows:

**Row 1**: ID

**Row 2**: :math:`H_g`, :math:`T_s`

**Row 3**: :math:`C_r`, :math:`C_n`, :math:`h_m`, :math:`h_b`, :math:`h_d`

where:

- **Identifier (ID)** : Identifier string for the data set.

- **Wave Height** (:math:`H_g`): Initial wave height (in meters).

- **Wave Period** (:math:`T_s`): Wave period (in seconds).

- **Reflection Coefficient** (:math:`C_r`): Reflection coefficient (taken as 1.0 for vertical walls).

- **Coefficient for Elevated Mean Water Level** (:math:`C_n`): Coefficient for elevated mean water level.

- **Mean Water Level** (:math:`h_m`): Mean water level before wave reflection, relative to NAP.

- **Bed Level** (:math:`h_b`): Bed level, relative to NAP.

- **Top of the Door Level** (:math:`h_d`): The top level of the door is positioned, relative to NAP.


Formulas Used
-------------  
The following formulas are applied in the calculations:

1. **Wave Height (reflected wave)**:
   
   .. math::
       H_{rr} = (1 + C_r) \cdot H_g

2. **Mean Water Level (reflected wave)**:

   .. math::
       h_r = h_m + C_n \cdot H_g


3. **Water depth after wave reflection**:

   .. math::
       d_r = h_r - h_b



4. **Wave length calculation**:
   
   Iteratively calculated using:


   .. math::
       L_{g} = \frac{g \cdot T_s^2}{2 \pi} \cdot \tanh \left( \frac{2 \pi \cdot d_r}{L_{go}} \right)


5. **Wave number**:

   .. math::
       m = \frac{2 \pi}{L_g}

6. **Wave number adjusted for depth**:

   .. math::
       k = \sqrt{g \cdot m \cdot \tanh(m \cdot d_r)}

7. **Pressure calculations for linear wave theory**:
   
   The pressures at different depths (z) are calculated in each time iteration step :math:`(i)` as:


   .. math::
       p_{} = -\rho \cdot g \cdot z - \rho \cdot g \cdot \frac{H_{rr}}{2} \cdot \frac{\cosh(m \cdot (d_r + z))}{\cosh(m \cdot d_r)} \cdot \cos(k \cdot t)





8. **Hydrostatic pressure calculation**:

   .. math::
       ph_{} = -\rho \cdot g \cdot z - \rho \cdot g \cdot \frac{H_{rr}}{2} \cdot \cos(k \cdot t)

9.  **Force calculations by linear wave theory**:
   The force by linear wave theory is calculated in each iteration step :math:`(i)` as follows:


   .. math::
       F_{h} = \frac{p_{r}}{2} \cdot (h_{o} - h_r) + \frac{p_{r} + p_{2}}{2} \cdot (h_r - h_{2}) \
       + \frac{p_{2} + p_{3}}{2} \cdot (h_{2} - h_{3}) + \frac{p_{3} + p_{4}}{2} \cdot (h_{3} - h_{4}) \
       + \frac{p_{4} + p_{5}}{2} \cdot (h_{4} - h_{5}) + \frac{p_{5} + p_b}{2} \cdot (h_{5} - h_b)

   
10. **Hydrostatic force calculation**:
    The hydrostatic force is calculated as:
    
    .. math::
        F_{hh} = 0.5 \cdot \rho \cdot g \cdot d_r^2


Definitions of Parameters
-------------------------  
- :math:`\rho`: Water density (kg/m³).  
- :math:`g`: Gravitational acceleration (9.81 m/s²).  
- :math:`\pi`: Mathematical constant.  
- :math:`C_r`: Reflection coefficient.  
- :math:`C_n`: Coefficient for elevated mean water level.  
- :math:`h_m`: Mean water level before reflection (relative to NAP).  
- :math:`h_b`: Bed level (relative to NAP).  
- :math:`h_d`: Level of the top of the door (relative to NAP).  
- :math:`H_g`: Initial wave height (m).  
- :math:`T_s`: Wave period (s).  
- :math:`h_r`: Adjusted water level (m).  
- :math:`d_r`: Water depth after wave reflection (m).  
- :math:`z, z_1, z_2, z_3, z_4, z_5, z_b, z_d`: Various depth levels used in calculations (m).  
- :math:`L_{go}, L_g`: Initial and adjusted wave lengths (m).  
- :math:`m`: Wave number (1/m).  
- :math:`k`: Wave number adjusted for depth (1/m).  
- :math:`t`: Time (s).  
- :math:`\eta`: Wave elevation (m).  
- :math:`h_o`: Water surface elevation (m).  
- :math:`z_o`: Wave elevation at the surface (m).  
- :math:`p_r, p_2, p_3, p_4, p_5, p_b, p_d`: Pressures at various depths (Pa).  
- :math:`ph_r, ph_2, ph_3, ph_4, ph_5, ph_b, ph_d`: Hydrostatic pressures at various depths (Pa).  
- :math:`F_h`: Force by linear wave theory (N).  
- :math:`F_{hh}`: Hydrostatic force (N).  
- :math:`c_1, c_2`: Coefficients calculated for output.  

Output
-------------------------

The program saves results in an output file with the extension `.OUT`. Each row corresponds to a combination of wave height (:math:`H_g`) and wave period (:math:`T_s`) with the following columns:

:math:`H_{rr}/(g \cdot T_s^2)`, :math:`c_1`, :math:`c_2`, :math:`H_{rr}/d_r`, 

Example Output
-------------------------
The values below are the first row from the code output using the default values.

.. code-block:: text

    0.02548, 0.99564, 1.00537, 0.05000