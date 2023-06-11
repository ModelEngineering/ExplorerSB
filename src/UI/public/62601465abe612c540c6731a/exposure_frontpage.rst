About this model
====================

This is a bond-graph model of beta-1 adrenergic receptor ( :math:`{\beta}`-1AR) metabolism in the cardiac cell.

    **INPUTS:** 
        - Ligand (L) stimulus e.g. isoproterenol 
        
    **OUTPUTS:** 
        - Change in molar amount of :math:`{\beta}`-1AR (R), 
        
    **REACTIONS:** 
        - Phosphorylation of :math:`{\beta}`-1AR by :math:`{\beta}`-ARK, producing :math:`{\beta}`-1AR\ :sub:`d`\
        - Phosphorylation of :math:`{\beta}`-1AR by PKACI, producing :math:`{\beta}`-1AR\ :sub:`p`\
        

Model status
=============

The current CellML implementation runs in OpenCOR.


Model overview
===================
This model is made by from an existing kinetic model, where the mathematics are translated into the bond-graph formalism. This describes the model in energetic terms and forces adherence to the laws of thermodynamics.

The creation of the composite LR and LRG species are not included in this module. See the `module for L, R, and G binding for these. <https://models.physiomeproject.org/workspace/6f7>`_

For the following figures, all enzymes are shown in maroon.

.. figure:: exposure/kinetic_reactions.png
   :width: 100%
   :align: center
   :alt: Original kinetic formulations

   Fig. 1. Original kinetic formulations.


|

.. figure:: exposure/BG_BARK_reaction.png
   :width: 100%
   :align: center
   :alt: BG BARK reaction
   
   Fig. 2. Bond-graph formulation of the reaction involving  the :math:`{\beta}`-ARK enzyme, in the phosphorylation of :math:`{\beta}`-1AR (Figure 1, left). The :math:`{\beta}`-ARK enzyme was added as both a reactant and product to the original reaction, to show the fependence of the reaction rate on its concentration.


|

.. figure:: exposure/BG_PKACI_reaction.png
   :width: 100%
   :align: center
   :alt: BG PKACI reaction
   
   Fig. 3. Bond-graph formulation of the reaction involving the PKACI enzyme, in the phosphorylation of :math:`{\beta}`-1AR at another site to the :math:`{\beta}`-ARK enzyme (Figure 1, right).


|

For the above bond-graphs, a '0' node refers to a junction where all chemical potentials are the same. A '1' node refers to all fluxes being the same going in and out of the junction.

Parameter finding
~~~~~~~~~~~~~~~~~
A description of the process to find bond-graph parameters is shown in the folder    `parameter_finder <parameter_finder>`_, which relies on the:

1. stoichiometry of system

2. kinetic constants for forward/reverse reactions

  - If not already, all reactions are made reversible by assigning a small value to the reverse  direction.
  
3. `linear algebra script <https://models.physiomeproject.org/workspace/6ba/file/c32be022513dc4b620d74803a6ace6ca2d817e11/parameter_finder/find_BG_parameters.py>`_. 

Here, this solve process is performed in Python.


Original kinetic model
======================
Saucerman et al: `Modeling beta-adrenergic control of cardiac myocyte contractility in silico. <https://models.physiomeproject.org/exposure/9766d9bd0325c31e47a31b291e26ccad>`_

