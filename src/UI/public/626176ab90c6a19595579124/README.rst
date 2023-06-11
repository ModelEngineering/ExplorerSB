About this model
====================

:Original publication: `Poh, Yong Cheng, et al (2012)`_:  "A quantitative model of human jejunal smooth muscle cell electrophysiology." PloS one 7.8 (2012): e42385.

:DOI: https://doi.org/10.1371/journal.pone.0042385

.. _`Poh, Yong Cheng, et al (2012)`: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0042385

Model status
=============

The current CellML model implementation runs in OpenCOR_.
The results have been validated against the data extracted from the figures in the published `Poh, Yong Cheng, et al (2012)`_. Using the default parameters provided in the paper except for the modification listed in the following sections, Figure 4, 5, 8, 9, 13 can be reproduced with marginal difference, while the difference becomes significant at less negative clamping voltages in Figure 2, 3, and 6. By increasing the intracellular concentrations, we have got better simulated IV curves, however, the specific experiment settings cannot be confirmed by the authors. For the same reason, there is a discrepancy in Figiure 10.

The model structure can be found in the documentation of ``Components``, while the  simulation results are shown under ``Experiments``. The limitation and curation process has been summarized in the `Model history`_ and  `Known issues`_.

Model overview
===================
This workspace holds a CellML_ encoding of the `Poh, Yong Cheng, et al (2012)`_ model. 
The `Poh, Yong Cheng, et al (2012)`_ paper describes the first biophysically based computational model of human jejunal SMC (hJSMC) electrophysiology. 
It includes nine types of ion channels and transporters, while the ionic currents are described by either a traditional Hodgkin-Huxley (HH) formalism or a deterministic multi-state Markov (MM) formalism.

.. figure::  Doc/schematics.png
   :width: 85%
   :align: center
   :alt: Schematics of the model

   A diagrammatic representation of the Poh, Yong Cheng, et al (2012) model.

.. _CellML: https://www.cellml.org/

Modular description
===================

Components
----------

CellML divides the mathematical model into distinct components, which are able to be re-used.
The main CellML components are:

- `Membrane potential component <Components/Membrane_potential.cellml/view>`_
  
- `Clamped current component <Components/Clamped_current_Xi.cellml/view>`_ (the ionic current during a voltage clamp)
    
- `Ionic currents component <Components/Ionic_currents.cellml>`_, a single definition instantiated for: 
    - L-type :math:`Ca^{2+}` channels: `ICaL <Components/ICaL.cellml>`_
    - T-type :math:`Ca^{2+}` channels: `ICaT <Components/ICaT.cellml>`_
    - Voltage dependent :math:`K^{+}` channels: `IKv <Components/IKv.cellml>`_
    - Large conductance :math:`Ca^{2+}` and voltage activated :math:`K^{+}` channels: `IBK <Components/IBK.cellml>`_
    - :math:`Na^{+}` channels: `INa <Components/INa.cellml>`_

- The rest of currents are defined separately:
    - :math:`Na^{+}`- :math:`K^{+}` pump: `INaK <Components/INaK.cellml>`_
    - :math:`Na^{+}`- :math:`Ca^{2+}` exchanger: `INCX <Components/INCX.cellml>`_
    - Non-selective leak current (sodium and potassium): `INS_Na <Components/INS_Na.cellml>`_ and `INS_K <Components/INS_K.cellml>`_

- `Ionic concentrations component <Components/Ionic_concentrations.cellml>`_ for :math:`Ca_i^{2+}`, :math:`Na_i^{+}` and :math:`K_i^{+}` 
    
- `Gating kinetics component <Components/gating_kinetics.cellml>`_ – a single definition instantiated for the d, f, x, and y gates
  
- Channel states for the MM formalism of IBK, INa and ICaL
  
- `Nernst potential component <Components/Nernst_potential.cellml>`_, a single definition instantiated for `Na, Ca2+ and K <Components/E_Nernst.cellml>`_
  
- `Temperature component <Components/temperature_factor.cellml/view>`_
  
- `Time component <Components/time.cellml/view>`_ 

Each of these blocks is itself a CellML model, which enables us to reuse the various components in future studies and models.

Experiments
---------------------

