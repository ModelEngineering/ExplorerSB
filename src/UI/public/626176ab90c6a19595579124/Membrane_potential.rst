Membrane potential model
------------------------

The `Membrane potential component <../Components/Membrane_potential.cellml>`_ defines the complete `equations of the membrane potential and total ionic current <../Components/Membrane_potential.cellml/cellml_math>`_.
It combines the imported ionic current components and ionic concentrations components:

- L-type :math:`Ca^{2+}` channels: `ICaL <../Components/ICaL.cellml>`_
  
It instantiates the imported `Ionic currents component <../Components/Ionic_currents.cellml>`_ with computed :math:`PO` using `ICaL channel states component <../Components/ICaL_channel_states.cellml>`_, while the Nernst potential :math:`E_{Ca}` computation is defined by the `Nernst potential component <../Components/E_Nernst.cellml>`_. 

- T-type :math:`Ca^{2+}` channels: `ICaT <../Components/ICaT.cellml>`_

It instantiates the imported `Ionic currents component`_ with computed :math:`PO` using `ICaT channel states component <../Components/ICaT_channel_states.cellml>`_, while the Nernst potential :math:`E_{Ca}` computation is defined by the `Nernst potential component`_.   

- Voltage dependent :math:`K^{+}` channels: `IKv <Components/IKv.cellml>`_

It instantiates the imported `Ionic currents component`_ with computed :math:`P_{Kv} = x_{Kv}*y_{Kv}`. The gating kinetics is defined in the imported `gating kinetics component <../Components/gating_kinetics.cellml>`_, while the steady states of x and y gate are defined by the imported `IKv gating steady state component <../Components/IKv_gating_inf.cellml>`_,  the Nernst potential :math:`E_{K}` computation is defined by the `Nernst potential component`_. 

- Large conductance :math:`Ca^{2+}` and voltage activated :math:`K^{+}` channels: `IBK <Components/IBK.cellml>`_

It instantiates the imported `Ionic currents component`_ with computed :math:`PO` using `IBK channel states component <../Components/IBK_channel_states.cellml>`_, while the Nernst potential :math:`E_{K}` computation is defined by the `Nernst potential component`_.

- :math:`Na^{+}` channels: `INa <Components/INa.cellml>`_

It instantiates the imported `Ionic currents component`_ with computed :math:`PO` using `INa channel states component <../Components/INa_channel_states.cellml>`_, while the Nernst potential :math:`E_{Na}` computation is defined by the `Nernst potential component`_.

- :math:`Na^{+}`- :math:`K^{+}` pump: `INaK <Components/INaK.cellml>`_

- :math:`Na^{+}`- :math:`Ca^{2+}` exchanger: `INCX <Components/INCX.cellml>`_

- Non-selective sodium leak current: `INS_Na <Components/INS_Na.cellml>`_

- Non-selective potassium leak current: `INS_K <Components/INS_K.cellml>`_

- The imported ionic concentrations components include :math:`Ca_i^{2+}`, :math:`Na_i^{+}` and :math:`K_i^{+}`.
