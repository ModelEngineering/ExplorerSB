import numpy as np
import sys
from gillespie_functions import compute_gillespie, propensities


### Set parameter values
class param(object):
    def __init__(self,volume, mu, alpha, nIP3R, gamma, a1, b1, a2, b2, a3, b3, nplc, delta, beta, nb_reactions):
        self.a1 = a1
        self.b1 = b1
        self.a2 = a2
        self.b2 = b2
        self.a3 = a3
        self.b3 = b3
        self.nplc = nplc
        self.delta = delta
        self.beta = beta
        self.mu = mu
        self.alpha = alpha
        self.nIP3R = nIP3R
        self.gamma = gamma
        self.volume = volume
	self.nb_reactions = nb_reactions
alpha = 1.0
gamma = 0.05
# a1 and b1 -> ca first site
a1 = 1.0
b1 = 0.1
# a2 & b2 -> ip3 site
a2 =1.0
b2 = 0.1
# a3 and b3 -> ca second site
a3 = 0.1
b3 = 0.1
delta = 0.1
beta = 0.01

sid = int(sys.argv[1])
np.random.seed(sid)
nx = 200.0
ny = 200.0
size = 1
volume = (nx * ny)/size
nIP3R = 1000
mu=50
nplc = 1000

#defining gillespie parameters (number of reactions and number of states + all parameters of model)
nb_reactions = 5 + 2 * 3 * nIP3R
nb_states = 2 + 3 * nIP3R

p = param(volume, mu, alpha, nIP3R, gamma, a1, b1, a2, b2, a3, b3, nplc, delta, beta, nb_reactions)


### INITIALIZATION
t= 0.0
total_time = 10000
ca0 = 50
ip0 = 15

#initialization of a vector that stores # ca, # ip3, state of first ca (ca1) site #1, state of ip3 site #1, state of second ca (ca2) site #1,
# ca1_#2, ip3_#2, ca2_#2, ..., ca1_#n, ip3_#n, ca2_#n 
vec = np.zeros(2 + 3 * nIP3R)
vec[0] = ca0
vec[1] = ip0

"""
initialize matrix sm that represents if reaction will increase or decrease nb of elements in a given state
	columns: ca IP3 IP3R1_ca1 IP3R2_ip3 IP3R3_ca2 ......... IP3Rn_ca1 IP3Rn_ip3 IP3Rn_ca2
	lines: leak mu alpha IP3S_plc Ir a1 b1 a2 b2 a3 b3 .... nIP3R times
	       ca      ip3      IP3R1_ca1   IP3R1_ip3  IP3R2_ca2 .... IP3Rn_ca1  IP3Rn_ip3  IP3Rn_ca2  
leak		1	0	0									
mu		1	0	0									
alpha		-1	0	0
IP3s+plc	0	1	0										
Ir		0	-1	0									
a1		0	0	1									
b1		0	0	-1									
a2		0	0	0									
b2		0	0	0									
a3		0	0	0									
b3		0	0	0	
"""
sm = np.zeros((nb_reactions, nb_states))
# nb ca evolves positively with leak and mu and negatively with alpha
sm[0, 0] = 1.0
sm[1, 0] = 1.0
sm[2, 0] = -1.0
#IP3 synthesis (IP3s and plc activation) term
sm[3, 1] = 1.0
#ip3 degradation term
sm[4, 1] = -1.0

#set signs of reactions for all receptor sites (3*nIP3R)
for r in range(nIP3R):
	for site in range(3):
		sm[5 + 2 * (3 * r + site) + 0, 2 + 3 * r + site] =  1.0
                sm[5 + 2 * (3 * r + site) + 1, 2 + 3 * r + site] = -1.0


###COMPUTE GILLESPIE
while t < total_time:
    next_t, new_vec = compute_gillespie(vec, sm, p)
    t += next_t
    vec = new_vec
    #set indexes of states of each type of IP3R binding site
    idx_ca1 = 2 + 3 * np.arange(0, nIP3R)
    idx_ip3 = 3 + 3 * np.arange(0, nIP3R)
    idx_ca2 = 4 + 3 * np.arange(0, nIP3R)
    # get vector of each IP3R (equals 1.0 if open, 0 if closed): first Ca and IP3 bound (state=1.0) and second Ca unbound (state=0)
    ncc = vec[idx_ca1] * vec[idx_ip3] * (1 - vec[idx_ca2])
    # same method, number of first Ca sites that are bound, same for IP3 and second Ca sites
    nca1 = np.sum(vec[idx_ca1])
    nca2 = np.sum(vec[idx_ca2])
    nip3 = np.sum(vec[idx_ip3])

    # get number of open IP3R: sum of IP3R state vector (equals 1.0 if open)
    rnc  = np.sum(ncc)
    # for each reaction, print nb ca, nb ip3, nb R open, nb free ca1, ca2 and ip3 sites
    print "%.2f" % t, vec[0], vec[1], rnc, nIP3R-nca1, nIP3R-nca2, nIP3R-nip3
