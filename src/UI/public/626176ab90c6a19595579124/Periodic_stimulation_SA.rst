Sensitivity analysis
--------------------------

In the `Sensitivity analysis experiment <../Experiments/Periodic_stimulation_SA.cellml>`_, the `Membrane potential component <../Components/Membrane_potential.cellml/view>`_ is configured and parameterised with an applied `periodic stimulus current <../Experiments/Periodic_IStim_protocol.cellml>`_. 

You can change the parameters of stimulation in the component ``Istim_parameters`` and the maximum conductances of ionic channels in the component ``g_parameters``. 

You can also bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Periodic_stimulation_SA.sedml>`__ into OpenCOR and executing the simulation.

Sensitivity analysis result
----------------------------

Figure [#]_ shows sensitivity analysis by 50% increase or decrease in maximum channel conductance. This evaluates the contributions of key ionic currents towards hJSMC membrane voltage. (e) shows the free intracellular :math:`Ca^{2+}` concentrations corresponding to changes in (d).

.. [#]

.. figure::  ../Simulation/simFig13.png
   :width: 85%
   :align: center
   :alt: simFig13

     


