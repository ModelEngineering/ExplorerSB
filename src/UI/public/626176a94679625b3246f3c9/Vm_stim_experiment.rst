Membrane potential simulation experiment
----------------------------------------

In the `Membrane potential simulation experiment <Experiments/Vm_stim_experiment.cellml/view>`_, the `Excitation-contraction component <../Components/EC_uSMC.cellml>`_ is configured and parameterised. The component ``Vm`` is defined to simulate a recorded human plateau potential.

You can bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Vm_stim_experiment.sedml>`_ into OpenCOR and executing the simulation.

Simulation of :math:`Ca_i^{2+}` Control and Stress Production
-------------------------------------------------------------

Figure [#]_ shows the simulation of changes in :math:`Ca_i^{2+}` and stress in response to the plateau potential :math:`V_m`.

.. [#]

.. figure::  ../Simulation/simFig12.png
   :width: 75%
   :align: center
   :alt: simFig12

            