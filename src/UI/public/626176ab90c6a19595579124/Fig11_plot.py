import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
filename = 'simFig11_0.csv'
# Figure name
prefig = 'Fig11'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 8, 6
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
y_name = ['Iion']
current= r'$I_{ion}$'
y_labels = ['Normalized Current %s' % current]
Cai= 0.0001
Nai= 10.5731241425458
T=297
for i, varName in enumerate(y_name):   
    ax[i] = fig.add_subplot(subpRow, subpCol, i+1)  
    data = pd.read_csv(filename)
    x_data = data[x_name]
    y_data = data[varName]
    ny_data=y_data/max(abs(y_data))   
    ax[i].plot(x_data, ny_data,  color=cycle[1], label = 'CellML@$Ca_i$=$Ca_o$=%.4f nM, $Na_i$=%.2f mM, T=%dK' % (Cai, Nai,T))

    ofilename ='fig11.csv' 
    odata = pd.read_csv(ofilename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']    
    ax[i].plot(ox_data, oy_data, '.',  color=cycle[0], label = 'Poh_et_al_hJSMC')

    plt.tick_params(direction='in', axis='both')    
    ax[i].legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax[i].set_xlabel ('Voltage (mV)', fontsize= labelfontsize)
    ax[i].set_ylabel (y_labels[i], fontsize= labelfontsize)
    ax[i].set_title('%s in the paper' % (prefig))

figfiles = '%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







