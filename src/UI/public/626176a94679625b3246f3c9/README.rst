About this model
====================

:Original publication: `Bursztyn, Limor, et al (2007)`_:  "Mathematical model of excitation-contraction in a uterine smooth muscle cell."  American Journal of Physiology-Cell Physiology 292.5 (2007): C1816-C1829.

:DOI: https://pubmed.ncbi.nlm.nih.gov/17267547/

.. _`Bursztyn, Limor, et al (2007)`: https://pubmed.ncbi.nlm.nih.gov/17267547/

Model status
=============

The current CellML implementation runs in OpenCOR_.
The results have been validated against the data extracted from the figures in the published `Bursztyn, Limor, et al (2007)`_. We provide the settings used for the figure reproduction with the simulation results shown under ``Experiments``. The model structure can be found in the documentation of ``Components``. The curation process has been summarized in the `Model history`_ and  `Known issues`_.

Model overview
===================
This workspace holds a CellML_ encoding of the `Bursztyn, Limor, et al (2007)`_ model. 
The `Bursztyn, Limor, et al (2007)`_ paper describes three :math:`Ca^{2+}` control mechanisms: voltage-operated :math:`Ca^{2+}` channels, :math:`Ca^{2+}` pumps and :math:`Na^{+}/Ca^{2+}` exchangers, which employ the mathematical formulation proposed in `Parthimos, Dimitris et al (1999)`_. The cross-bridge model of `Hai and Murphy (1988)`_ is used to describe the processes of myosin light chain (MLC) phosphorylation and stress production, which is essentially a deterministic multi-state Markov model (MM).

.. _`Parthimos, Dimitris et al (1999)`: https://doi.org/10.1152/ajpheart.1999.277.3.H1119
.. _`Hai and Murphy (1988)`: https://doi.org/10.1152/ajpcell.1988.254.1.C99

.. figure::  Doc/model.png
   :width: 70%
   :align: center
   :alt: Schematics of the model

   A diagrammatic representation of the Bursztyn, Limor, et al (2007) model.

.. _CellML: https://www.cellml.org/

Modular description
===================

Components
----------

CellML divides the mathematical model into distinct components, which are able to be re-used.
The main CellML components are:

- `Excitation-contraction component <Components/EC_uSMC.cellml>`_, including:
    - `Nernst potential computation <cellLib/Components/Nernst_potential.cellml>`_
    - `Four-stage cross-bridge model (CB4HM) <cellLib/Components/CB4HM.cellml>`_
    - `Ions fluxes component <Components/J_Ca.cellml>`_
  
- `Ions fluxes component <Components/J_Ca.cellml>`_, including:
    - L-type voltage dependent :math:`Ca^{2+}` channels :math:`J_{VOCC}`, and the computation of current reuses the imported ionic current components
    - the efflux through :math:`Ca^{2+}` pump :math:`J_{Ca,pump}`
    - the flux through the :math:`Na^{+}/Ca^{2+}` exchangers :math:`J_{Na/Ca}`
    
- `Excitation-contraction unit <Components/Unit_uSMC.cellml>`_, which decouples the connection between the excitation and contraction. This is used to test individual ion fluxes and contraction development.
   

Each of these blocks is itself a CellML model, which enables us to reuse the various components in future studies and models.

Experiments
---------------------

Following best practices, this model separates the mathematics from the parameterisation of the model. The mathematical model is imported into a specific parameterised instance in order to perform numerical simulations. 
The parameterisation would include defining the stimulus protocol to be applied.

This workspace has seven sets of experiments and corresponding simulation results:

1. `Single stimulation experiment <Experiments/Single_stim_experiment.cellml/view>`_     
2. `Multiple stimulation experiment <Experiments/Multi_stim_experiment.cellml/view>`_   
3. `Voltage ramp experiment <Experiments/Vramp_experiment.cellml/view>`_ 
4. `Membrane potential simulation experiment <Experiments/Vm_stim_experiment.cellml/view>`_
5. `Sodium concentration experiment <Experiments/Nai_experiment.cellml/view>`_
6. `Calcium concentration experiment 1 <Experiments/Cai_experiment1.cellml/view>`_
7. `Calcium concentration experiment 2 <Experiments/Cai_experiment2.cellml>`_

Simulation settings 
-------------------
Simulation settings are encoded in SED-ML_ documents for experiment execution. It is common that we may need to vary experimental settings to obtain data under various conditions. Hence, the full experimental settings are encoded in the simulation scripts.
The Python scripts to run simulation and reproduce the figures in the original paper are included under the ``Simulation`` folder. The name of the simulation and plot scripts
indicates the Figure number in the primary paper. For example, Fig2_sim.py is used to generate the simulation data and Fig2_plot.py reproduces the graph shown in Figure 2 in the primary paper.

.. _SED-ML: http://sed-ml.org/

Model history
=================== 
There is no publicly available code for this model.

Known issues
===================

1.  During curation process, we noticed trivial typographical errors in parameter units and references in Table 3 of `Bursztyn, Limor, et al (2007)`_. Hence, we correct
these in Table 4 to remove potential confusion.
   
.. figure::  Doc/para.png
   :width: 85%
   :align: center
   :alt: Correction of primary Table 3

   Correction of primary Table 3 

2. We have summarized experiment settings along with simulation results, providing more details that were not included in the primary paper.
 
.. _OpenCOR: https://opencor.ws/

