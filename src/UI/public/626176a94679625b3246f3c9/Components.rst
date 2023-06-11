Components
----------

- `Excitation-contraction component <../Components/EC_uSMC.cellml>`_, including:
    - `Nernst potential computation <../cellLib/Components/Nernst_potential.cellml>`_
    - `Four-stage cross-bridge model (CB4HM) <../cellLib/Components/CB4HM.cellml>`_
    - `Ions fluxes component <../Components/J_Ca.cellml>`_
  
- `Ions fluxes component <../Components/J_Ca.cellml>`_, including:
    - L-type voltage dependent :math:`Ca^{2+}` channels :math:`J_{VOCC}`, and the computation of current reuses the imported ionic current components
    - the efflux through :math:`Ca^{2+}` pump :math:`J_{Ca,pump}`
    - the flux through the :math:`Na^{+}/Ca^{2+}` exchangers :math:`J_{Na/Ca}`
    
- `Excitation-contraction unit <../Components/Unit_uSMC.cellml>`_, which decouples the connection between the excitation and contraction. This is used to test individual ions fluxes and contraction development.
   

Each of these blocks is itself a CellML model, which enables us to reuse the various components in future studies and models.
