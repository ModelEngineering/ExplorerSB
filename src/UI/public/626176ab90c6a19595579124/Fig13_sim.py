# To reproduce the data needed for Figure 13 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig13_sim.py

import opencor as oc
import numpy as np
# The prefix of the saved output file name 
prefilename = 'simFig13_'
# Load the simulation file
simfile='Periodic_stimulation_SA.sedml'
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
rows=20*1000*10
r = np.zeros((rows,len(varName)))

# control
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
   r[:,0] = results.voi().values()[0:rows]
   r[:,1] = results.states()['outputs/V'].values()[0:rows]
   r[:,2] = results.states()['outputs/Cai'].values()[0:rows]
   # clear the results except the last run
   simulation.clear_results()

 # Save the simulation result of the last run
filename='%s0.csv' % (prefilename)
np.savetxt(filename, vars, fmt='%s',delimiter=",")
with open(filename, "ab") as f:
    np.savetxt(f, r, delimiter=",")
f.close

# Parameters to change
gs = [1.0217, 80, 25.1, 1.44]
gnames = ['g_Kv', 'g_BK', 'g_Na', 'g_CaL']
files = ['a', 'b', 'c', 'd']

for j , Gmax in enumerate(gs):
   # Set constant parameter values
   gkey = 'g_parameters/%s' % gnames[j]

   for n in range(2):
        if n == 0: #increase 50%
           # Reset states and parameters
           simulation.reset(True)
           data.constants()[gkey] = Gmax*1.5
        else: # decrease 50%
            # Reset states and parameters
           simulation.reset(True)
           data.constants()[gkey] = Gmax*0.5
 
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
          r[:,0] = results.voi().values()[0:rows]
          r[:,1] = results.states()['outputs/V'].values()[0:rows]
          r[:,2] = results.states()['outputs/Cai'].values()[0:rows]
          # clear the results except the last run
          simulation.clear_results()
       
        # Save the simulation result of the last run
        filename='%s%s%d.csv' % (prefilename,files[j],(n+1))
        np.savetxt(filename, vars, fmt='%s',delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close