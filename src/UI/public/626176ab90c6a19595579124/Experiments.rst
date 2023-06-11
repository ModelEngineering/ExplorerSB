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