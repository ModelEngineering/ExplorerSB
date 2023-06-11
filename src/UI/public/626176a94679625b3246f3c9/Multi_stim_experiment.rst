Multiple stimulation experiment
-------------------------------

In the `Multiple stimulation experiment <Experiments/Multi_stim_experiment.cellml/view>`_, the `Excitation-contraction component <../Components/EC_uSMC.cellml>`_ is configured and parameterised with an applied `multiple pulses patch clamp protocol <../cellLib/Protocols/Patch_clamp_protocol.cellml>`_. 

You can change the parameters of stimulation in the component ``Vstim_para``. 

You can also bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters. We defined ``control_para`` to alter some parameters such as intracellular :math:`Na^{+}` concentration, inhibition of :math:`Ca^{2+}` pumps control :math:`inhPump`, for specific experiments.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Multi_stim_experiment.sedml>`_ into OpenCOR and executing the simulation.

The model reaction to a train of pulse potentials
--------------------------------------------------

We parameterise the multiple pulses patch clamp protocol to generate a train of 10 voltage pulses of 100 ms duration from a holding potential of −80 mV to a pulse potential of 0 mV, with an interval of 330 ms between the pulses.
Figure [#]_ shows the model :math:`Ca_i^{2+}` to the train of pulse potentials.

.. [#]

.. figure::  ../Simulation/simFig6.png
   :width: 75%
   :align: center
   :alt: simFig6

   Simulated model reaction to a train of pulse potentials.         

The experiment setting to reproduce Figure 2 is summarized in the following:

.. figure::  ../Simulation/table3.png
   :width: 75%
   :align: center
   :alt: table3

   Experiment setting.

Figure [#]_ shows simulations of changes in :math:`Ca_i^{2+}` and stress in response to pacing pulses. 

.. [#]
         
.. figure::  ../Simulation/simFig11.png
   :width: 75%
   :align: center
   :alt: simFig11

