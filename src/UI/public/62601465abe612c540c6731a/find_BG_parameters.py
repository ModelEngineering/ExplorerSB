# This script calculates the bond graph parameters for all reactions of the
# a given module. Specify the directory.
# based on SERCA model of Pan et al, which is based on Tran et al. (2009). 
# Parameters calculated in module's directory, by using the kinetic
# parameters and stoichiometric matrix.

# return W from kinetic_parameters

import os
import csv
import json
import math
import numpy as np
import sympy
from sympy import Matrix, S, nsimplify
from scipy.linalg import null_space
from fractions import Fraction

def read_IDs(path):
    data = []
    with open(path,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        f.close()
    return data


def load_matrix(stoich_path):
    matrix = []
    with open(stoich_path,'r') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            matrix.append([int(r) for r in row])
        f.close()
    return matrix

# def rational_nullspace(A, max_denom = 10):
#     v = null_space(A)
#     vFrac = [[Fraction(num).limit_denominator(max_denominator=max_denom) for num in row] for row in v]
#
#     vRat = [] #np.zeros([len(vFrac),len(vFrac[0])])
#     if not v.any():
#         return []
#     all_denom = [[res.denominator for res in row] for row in vFrac]
#     if all_denom.count(all_denom[0]) == len(all_denom):# identical
#         for row in vFrac:
#             largest_denom = max([res.denominator for res in row])
#             vRat.append( [vi.numerator for vi in row] )
#         return vRat
#     else:
#         print('denominators for fractions of rational nullspace are not identical')
#         return []

if __name__ == "__main__":

    ## booleans
    write_parameters_file = True
    include_constraints = True
    include_type2_reactions = True

    ## Set directories
    current_dir = os.getcwd()
    data_dir = current_dir + '\data'
    output_dir = current_dir + '\output'
    modname = os.path.dirname(current_dir).split('\\')[-1].split('BG_')[-1]
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    if ('beta1' in current_dir) and False:
        matstr = '_withR_LR_scheme4'
    else:
        matstr = ''

    ## Define volumes
    V_myo = 34.4 # pL
    V = dict()
    V['V_myo'] = V_myo

    ## Load forward matrix
    if include_type2_reactions:
        stoich_path = data_dir + '\\all_forward_matrix%s.txt'%matstr
    else:
        stoich_path = data_dir + '\\all_noType2_forward_matrix.txt'

    N_f = load_matrix(stoich_path)


    ## Load reverse matrix
    if include_type2_reactions:
        stoich_path = data_dir + '\\all_reverse_matrix%s.txt'%matstr
    else:
        stoich_path = data_dir + '\\all_noType2_reverse_matrix.txt'
    
    N_r = load_matrix(stoich_path)

    N_fT = np.transpose(N_f)
    N_rT = np.transpose(N_r)

    ## Calculate stoichiometric matrix
    # I matrix to align with placement of kappa down the column.
    # x-axis of stoich matrix (R1a, R1b etc) coincides with the kp km of that kinetic reaction
    N = [[N_r[j][i] - N_f[j][i] for i in range(len(N_f[0]))] for j in range(len(N_f))]
    N_T = [[N_rT[j][i] - N_fT[j][i] for i in range(len(N_fT[0]))] for j in range(len(N_fT))]

    num_rows = len(N)
    num_cols = len(N[0])
    dims = dict()
    dims['num_rows'] = num_rows
    dims['num_cols'] = num_cols

    I = np.identity(num_cols)

    M = np.append(np.append(I, N_fT,1), np.append(I, N_rT,1),0)

    func = __import__('kinetic_parameters_%s'%modname)
    [k_kinetic, N_cT, K_C, W] = func.kinetic_parameters(M, include_type2_reactions, dims, V)
    if not include_constraints:
        N_cT = []

    try:
        M = np.append(M, N_cT,0)
        k = np.append(k_kinetic, K_C, 0)
    except:
        k = k_kinetic

    # Calculate bond graph constants from kinetic parameters
    # Note: units of kappa are fmol/s, units of K are fmol^-1
    lambda_expo = np.matmul(np.linalg.pinv(M), [math.log(ik) for ik in k])
    lambdaW = [math.exp(l) for l in lambda_expo]


    # Check that kinetic parameters are reproduced by bond graph parameters
    k_est = np.matmul(M,[math.log(k) for k in lambdaW])
    k_est = [math.exp(k) for k in k_est]
    diff = [(k[i] - k_est[i])/k[i] for i in range(len(k))]

    error = np.sum([abs(d) for d in diff])

    # Checks
    N_rref = sympy.Matrix(N).rref()
    R = nsimplify(Matrix(N), rational=True).nullspace() #rational_nullspace(N, max_denom=len(N[0]))
    if R:
        R = np.transpose(np.array(R).astype(np.float64))[0]
    # Check that there is a detailed balance constraint
    Z = nsimplify(Matrix(M), rational=True).nullspace() #rational_nullspace(M, 2)
    if Z:
        Z = np.transpose(np.array(Z).astype(np.float64))[0]

    kf = k_kinetic[:num_cols]
    kr = k_kinetic[num_cols:]
    K_eq = [kf[i]/kr[i] for i in range(len(kr))]
    try:
        zero_est = np.matmul(np.transpose(R),K_eq)
        zero_est_log = np.matmul(np.transpose(R),[math.log(k) for k in K_eq])
    except:
        print('undefined R nullspace')

    # if not R_mat:
    #     warning('R_mat is empty: matrix is full rank')
    
    lambdak = [lambdaW[i]/W[i] for i in range(len(W))]
    kappa = lambdak[:len(N[0])]
    K = lambdak[len(N[0]):]

    rxnID = read_IDs('data\\rxnID.txt')
    Kname = read_IDs('data\\Kname.txt')


    # ### print outputs ###
    for ik in range(len(kappa)):
        print('var kappa_%s: fmol_per_sec {init: %g, pub: out};' %(rxnID[ik],kappa[ik]))
    for ik in range(len(Kname)):
        print('var K_%s: per_fmol {init: %g, pub: out};' %(Kname[ik],K[ik]))

    file = open(output_dir + '/all_parameters_out.json', 'w')
    data = { "K": K, "kappa": kappa, "k_kinetic": k_kinetic }
    json.dump(data, file)


    cellmlfilepath = os.getcwd() + '\\TEMP.cellml.txt'
    with open(cellmlfilepath, 'w') as cid:
        cid.write('def model individual_%s as\n def import using "units_and_constants/units_BG.cellml" for\n\
        unit mM using unit mM;\nunit fmol using unit fmol;\nunit per_fmol using unit per_fmol;\n\
        unit J_per_mol using unit J_per_mol;\nunit fmol_per_sec using unit fmol_per_sec;\n\
        unit C_per_mol using unit C_per_mol;\n  unit J_per_C using unit J_per_C;\n\
        unit microm3 using unit microm3;\n  unit fF using unit fF;\n\
        unit fC using unit fC;\n  unit fA using unit fA;\n\
        unit per_second using unit per_second;\n  unit millivolt using unit millivolt;\n\
        unit per_sec using unit per_sec;\n  unit J_per_K_per_mol using unit J_per_K_per_mol;\n\
        unit fmol_per_L using unit fmol_per_L;\n  unit fmol_per_L_per_sec using unit fmol_per_L_per_sec;\n\
        unit per_sec_per_fmol_per_L using unit per_sec_per_fmol_per_L;\n  unit uM using unit uM;\n\
        unit mM_per_sec using unit mM_per_sec;\n  unit uM_per_sec using unit uM_per_sec;\n\
        unit pL using unit pL;\n  unit m_to_u using unit m_to_u;\n enddef;\n' %(modname))
        cid.write('def import using "units_and_constants/constants_BG.cellml" for\n\
            comp constants using comp constants;\nenddef;\n\n')
        cid.write("    def comp environment as\n\
    var time: second {pub: out};\n\
    // initial values\n")
        for Kn in Kname:
            cid.write('var q_%s_init: fmol {init: 1e-888};\n' %(Kn))
        cid.write('// Global value\n')
        for Kn in Kname:
            cid.write('var q_%s: fmol {pub: out};\n'%Kn)
        cid.write('// From submodule\n')
        for Kn in Kname:
            cid.write('var q_%s_m%s: fmol {pub: in};\n'%(Kn, modname))
        for Kn in Kname:
            cid.write('q_%s = q_%s_m%s + q_%s_init;\n'%(Kn, Kn,
                modname,Kn))
        cid.write('enddef;\n\n')
        cid.write('def comp %s_parameters as\n' %(modname))
        for ik in range(len(kappa)):
            cid.write('var kappa_%s: fmol_per_sec {init: %g, pub: out};\n' % (rxnID[ik], kappa[ik]))
        for ik in range(len(Kname)):
            cid.write('var K_%s: per_fmol {init: %g, pub: out};\n' % (Kname[ik], K[ik]))
        cid.write('enddef;\n')

        cid.write('def comp %s as\n' %(modname))
        cid.write('        var time: second {pub: in};\n\
        var R: J_per_K_per_mol {pub: in};\n\
        var T: kelvin {pub: in};\n\
        // parameters\n')
        for ik in range(len(kappa)):
            cid.write('var kappa_%s: fmol_per_sec {pub: in};\n' % (rxnID[ik]))
        for ik in range(len(Kname)):
            cid.write('var K_%s: per_fmol {pub: in};\n' % (Kname[ik]))

        cid.write('// Input from global environment\n')
        for Kn in Kname:
            cid.write('var q_%s_global: fmol {pub: in};\n'%Kn)
        cid.write('// Output to global environment\n')
        for Kn in Kname:
            cid.write('var q_%s: fmol {init: 1e-16, pub: out};\n'%(Kn))
        cid.write('// Constitutive parameters\n')
        for Kn in Kname:
            cid.write('var mu_%s: J_per_mol;\n'%(Kn))
        for rx in rxnID:
            cid.write('var v_%s: fmol_per_sec;\n'%(rx))
        for Kn in Kname:
            cid.write('mu_%s = R*T*ln(K_%s*q_%s_global);\n'%(Kn,Kn,Kn))
        for rx in rxnID:
            cid.write('v_%s = ppp;\n'%(rx))
        for Kn in Kname:
            cid.write('ode(q_%s, time) = qqq;\n'%Kn)
        cid.write('enddef;\n')

        cid.write('def map between environment and %s for\n'%modname)
        cid.write('vars time and time;\n')
        for Kn in Kname:
            cid.write('vars q_%s_m%s and q_%s;\n'%(Kn, modname,Kn))
            cid.write('vars q_%s and q_%s_global;\n'%(Kn, Kn))
        cid.write('enddef;\n')
        cid.write('def map between %s and %s_parameters for\n'%(modname,modname))
        for ik in rxnID:
            cid.write('vars kappa_%s and kappa_%s;\n' % (ik, ik))
        for mod in Kname:
            cid.write('vars K_%s and K_%s;\n' % (mod, mod))
        cid.write('enddef;\n')
        cid.write('def map between constants and %s for\n'%modname)
        cid.write('vars R and R;\n vars T and T;\n')
        cid.write('enddef;\n')
        cid.write('enddef;\n')
        cid.close()

    print('error =', (error))


