# To reproduce the data needed for Figure 2 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig2_sim.py

import opencor as oc
import numpy as np

# Load the simulation file
simfile='../Single_stim_experiment.sedml'
simulation = oc.open_simulation(simfile)
# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()
# Set the experiments
Vholding, t_ss = -80, 16
Vtest = 0
Nai=[ 16.55]
Cai_init= 980.63e-6
inhPump=[0, 1]
# The prefix of the saved output file name 
prefilename = ['simFig2A','simFig2B']
# Define the interval of interest for this simulation experiment
start, pointInterval = 0, 0.001
data.set_starting_point(start)
data.set_point_interval(pointInterval)
# Data to save
varName = np.array(["time", "Cai", "V"])
vars = np.reshape(varName, (1, len(varName)))
# start to save when the test voltage returns to holding
rows=int(16/pointInterval+1)
r = np.zeros((rows,len(varName)))

for j, iprefilename in enumerate(prefilename):
    for k, iNai in enumerate(Nai):
        data.set_ending_point(t_ss)
        # Reset states and parameters
        simulation.reset(True)
        # Set constant parameter values
        data.constants()['Vstim_para/V_actHolding'] = Vholding
        data.constants()['Vstim_para/V_actTest'] = Vtest
        data.constants()['Vstim_para/t_act'] = 0
        data.constants()['Vstim_para/t_ss'] = t_ss
        data.constants()['control_para/Nai'] = iNai
        data.states()['outputs/Cai'] = Cai_init
        data.constants()['control_para/inhPump'] = inhPump[j]
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Grab a specific algebraic variable results 
        r[:,0] = results.voi().values()[-rows:]
        r[:,1] = results.states()['outputs/Cai'].values()[-rows:]
        r[:,2] = results.algebraic()['outputs/V'].values()[-rows:]
        # clear the results except the last run
        simulation.clear_results() 
        # Save the simulation result of the last run
        filename='../simulatedData/%s_%d.csv' % (iprefilename,k)
        np.savetxt(filename, vars, fmt='%s',delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close

