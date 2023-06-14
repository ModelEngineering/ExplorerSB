Sodium concentration experiment
-------------------------------

In the `Sodium concentration experiment <Experiments/Nai_experiment.cellml/view>`_, the `Excitation-contraction unit <../Components/Unit_uSMC.cellml>`_ is configured and parameterised with an applied `Single pulse patch clamp protocol <../cellLib/Protocols/Patch_clamp_protocol.cellml>`_. In addition, the component ``Nai`` is defined to generate a linear :math:`Na_i^{+}` profile from 1 mM to 46 mM. 

You can change the parameters of stimulation in the component ``Vstim_para``, while -50 mV holding voltage is used for Figure 8B.

You can also bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters. We defined ``control_para`` to alter some parameters such as :math:`Ca_i^{2+}` for this specific experiment.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Nai_experiment.sedml>`_ into OpenCOR and executing the simulation.

Sensitivity Analysis for :math:`Na_i^{+}`
------------------------------------------

Figure [#]_ A uses the settings in `Single stimulation experiment <Experiments/Single_stim_experiment.cellml/view>`_ and the values are list in the following.

.. figure::  ../Simulation/table2.png
   :width: 75%
   :align: center
   :alt: table2

   Experiment setting.

The `Sodium concentration experiment <Experiments/Nai_experiment.cellml/view>`_ is used to generate a linear :math:`Na_i^{+}` from 1 mM to 46 mM for the computation of :math:`J_{Na/Ca}` in plot B. 

.. [#]

.. figure::  ../Simulation/simFig8.png
   :width: 75%
   :align: center
   :alt: simFig8

   Sensitivity analysis for :math:`Na_i^{+}`.         