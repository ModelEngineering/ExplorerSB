# B1AR module 

#     return (k_kinetic, N_cT, K_C, W) kinetic parameters, constraints, and vector of volumes in each
# compartment (pL) (1 if gating variable, or in element corresponding to
# kappa)

# 6 sep 21: removing signalling rewactions (separate module, LRGbinding)

# 5 Oct removing B1tot as the product of PKACI reaction with R. Instead,
# using R as the substrate, which gets phosphorylated to B1AR_p by PKACI.
# This means reactions p1 and p2 are switched around with directions
# reversed.

import numpy as np 

def kinetic_parameters(M, include_type2_reactions, dims, V):
    # Set the kinetic rate constants.
    # original model had reactions that omitted enzymes as substrates e.g. BARK
    # convert unit from 1/s to 1/uM.s by dividing by conc of enzyme
    # all reactions were irreversible, made reversible by letting kr ~= 0
    
    num_cols = dims['num_cols']
    num_rows = dims['num_rows']

    # concentration of BARK = 0.6uM (crude approx from litsearch, for GRK)
    bigNum = 1e6
    fastKineticConstant = bigNum
    smallReverse = fastKineticConstant/(pow(bigNum,2))
    cBARK = 0.6                #uM
    cPKACI = 0.0587898478276673        #uM
    
    Kl = 0.285 # uM
    Kr = 0.062 # uM
    Kc = 33 # uM
    
    kB11p = 1.1e-3 / cBARK     # 1/uM.s
    kB11m = 2.2e-3             # 1/s
    kB12p = fastKineticConstant#1/s
    kB12m = smallReverse       # 1/uM.s
    kB21p = kB11p              # 1/uM.s
    kB21m = kB11m              # 1/s
    kB22p = fastKineticConstant#1/s
    kB22m = smallReverse       # 1/uM.s
    kP1p = 3.6e-3              # 1/uM.s 
    kP1m = 2.2e-3              # 1/s 
    kP2p = fastKineticConstant # 1/s
    kP2m = smallReverse        # 1/uM.s
    
    # detailed balance for kP2p
#     kP2p = kP2m*kP1m/kP1p
    
    k_kinetic = [
        kB11p, kB12p, kB21p, kB22p, kP1p, kP2p,
        kB11m, kB12m, kB21m, kB22m, kP1m, kP2m
        ]
    nid = [1,10]

    # CONSTRAINTS
    N_cT = np.zeros(len(M[0]))
    if True:
        # PKACI: substrate R is in eqlm with product B1ARp
        N_cT[num_cols + nid[0]] = 1
        N_cT[num_cols + nid[1]] = -1
    
    
    K_C = [1]

    # volume vector
    W = list(np.append([1] * num_cols, [V['V_myo']] * num_rows))

    return (k_kinetic, [N_cT], K_C, W) 