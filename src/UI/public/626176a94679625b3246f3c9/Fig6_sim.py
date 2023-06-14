# To reproduce the data needed for Figure 6 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig6_sim.py

import opencor as oc
import numpy as np

# Load the simulation file
simfile='../Multi_stim_experiment.sedml'
simulation = oc.open_simulation(simfile)
# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()
# Set the experiments
Vholding=[-80]
t_ss = [0]
t_act = [0.1]
Vtest = [0]
Nai=[ 16.55]
end =[14.4]
# Define the interval of interest for this simulation experiment
start, pointInterval = 0, 0.001
data.set_starting_point(start)
data.set_point_interval(pointInterval)
# Data to save
varName = np.array(["time",  "Cai", "V"])
vars = np.reshape(varName, (1, len(varName)))
rows=[int((14.4)/pointInterval+1)]
# The prefix of the saved output file name 
prefilenames = ['simFig6']
inhPump=1

for j, prefilename in enumerate(prefilenames):
    data.set_ending_point(end[j])   
    # Reset states and parameters
    simulation.reset(True)
    # Set constant parameter values
    data.constants()['Vstim_para/V_actHolding'] = Vholding[j]
    data.constants()['Vstim_para/V_actTest'] = Vtest[j]
    data.constants()['Vstim_para/t_act'] = t_act[j]
    data.constants()['Vstim_para/t_ss'] = t_ss[j]
    data.constants()['control_para/Nai'] = Nai[j]
    data.constants()['control_para/inhPump'] = inhPump
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Grab a specific algebraic variable results 
    r = np.zeros((rows[j],len(varName)))
    r[:,0] = results.voi().values()[-rows[j]:]
    r[:,1] = results.states()['outputs/Cai'].values()[-rows[j]:]
    r[:,2] = results.algebraic()['outputs/V'].values()[-rows[j]:]
    # clear the results except the last run
    simulation.clear_results() 
    # Save the simulation result of the last run
    filename='../simulatedData/%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s',delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
    

