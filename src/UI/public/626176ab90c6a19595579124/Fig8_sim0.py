# To reproduce the data needed for Figure 7 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: Fig8_sim.py

import opencor as oc
import numpy as np
# The prefix of the saved output file name 
prefilename = 'simFig8'
# Load the simulation file
simfile='new_poh_2012.sedml'
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
# Reset states and parameters
simulation.reset(True)
for i in range(N): 
   # Set constant parameter values
   start=i*60000
   end=start+60000
   data.set_starting_point(start)
   data.set_ending_point(end)
   simulation.run()
   # Access simulation results
   results = simulation.results()
   # Grab a specific algebraic variable results
   r[:,0] = results.voi().values()[-rows:]
   r[:,1] = results.states()['membrane/V'].values()[-rows:]
   r[:,2] = results.states()['ionic_concentrations/Cai'].values()[-rows:]
   # clear the results except the last run
   simulation.clear_results()

 # Save the simulation result of the last run
filename='%s.csv' % (prefilename)
np.savetxt(filename, vars, fmt='%s',delimiter=",")
with open(filename, "ab") as f:
    np.savetxt(f, r, delimiter=",")
f.close


