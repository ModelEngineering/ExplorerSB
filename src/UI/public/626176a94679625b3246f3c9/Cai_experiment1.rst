Calcium concentration experiments
---------------------------------

In the `Calcium concentration experiment 1 <Experiments/Cai_experiment1.cellml/view>`_, the `Excitation-contraction unit <../Components/Unit_uSMC.cellml>`_ is configured and parameterised. The component ``Cai`` is defined to generate a :math:`Ca_i^{2+}` profile close to the measured values in Figure 9C. 

In the `Calcium concentration experiment 2 <Experiments/Cai_experiment2.cellml>`_, the `Excitation-contraction unit <../Components/Unit_uSMC.cellml>`_ is configured and parameterised. The component ``Cai`` defines a piecewise linear function to construct the input :math:`Ca_i^{2+}` for Figure 10B.

You can bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters. 

The simulation experiment can be obtained by loading the `corresponding SED-ML document Cai_experiment 1 <../Simulation/Cai_experiment1.sedml>`_ and `Cai_experiment 2 <../Simulation/Cai_experiment2.sedml>`_ into OpenCOR and executing the simulation.

MLC Phosphorylation and Stress Production by the Contracting Cell
-----------------------------------------------------------------

Figure [#]_ uses the settings in `Calcium concentration experiment 1 <Experiments/Cai_experiment1.cellml/view>`_.

.. [#]

.. figure::  ../Simulation/simFig9.png
   :width: 75%
   :align: center
   :alt: simFig9

   Simulation of MLC phosphorylation (A) and force production (B) in human nonpregnant myometrium in response to an increase in :math:`Ca_i^{2+}`.

Figure [#]_ uses the settings in `Calcium concentration experiment 2 <Experiments/Cai_experiment2.cellml>`_. 

.. [#]

.. figure::  ../Simulation/simFig10.png
   :width: 75%
   :align: center
   :alt: simFig10

   Stress development and relaxation during stretch-induced phasic contraction of human myometrium.         