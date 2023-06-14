Single stimulation experiment
------------------------------

In the `Single stimulation experiment <Experiments/Single_stim_experiment.cellml/view>`_, the `Excitation-contraction component <../Components/EC_uSMC.cellml>`_ is configured and parameterised with an applied `Single pulse patch clamp protocol <../cellLib/Protocols/Patch_clamp_protocol.cellml>`_. 

You can change the parameters of stimulation in the component ``Vstim_para``. 

You can also bypass the parameters in the component ``model_parameters`` and ``initial_conditions`` and define your own parameters. We defined ``control_para`` to alter some parameters such as intracellular :math:`Na^{+}` concentration for specific experiments.

The simulation experiment can be obtained by loading the `corresponding SED-ML document <../Simulation/Single_stim_experiment.sedml>`_ into OpenCOR and executing the simulation.

Control of Intracellular :math:`Ca^{2+}` Concentration
------------------------------------------------------

The experiment setting to reproduce Figure 2-4 is summarized in the following:

.. figure::  ../Simulation/table1.png
   :width: 75%
   :align: center
   :alt: table1

   Experiment setting.

Figure [#]_ shows simulations of :math:`Ca_i^{2+}` decay (in nM). A: :math:`Ca_i^{2+}` decay under inhibition of :math:`Ca^{2+}` pumps. B: :math:`Ca_i^{2+}` decay in control conditions.

.. [#]

.. figure::  ../Simulation/simFig2.png
   :width: 75%
   :align: center
   :alt: simFig2

   Simulated :math:`Ca_i^{2+}` decay (in nM).  

Figure [#]_ shows simulations of :math:`Ca_i^{2+}` rise and decay following a 200 ms voltage pulse from a holding potential of -50 mV to pulse potentials of 0 mV (A), 10 mV (B), and -10 mV (C).

.. [#]

.. figure::  ../Simulation/simFig3.png
   :width: 75%
   :align: center
   :alt: simFig3

   Simulated :math:`Ca_i^{2+}` rise and decay.

Figure [#]_ shows simulations of :math:`Ca_i^{2+}` rise and decay following a 200 ms voltage pulse from a holding potential of -50 mV to pulse potentials of -20 mV (A) and 20 mV (B).

.. [#]
   
.. figure::  ../Simulation/simFig4.png
   :width: 75%
   :align: center
   :alt: simFig4
   
   Simulated :math:`Ca_i^{2+}` rise and decay.

The experiment setting to reproduce primary Figure 5A and 5B are the same as the one used in primary Figure 2B and Figure 3A, respectively.

Figure [#]_ shows simulations of :math:`Ca^{2+}` fluxes through various :math:`Ca^{2+}` control mechanisms. Plot A shows :math:`Ca^{2+}` flux through :math:`Na^{+}/Ca^{2+}` exchangers and :math:`Ca^{2+}` pumps during :math:`Ca_i^{2+}` decay for a holding potential of -80 mV followed by a 750 ms voltage pulse to 0 mV, while plot B shows :math:`Ca^{2+}` flux through :math:`Ca^{2+}` channels and :math:`Ca^{2+}` extraction mechanisms during :math:`Ca^{2+}` rise and decay in response to a 200 ms voltage pulse to 0 mV from a holding potential of -50 mV.

.. [#]
         
.. figure::  ../Simulation/simFig5.png
   :width: 75%
   :align: center
   :alt: simFig5
         
   Simulated :math:`Ca^{2+}` fluxes through various :math:`Ca_i^{2+}` control mechanisms.         