Following best practices, this model separates the mathematics from the parameterisation of the model. The mathematical model is imported into a specific parameterised instance in order to perform numerical simulations. 
The parameterisation would include defining the stimulus protocol to be applied.

This workspace has three sets of experiments and corresponding simulation results:

1. `Periodic stimulation experiment <Experiments/Periodic_stimulation.cellml/view>`_     

2. `Voltage clamp experiment <Experiments/Patch_clampXi_experiment.cellml/view>`_ 
   
3. `Sensitivity analysis experiment <Experiments/Periodic_stimulation_SA.cellml/view>`_ 

Simulation settings 
-------------------
Simulation settings are encoded in SED-ML_ documents for experiment execution. 
The python scripts to run simulation and reproduce the figures in the original paper are also included.

.. _SED-ML: http://sed-ml.org/

Model history
=================== 

The original model implementation is from `A Quantitative Model of Human Jejunal Smooth Muscle Cell Electrophysiology`_ encoded in CellML by Yong Cheng Poh. The main modification is summarized as follows:

1. Modularize the CellML model for reusability.
   
2. Add  `Clamped current component`_,  `Patch clamp protocol <Experiments/Patch_clamp_protocol.cellml>`_ and `Voltage clamp experiment`_ to simulate a membrane current during a voltage clamp.

3. Modify `Periodic IStim protocol <Experiments/Periodic_IStim_protocol.cellml>`_  and `Periodic stimulation experiment`_ to enable the periodic stimulation for Figure 8. 
   
4. Modify a few parameters based on the author provided `C code`_ to reproduce the figures in the original paper. (please see `Known issues`_).   
   
5. Modify some equations according to the author provided CellML code to reproduce the figures in the original paper. (please see `Known issues`_).

6. Add the python scripts to run simulation and reproduce the figures in the original paper.   

.. _`A Quantitative Model of Human Jejunal Smooth Muscle Cell Electrophysiology`: https://models.physiomeproject.org/w/yc_poh/poh_2012

.. _`C code`: https://computationalbiolab.github.io/jejunal_smc_model/

Known issues
===================

1.  The parameters :math:`P_{NCX}=1992.1865`, :math:`P_{NaK}=16.197`, :math:`\tau_{dCat}=1.9508` and :math:`0.005956`  in Eq(S-24) are different from the values provided in the supplemental materials of the paper.
   
2.  The equations (S-5, S-6, S-7) have been multiplied by :math:`1e-15` for unit conversion.
   
3.  The equations (S-13, S-14), (S-23,..., S-28), (S-36, S-37), (S-43, S-44), and (S-80,..., S-91) have been multiplied by corresponding temperature factors. The reference temperature for :math:`I_{CaL}` is :math:`310` K, while :math:`I_{CaT}` is constructed based on :math:`297` K. The reference temperatures for other currents are :math:`297` K.
   
4.  The intracellular :math:`Ca^{2+}` concentrations terms have been removed from the equations (S-67,..., S-70) and (S-75,..., S-78).
   
5.  For voltage clamp experiments, as the clamping values for intracellular concentrations of :math:`Ca_i^{2+}`, :math:`Na_i^{+}` and :math:`K_i^{+}` were not specified in the paper, we use the initial values that the author used in their CellML model.
    
6.  For clamped :math:`I_{CaL}` in Figure 2, the :math:`\theta` and :math:`\delta` are set to :math:`0` to switch off the :math:`Ca_i^{2+}` dependency.
   
7.  The holding voltage for Figure 4 was not specified, and we use :math:`-70` mV.
   
8.  Using the default parameters provided in the paper except for the above modification, Figure 4, 5, 8, 9, 13 can be reproduced with marginal difference, while the difference becomes significant at less negative clamping voltages in Figure 2, 3, and 6. By increasing the intracellular concentrations, we have got better simulated IV curves, however, the specific experiment settings cannot be confirmed by the authors. For the same reason, there is a discrepancy in Figiure 10.

9.  The partial notations in the mathematical equations of state transitions for :math:`I_{CaL}` are different from the ones in `the referenced paper <https://doi.org/10.1529/biophysj.106.088807>`_.

.. _OpenCOR: https://opencor.ws/

