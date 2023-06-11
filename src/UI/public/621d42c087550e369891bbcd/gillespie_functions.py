import numpy as np
import numpy.random as rnd 
import sys


"""
define propensities method
input: vector storing state at time t of all species (including the 3 binding sites of all IP3R molecules) , parameters
output: propensities array																	
"""

def propensities(vec, p):
 	ai = np.zeros(p.nb_reactions)
	# get number of ca and IP3 from vec
        ca = vec[0]
        ip3 = vec[1]
	# set indexes that represent state of each binding site (ca1, ip3 and ca2) of each IP3R
	idx_ca1 = 2 + 3 * np.arange(0, p.nIP3R)
        idx_ip3 = 3 + 3 * np.arange(0, p.nIP3R)
        idx_ca2 = 4 + 3 * np.arange(0, p.nIP3R)
	# compute vector of each IP3R state (1.0 if open, 0 if closed): ca1 and IP3 bound ca2 unbound 
        ncc = vec[idx_ca1] * vec[idx_ip3] * (1 - vec[idx_ca2])
	# compute number of bound sites for each type of binding site (ca1, ip3 and ca2) from all IP3Rs
        nca1 = np.sum(vec[idx_ca1])
        nca2 = np.sum(vec[idx_ca2])
        nip3 = np.sum(vec[idx_ip3])
        
	# get number of open IP3R: sum of IP3R state vector (equals 1.0 if open)
        rnc  = np.sum(ncc)


	#### COMPUTE PROPENSITIES ####
	#first compute propensity for IP3R-independent ca influx
        ai[0] =  p.nIP3R * p.gamma
	# compute propensity for ca flux through open IP3R
        ai[1] =  p.mu * rnc
	# compute propensity for ca decay
        ai[2] =  p.alpha * ca   
	# compute propensity for ip3 synthesis via Ca-dependent PLC activity
        ai[3] =  p.nplc * ca * p.delta / p.volume
	# compute propensity for ip3 decay
        ai[4] =  p.beta * ip3 

	# for remaining columns (index 5 to len(ai)), compute propensity for IP3R sites binding/unbinding
        rx = np.arange(p.nIP3R)
	# compute propensity for ca1 sites binding to Ca
        ai[5 + 2 * (3 * rx + 0) + 0] =  p.a1 * ca * (1 - vec[2 + 3*rx + 0]) / p.volume
	# compute propensity for ca1 sites unbinding from Ca
        ai[5 + 2 * (3 * rx + 0) + 1] =  p.b1 * vec[2 + 3*rx + 0]
	# compute propensity for ip3 sites binding to IP3
        ai[5 + 2 * (3 * rx + 1) + 0] =  p.a2 * ip3 * (1 - vec[2 + 3*rx + 1]) / p.volume
	# compute propensity for ip3 sites unbinding from IP3
        ai[5 + 2 * (3 * rx + 1) + 1] =  p.b2 * vec[2 + 3*rx + 1]
	# compute propensity for ca2 sites binding to Ca
        ai[5 + 2 * (3 * rx + 2) + 0] =  p.a3 * ca * (1 - vec[2 + 3*rx + 2]) / p.volume
	# compute propensity for ca2 sites unbinding from Ca
        ai[5 + 2 * (3 * rx + 2) + 1] =  p.b3 * vec[2 + 3*rx + 2]


        return ai


"""
define compute_gillespie method
input: vector storing state at time t of all species (including all binding sites), array with signs of reactions (sm), parameters
output: next time, vector storing state at time t+next_t of all species
"""
def compute_gillespie(vec, sm, p):
	#compute propensities
        ai = propensities(vec, p)
	# sum all propensities (ca IP3R1_ca1 IP3R2_ip3 IP3R3_ca2 ......... IP3Rn_ca1 IP3Rn_ip3 IP3Rn_ca2 ip3)
        a = np.sum(ai)
	#pick randomly time for next reaction
        next_t = - np.log(rnd.random()) / a 
	# pick randomly next reaction
        reaction = rnd.choice(p.nb_reactions, p = ai/a)
	probs=ai/a
        new_vec = vec
        new_vec +=  sm[reaction, :]
        return next_t, new_vec
