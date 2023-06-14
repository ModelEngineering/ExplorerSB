Voltage ramp experiment
--------------------------

In the `Voltage ramp experiment <Experiments/Vramp_experiment.cellml/view>`_, the `Excitation-contraction unit <../Components/Unit_uSMC.cellml>`_ is configured and parameterised with an applied `voltage ramp protocol <../cellLib/Protocols/Patch_clamp_protocol.cellml>`_. 

You can change the parameters of stimulation in the component ``Vstim_para``, while the ramp voltage signal has 1 mV/s rising rate and the range of variation is from -100 mv to 60 mV in the following simulation.

You can also bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters. We defined ``control_para`` to alter some parameters such as :math:`K_{Ca,1/2}` for this specific experiment.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Vramp_experiment.sedml>`_ into OpenCOR and executing the simulation.

Sensitivity Analysis for :math:`K_{Ca,1/2}`
-------------------------------------------

Figure [#]_ A uses the configurations in `Single stimulation experiment <Experiments/Single_stim_experiment.cellml/view>`_ and the experiment settings are listed in the following.

.. figure::  ../Simulation/table2.png
   :width: 75%
   :align: center
   :alt: table2

   Experiment setting.

The `Voltage ramp experiment <Experiments/Vramp_experiment.cellml/view>`_ is used to provide a voltage ramp ranging from -100 mv to 60 mV to compute the activation function in plot B. 

.. [#]

.. figure::  ../Simulation/simFig7.png
   :width: 75%
   :align: center
   :alt: simFig7

   Sensitivity analysis for :math:`K_{Ca,1/2}`.         