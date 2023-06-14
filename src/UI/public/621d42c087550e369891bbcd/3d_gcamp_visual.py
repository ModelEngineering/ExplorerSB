import numpy as np
import sys
from random import randrange as randr
import steps.rng as srng
import steps.solver as ssolver
import ip3r_model_mesh_gcamp


# Set simulation parameters
NITER = 1
T_END = 3.0
DT = 0.0001
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

###########################
###### VISUALIZATION ######
###########################

import pyqtgraph as pg
import steps.visual as visual

# Visualization initialization
app = pg.mkQApp()

# Create plot display
plots = visual.PlotDisplay("3d fine astrocytic process model", size=(600, 400))

# Create Plots
pen = pg.mkPen(color=(255, 255, 255), width=2)
p = plots.addCompSpecPlot("<span style='font-size: 16pt'>Number of GCaMP_ca", sim, "cyto", "ca_GCaMP6s", data_size=1000,
                          measure="count", pen=(255, 0.647 * 255, 0))
p.getAxis('left').setPen(pen)
p.getAxis('bottom').setPen(pen)
p.showGrid(x=True, y=True)
labelStyle = {'color': '#ffffff', 'font-size': '16px'}
p.setLabel('bottom', 'Time', 's', **labelStyle)

plots.nextRow()

p = plots.addPatchSpecPlot("<span style='font-size: 16pt'>Number of open IP3R", sim, "er_patch", "open_IP3R", data_size=1000, measure="count", y_range=[-1, 3], pen=(255, 255, 255))
p.getAxis('left').setPen(pen)
p.getAxis('bottom').setPen(pen)
p.showGrid(x=True, y=True)
p.setLabel('bottom', 'Time', 's', **labelStyle)

# Create simulation displays
ER_display = visual.SimDisplay("er", w=600, h=400)
cytIP3_display = visual.SimDisplay("ip3", w=600, h=400)
gcamp_ca_display = visual.SimDisplay("ca_GCaMP6s", w=600, h=400)
memb_display = visual.SimDisplay("er_patch", w=600, h=400)
full_display = visual.SimDisplay("Full View", w=600, h=400)

# Create static mesh components
ER_view = visual.VisualPatchMesh("cyto_patch", full_display, mesh, "er_patch", color=[0.678, 1.000, 0.184, 0.05])
cyt_view = visual.VisualCompMesh("cyto", full_display, mesh, "cyto", color=[0.941, 1.000, 0.941, 0.05])
memb_view = visual.VisualPatchMesh("cyto_patch", full_display, mesh, "cyto_patch", color=[1.000, 0.973, 0.863, 0.05])

# Create dynamic species components
IP3_cyt = visual.VisualCompSpec("IP3_cyt", full_display, mesh, sim, "cyto", "ip3", [1.0, 0.0, 0.0, 1.0],spec_size=0.02)
gcamp_ca = visual.VisualCompSpec("GCaMP_ca", full_display, mesh, sim, "cyto", "ca_GCaMP6s", [1.000, 0.647, 0.000, 1.0], spec_size=0.02)
IP3R_MEMB = visual.VisualPatchChannel("IP3R_memb", full_display, mesh, sim, "er_patch",
                                      {"unb_IP3R": [0.0, 1.0, 1.0, 0.2], "ip3_IP3R": [0.0, 0.0, 1.0, 0.5],
                                       "open_IP3R": [1.0, 1.0, 1.0, 1], "caa_IP3R": [1.0, 0.0, 1.0, 0.3],
                                       "cai_IP3R": [0.0, 1.0, 1.0, 0.3], "cai_ip3_IP3R": [1.0, 0.0, 1.0, 0.6],
                                       "ca2_IP3R": [0.0, 1.0, 1.0, 0.4], "ca2_ip3_IP3R": [1.0, 0.0, 1.0, 0.8]}, spec_size=0.02)

# Add associated components to individual displays
ER_display.addItem(ER_view)

gcamp_ca_display.addItem(cyt_view)
gcamp_ca_display.addItem(gcamp_ca)

cytIP3_display.addItem(cyt_view)
cytIP3_display.addItem(IP3_cyt)

memb_display.addItem(memb_view)
memb_display.addItem(IP3R_MEMB)

# Add simulation and displays to control
x = visual.SimControl([sim], [ER_display, cytIP3_display, gcamp_ca_display, memb_display,full_display], [plots], end_time=T_END, upd_interval=DT)
sim.run(0)

# Enter visualization loop
app.exec_()

