Voltage clamp experiment
------------------------

In the `Voltage clamp experiment <../Experiments/Patch_clampXi_experiment.cellml>`_, the `Clamped current component <../Components/Clamped_current_Xi.cellml/view>`_ is configured and parameterised with an applied `Patch clamp protocol <../Experiments/Patch_clamp_protocol.cellml>`_. 

You can change the clamping parameters in the component ``Clamp_parameters``. 

You can also bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Patch_clampXi_experiment.sedml>`__ into OpenCOR and executing the simulation.

Clamped :math:`I_{CaL}`
-------------------------

Figure [#]_ shows normalized L-type calcium channels peak I–V plot for simulated data derived from the publication (dots) and the current CellML model (solid line) with different intracelluar concentrations.

.. [#]

.. figure::  ../Simulation/simFig2.png
   :width: 85%
   :align: center
   :alt: simFig2

Clamped :math:`I_{CaT}`
-------------------------
   
Figure [#]_ shows normalized T-type calcium channels peak I–V plot for simulated data derived from the publication (dots) and the current CellML model (solid line) with different intracelluar concentrations.
   
.. [#]
   
.. figure::  ../Simulation/simFig3.png
      :width: 85%
      :align: center
      :alt: simFig3

Clamped :math:`I_{Kv}`
-------------------------

Figure [#]_ shows normalized I–V plot of whole cell voltage-activated potassium currents for simulated data derived from the publication (dots) and the current CellML model (solid line).

.. [#]

.. figure::  ../Simulation/simFig4.png
   :width: 85%
   :align: center
   :alt: simFig4     

Clamped :math:`P_{BK}`
-------------------------

Figure [#]_ shows Open probability of BK channel versus clamping voltage (@ various :math:`Ca_i^{2+}`) for simulated data derived from the publication (dots) and the current CellML model (solid line).

.. [#]

.. figure::  ../Simulation/simFig5.png
   :width: 85%
   :align: center
   :alt: simFig5

Clamped :math:`I_{Na}`
-------------------------

Figure [#]_ shows normalized :math:`Na_^{+}` channel peak I–V plot for simulated data derived from the publication (dots) and the current CellML model (solid line) with different intracelluar concentrations.

.. [#]

.. figure::  ../Simulation/simFig6.png
   :width: 85%
   :align: center
   :alt: simFig6
   
Figure [#]_ shows whole cell current versus time traces subjected to voltage clamp at different holding voltages for simulated data derived from the publication (dots) and the current CellML model (solid line).

.. [#]

.. figure::  ../Simulation/simFig10.png
   :width: 85%
   :align: center
   :alt: simFig10
   
Figure [#]_ shows whole cell normalized I–V data from hJSMC model under near calcium-free conditions for simulated data derived from the publication (dots) and the current CellML model (solid line).

.. [#]

.. figure::  ../Simulation/simFig11.png
   :width: 85%
   :align: center
   :alt: simFig11
   