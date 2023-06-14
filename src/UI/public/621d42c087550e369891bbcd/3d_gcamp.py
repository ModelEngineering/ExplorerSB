import numpy as np
import sys
import steps.rng as srng
import steps.solver as ssolver
import ip3r_model_mesh_gcamp

# Set simulation parameters
T_END = 100.0
DT = 0.001
POINTS = int(T_END / DT)
tpnts = np.arange(0.0, T_END, DT)
ntpnts = tpnts.shape[0]

# Import model
mdl = ip3r_model_mesh_gcamp.getModel()

# Import geometry
mesh, cyt_tris, er_tris = ip3r_model_mesh_gcamp.gen_geom()

# Create random number generator
seed = int(sys.argv[1])
r = srng.create('mt19937', 512)
r.initialize(seed)

# Create solver object
sim = ssolver.Tetexact(mdl, mesh, r)

# Reset the simulation object
sim.reset()

# Set initial conditions
sim.setCompCount('cyto', 'ca', 10)
sim.setCompCount('cyto', 'ip3', 3)
sim.setPatchCount('cyto_patch', 'plc', 1696)
sim.setCompConc('cyto', 'GCaMP6s', 9.55e-6)
sim.setCompConc('cyto', 'ca_GCaMP6s', 450e-9)
sim.setPatchCount('er_patch', 'unb_IP3R', 50)

f = open("sim_gcamp.%d" % seed, "w")
print(f.name)

#run the simulation and record data
for i in range(ntpnts):
    sim.run(tpnts[i])
    f.write("%d %d\n" % (
        sim.getCompCount('cyto', 'ca_GCaMP6s'), sim.getPatchCount('er_patch', 'open_IP3R')))
f.close()

