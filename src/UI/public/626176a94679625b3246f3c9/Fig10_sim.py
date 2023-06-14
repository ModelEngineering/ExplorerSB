# To reproduce the data needed for Figure 10 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig10_sim.py

import opencor as oc
import numpy as np

# Load the simulation file
simfile='../Cai_experiment2.sedml'
simulation = oc.open_simulation(simfile)
# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()
# Set the experiments
end = 143
# Define the interval of interest for this simulation experiment
start, pointInterval = 0, 0.001
data.set_starting_point(start)
data.set_point_interval(pointInterval)
# Data to save
varName = np.array(["time", "phosphorylation", "stress","Cai"])
vars = np.reshape(varName, (1, len(varName)))
rows=[int((end)/pointInterval+1)]
# The prefix of the saved output file name 
prefilenames = ['simFig10']

for j, prefilename in enumerate(prefilenames):
    data.set_ending_point(end)   
    # Reset states and parameters
    simulation.reset(True)   
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Grab a specific algebraic variable results 
    r = np.zeros((rows[j],len(varName)))
    r[:,0] = results.voi().values()[-rows[j]:]
    r[:,1] = results.algebraic()['outputs/phosphorylation'].values()[-rows[j]:]
    r[:,2] = results.algebraic()['outputs/stress'].values()[-rows[j]:]
    r[:,3] = results.algebraic()['Cai/Cai'].values()[-rows[j]:]
    # clear the results except the last run
    simulation.clear_results() 
    # Save the simulation result of the last run
    filename='../simulatedData/%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s',delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
    

