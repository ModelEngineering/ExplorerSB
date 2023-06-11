import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig5'
items = ['a', 'b']
# Figure name
prefig = 'Fig5'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 6
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 1, 1
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 12, 12 # legend, label fontsize

# Read data from the files
x_name = 'V'
y_name = ['P_BK']
current= r'$P_{BK}$'
y_labels = ['Open probability %s' % current]
legends=['0.001mM','0.0003mM']
T=297
for i, varName in enumerate(y_name):   
    ax[i] = fig.add_subplot(subpRow, subpCol, i+1)
    j=0 
    filename= '%s%s.csv' % (prefilename,items[j])
    data = pd.read_csv(filename)
    x_data = data[x_name]
    y_data = data[varName]  
    ax[i].plot(x_data, y_data,  color=cycle[j], label = 'CellML@$Ca_i$=%s, T=%dK' % (legends[j],T))

    ofilename ='fig5%s.csv' % (items[j])
    odata = pd.read_csv(ofilename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']    
    ax[i].plot(ox_data, oy_data, '.',  color=cycle[j], label = 'Poh_et_al_hJSMC @%s' % (legends[j]))

    j=1
    filename= '%s%s.csv' % (prefilename,items[j])
    data = pd.read_csv(filename)
    x_data = data[x_name]
    y_data = data[varName]  
    ax[i].plot(x_data, y_data,  color=cycle[j], label = 'CellML@$Ca_i$=%s, T=%dK' % (legends[j],T))

    ofilename ='fig5%s.csv' % (items[j])
    odata = pd.read_csv(ofilename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']    
    ax[i].plot(ox_data, oy_data, '.',  color=cycle[j], label = 'Poh_et_al_hJSMC @%s' % (legends[j]))

    plt.tick_params(direction='in', axis='both')    
    ax[i].legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax[i].set_xlabel ('Voltage (mV)', fontsize= labelfontsize)
    ax[i].set_ylabel (y_labels[i], fontsize= labelfontsize)
    ax[i].set_title('%s in the paper' % (prefig))

figfiles = '%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







