# To reproduce the data needed for Figure 8 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig8_sim.py

import opencor as oc
import numpy as np
# The prefix of the saved output file name 
prefilename = 'simFig8'
# Load the simulation file
simfile='Periodic_stimulation.sedml'
simulation = oc.open_simulation(simfile)
# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()
# Define the interval of interest for this simulation experiment
pointInterval = 0.1
data.set_point_interval(pointInterval)
N=30
varName = np.array(["time","V", "Cai"])
vars = np.reshape(varName, (1, 3))
rows=40*1000*10
r = np.zeros((rows,len(varName)))
T=310
# Reset states and parameters
simulation.reset(True)
for i in range(N): 
   # Set constant parameter values
   start=i*60000
   end=start+60000
   data.set_starting_point(start)
   data.set_ending_point(end)
   data.constants()['Istim_parameters/T'] = T
   simulation.run()
   # Access simulation results
   results = simulation.results()
   # Grab a specific algebraic variable results
   r[:,0] = results.voi().values()[-rows:]
   r[:,1] = results.states()['outputs/V'].values()[-rows:]
   r[:,2] = results.states()['outputs/Cai'].values()[-rows:]
   # clear the results except the last run
   simulation.clear_results()

 # Save the simulation result of the last run
filename='%s.csv' % (prefilename)
np.savetxt(filename, vars, fmt='%s',delimiter=",")
with open(filename, "ab") as f:
    np.savetxt(f, r, delimiter=",")
f.close


