

This model is a simplified "0D" version of the 3D electromechanical cardiac model described in [Marchesseau, S. et al.] (1) and developed at **Inria Sophia Antipolis - Asclepios Team** (2). 

It describes the mechanical behavior of a single heart ventricle, based on the Bestel-Clement-Sorine model of myocardial tissue as described in [Chapelle et al.] (3) and the Mooney-Rivlin (4) strain energy for passive elasticity. Hemodynamics are represented through global values of pressures and flows in the ventricular chambers. The mechanical equations are coupled to the 3-element Windkessel model (5) for the after-load. Finally, cardiac pre-load is modeled by a (prescribed) varying atrial pressure with a "pressure bump" at the beginning of the cardiac cycle, to account for atrial contraction.

Some features related to the dynamics of a heart valve are currently relying on an unorthodox CellML (6) implementation (**HOD.cellml**). Thus, to run this model in *OpenCOR* (7), specific **ODE solver** settings are needed:

 - **Name:** `Euler (forward)`; and

 - **Step:** `1e-05 second`.

For the simulation itself, we recommend using the following settings, which are used to compute 3 heartbeats:

 - **Starting point:** `0 second`;

 - **Ending point:** `2.4 second`; and

 - **Point interval:** `0.001 second`.

Finally, for the output, we recommend creating 3 graph panels to, respectively, plot the following graphs:

 - **Volume curve:** `V_mL` against the *variable of integration*;

 - **Ventricular, atrial and aortic pressure curves:** `P_v`, `P_at` and `P_ar` against the *variable of integration*; and

 - **Pressure-volume curve:** `P_v` against `V_mL`.

This exposure also comes with both a SED-ML (7) file (**HOD.sedml**) and a COMBINE archive (8) file (**HOD.omex**). They contain exactly this configuration and can be readily opened and run using OpenCOR 0.5 (available at http://www.opencor.ws/downloads).

**Contact:** Roch Molléro at rochmollero@hotmail.com.

 - 1 / http://link.springer.com/article/10.1007/s10237-012-0446-z
 - 2 / https://team.inria.fr/asclepios/
 - 3 / https://hal.inria.fr/hal-00678772/document
 - 4 / https://en.wikipedia.org/wiki/Mooney%E2%80%93Rivlin_solid
 - 5 / http://www.sciencedirect.com/science/article/pii/0021929069900244
 - 6 / https://www.cellml.org/
 - 7 / http://journal.frontiersin.org/article/10.3389/fphys.2015.00026/full
 - 8 / http://bmcsystbiol.biomedcentral.com/articles/10.1186/1752-0509-5-198
 - 9 / https://www.ncbi.nlm.nih.gov/pubmed/25494900
