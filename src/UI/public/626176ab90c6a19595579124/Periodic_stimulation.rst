Periodic stimulation
--------------------------

In the `periodic stimulation experiment <../Experiments/Periodic_stimulation.cellml>`_, the `Membrane potential component <../Components/Membrane_potential.cellml/view>`_ is configured and parameterised with an applied `periodic stimulus current <../Experiments/Periodic_IStim_protocol.cellml>`_. 

You can change the parameters of stimulation in the component ``Istim_parameters``. The following simulation uses 310K for the temperature setting.

You can also bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Periodic_stimulation.sedml>`__ into OpenCOR and executing the simulation.

Membrane action potential
-------------------------

Figure [#]_ shows the simulated hJSMC action potential trace and free intracellular calcium concentration after a simulation of 30 minutes of electrical activity (@ 6 cpm).

.. [#]

.. figure::  ../Simulation/simFig8.png
   :width: 85%
   :align: center
   :alt: simFig8

   Simulated hJSMC action potentials after a simulation of 30 minutes of electrical activity and free intracellular calcium concentration.  

Figure [#]_ shows the simulated hJSMC action potential trace after a simulation of 30 minutes of electrical activity (@ 7.5 cpm). Note: ICC stimulus were modified.

.. [#]

.. figure::  ../Simulation/simFig9.png
   :width: 85%
   :align: center
   :alt: simFig9

   Simulated hJSMC action potentials after a simulation of 30 minutes of electrical activity (@ 7.5 cpm).


