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
