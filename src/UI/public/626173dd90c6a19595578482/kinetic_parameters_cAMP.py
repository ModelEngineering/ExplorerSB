# cAMP module

# Return kinetic parameters, constraints, and vector of volumes in each
# compartment (pL) (1 if gating variable, or in element corresponding to
# kappa)

# includes contributions from Gs and Gi proteins - assume they act on the
# same adenylyl cyclase form

# data for Gs is from saucerman2003
# data for Gi is made up from Shelley's brain 

import numpy as np

def kinetic_parameters(M, include_type2_reactions, dims, V):
    # Set the kinetic rate constants
    # knowns:   K_m [=] fmol/L
    #           kcat [=] per_sec
    
    num_cols = dims['num_cols']
    num_rows = dims['num_rows']
    
    K1_m = 1.03e3        # uM
    k1cat = 0.2          # 1/s
    K2_m = 3.15e+2       # uM
    k2cat = 8.5          # 1/s
    K3_m = 8.60e+2       # uM
    k3cat = 1e-16        # 1/s
    K4_m = 1.30          # uM
    k4cat = 5            # 1/s
    K5_m = 30            # uM
    K6_m = 0.4           # uM
    K7_m = 44            # uM
    KGiAC_m = 10 # made up value # uM

    # initialise arrays
    vkap = np.zeros(4)
    vkam = np.zeros(4)
    vkbp = np.zeros(4)
    vkbm = np.zeros(4)
    vkm2 = np.zeros(4)
    vkp2 = np.zeros(4)
    vK_m = [K1_m,K2_m,K3_m,K4_m,K5_m,K6_m,K7_m,KGiAC_m]
    vkcat = [k1cat,k2cat,k3cat,k4cat]

    kap_mult = [0.93, 0.1, 1, 1,0.1] # finding rates from literature?
    fastKineticConstant = 1e6 # 1/s

    # include the Gi reaction to remove it from the system in inhibited
    # form
    iks = range(4)
    for i in range(4):
        vkap[i] = kap_mult[i]*fastKineticConstant
        vkam[i] = vkap[i]*vK_m[iks[i]] - vkcat[i]
        vkbp[i] = vkcat[i]
        vkbm[i] = (vkap[i]*vkbp[i])/vkam[i]
    
    # reactions 1,2,3 are COUPLED as they share the same substrates and
    # products, so their Keq are the same. Choose Keq(1) as the truth to
    # use.
    
    if include_type2_reactions:
        iks = range(4,8)
        for i in range(4):
            vkm2[i] = fastKineticConstant
            vkp2[i] = vkm2[i]/vK_m[iks[i]]
    

    # Calculate bond graph constants from kinetic parameters
    # Note: units of kappa are fmol/s, units of K are fmol^-1
    k_kinetic = [vkap[0], vkbp[0], 
        vkap[1], vkbp[1],
        vkap[2], vkbp[2],
        vkap[3], vkbp[3],
        vkp2[0], vkp2[1],vkp2[2], vkp2[3],
        vkam[0], vkbm[0],
        vkam[1], vkbm[1],
        vkam[2], vkbm[2],
        vkam[3], vkbm[3],
        vkm2[0], vkm2[1],vkm2[2], vkm2[3],
        ]

    # CONSTRAINTS
    N_cT = np.zeros([2,len(M[0])]) 
    if False:
        # show substrate ATP is in eqlm with product cAMP
        N_cT[0][num_cols ] = 1
        N_cT[0][num_cols + 1] = -1
    # constraint for equilibrium between cAMP and five_AMP
    N_cT[0][num_cols + 1] = 1
    N_cT[0][num_cols + 10] = -1
    
    # constraint for formation of five_AMP from cAMP and PDE rxn 
    G_0_cAMP = -48.116 # kJ/mol
    R = 8.314
    T = 310
    K_cAMP = np.exp(G_0_cAMP/(R*T))*pow(10,6)
    N_cT[1][num_cols+2] = 1
    N_cT[1][num_cols] = -1

    K_C = [1, K_cAMP]

    # volume vector
    W = list(np.append([1] * num_cols, [V['V_myo']] * num_rows))

    return (k_kinetic, N_cT, K_C, W)













