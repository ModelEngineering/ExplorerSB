# To reproduce the data needed for Figure 2 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig2_sim.py

import opencor as oc
import numpy as np
# The prefix of the saved output file name 
prefilename = 'simFig2'
# Load the simulation file
simfile='Patch_clampXi_experiment.sedml'
simulation = oc.open_simulation(simfile)
# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()
# Set the experiments
Vholding, t_ss = -100, 1000
Vtest = range (-90, 40, 5)
duration = 140
Cai=[5.38843941249284e-5, 0.11]
T=297
# Define the interval of interest for this simulation experiment
start, end, pointInterval = 0, t_ss+duration, 0.1
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)
# Data to save
varName = np.array(["V", "ICaL"])
vars = np.reshape(varName, (1, len(varName)))
row_start=int(t_ss/pointInterval-50) # to get the peak
r = np.zeros((len(Vtest),len(varName)))
for j, iCai in enumerate(Cai):
   for i, V in enumerate(Vtest): 
      # Reset states and parameters
      simulation.reset(True)
      # Set constant parameter values
      data.constants()['Clamp_parameters/V_actHolding'] = Vholding
      data.constants()['Clamp_parameters/V_actTest'] = V
      data.constants()['Clamp_parameters/T'] = T
      data.constants()['Clamp_parameters/Cai'] = iCai
      simulation.run()
      # Access simulation results
      results = simulation.results()
      # Grab a specific algebraic variable results
      r[i,0] = V
      temp = results.algebraic()['outputs/I_CaL'].values()[row_start:]
      r[i,1] = -max(abs(temp))
      # clear the results except the last run
      simulation.clear_results()
   
    # Save the simulation result of the last run
   filename='%s_%d.csv' % (prefilename,j)
   np.savetxt(filename, vars, fmt='%s',delimiter=",")
   with open(filename, "ab") as f:
       np.savetxt(f, r, delimiter=",")
   f.close


