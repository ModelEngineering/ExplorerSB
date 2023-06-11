# To reproduce the data needed for Figure 5 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig5_sim.py

import opencor as oc
import numpy as np

# Load the simulation file
simfile='../Single_stim_experiment.sedml'
simulation = oc.open_simulation(simfile)
# The data object houses all the relevant information
# and pointers to the OpenCOR internal data representations
data = simulation.data()
# Set the experiments
Vholding=[-80, -50]
t_ss = [16, 0]
duration = [0, 0.2]
Vtest = [0, 0]
Nai=[ 16.55, 2.9836]
Cai_init= [980.63e-6, 123e-6]
end =[t_ss[0]+duration[0],t_ss[1]+duration[1]+3.5]
# Define the interval of interest for this simulation experiment
start, pointInterval = 0, 0.001
data.set_starting_point(start)
data.set_point_interval(pointInterval)
# Data to save
varName = np.array(["time", "J_CaPump", "J_NaCa", "J_VOCC"])
vars = np.reshape(varName, (1, len(varName)))
rows=[int((16)/pointInterval+1),int((duration[1]+3.5)/pointInterval+1)]
# The prefix of the saved output file name 
prefilenames = ['simFig5A','simFig5B']
inhPump=1

for j, prefilename in enumerate(prefilenames):
    data.set_ending_point(end[j])   
    # Reset states and parameters
    simulation.reset(True)
    # Set constant parameter values
    data.constants()['Vstim_para/V_actHolding'] = Vholding[j]
    data.constants()['Vstim_para/V_actTest'] = Vtest[j]
    data.constants()['Vstim_para/t_act'] = duration[j]
    data.constants()['Vstim_para/t_ss'] = t_ss[j]
    data.constants()['control_para/Nai'] = Nai[j]
    data.states()['outputs/Cai'] = Cai_init[j]
    data.constants()['control_para/inhPump'] = inhPump
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Grab a specific algebraic variable results 
    r = np.zeros((rows[j],len(varName)))
    r[:,0] = results.voi().values()[-rows[j]:]
    r[:,1] = results.algebraic()['outputs/J_CaPump'].values()[-rows[j]:]
    r[:,2] = results.algebraic()['outputs/J_NaCa'].values()[-rows[j]:]
    r[:,3] = results.algebraic()['outputs/J_VOCC'].values()[-rows[j]:]
    # clear the results except the last run
    simulation.clear_results() 
    # Save the simulation result of the last run
    filename='../simulatedData/%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s',delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
    

