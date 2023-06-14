import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
filename = 'simFig9.csv'
# Figure name
prefig = 'Fig9'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 6
fig = plt.figure(figsize=(fw,fh))
# Set subplots
subpRow, subpCol = 2, 1
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 12, 12 # legend, label fontsize

# Read data from the files
x_name = 'time'
y_name = ['V']
y_labels = ['Voltage (mV)']

for i, varName in enumerate(y_name):   
    ax[i] = fig.add_subplot(subpRow, subpCol, i+1)  
    data = pd.read_csv(filename)
    x_data = data[x_name]/1000
    if i==1:   
       y_data = (data[varName])*10**6
    else:
       y_data = data[varName]   
    ax[i].plot(x_data, y_data,  color=cycle[0], label = 'CellML model' )

    ofilename ='fig9.csv'
    odata = pd.read_csv(ofilename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']    
    ax[i].plot(ox_data, oy_data, '.',  color=cycle[0], label = 'Poh_et_al_hJSMC')

    plt.tick_params(direction='in', axis='both')    
    #ax[i].legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax[i].set_xlabel ('Time (s)', fontsize= labelfontsize)
    ax[i].set_ylabel (y_labels[i], fontsize= labelfontsize)
    ax[i].set_title('%s in the paper' % (prefig))

figfiles = '%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







