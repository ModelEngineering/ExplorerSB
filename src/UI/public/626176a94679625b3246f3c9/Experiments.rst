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