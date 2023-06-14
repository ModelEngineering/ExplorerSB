import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilenames = ['simFig4A','simFig4B']
ofilenames = ['fig4A', 'fig4B']
# Figure name
prefig = 'Fig4'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 8
fig = plt.figure(figsize=(fw,fh))
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 11, 12 # legend, label fontsize

t_ss = 0.2
# Read data from the files
x_name = 'time'
y_name = 'Cai'
y_labels = ['(A) [Ca]$_i$ (nM)','(B) [Ca]$_i$ (nM)',]
Nai=[ 2.9836]
Vtest = [-20, 20]
# Set subplots
subpRow, subpCol = len(prefilenames), 1

for h, plotN in enumerate(prefilenames):
    ax[h] = fig.add_subplot(subpRow, subpCol, h+1)    
    ofilename ='../originalData/%s.csv' % ofilenames[h]
    odata = pd.read_csv(ofilename)
    ox_data = odata['x']   
    oy_data = odata['Curve1']    
    ax[h].plot(ox_data, oy_data, '.',  color=cycle[0], label = 'Bursztyn et al, Nai=2.9836 mM') 
    
    for i, iNai in enumerate(Nai):
        filename='../simulatedData/%s_%d.csv' % (prefilenames[h],i)
        data = pd.read_csv(filename)
        x_data = data[x_name]- t_ss      
        y_data = data[y_name]*1000000   
        ax[h].plot(x_data, y_data,  color=cycle[i], label = 'V=%d mV, Nai=%.4f mM' % (Vtest[h],iNai))      
           
    plt.tick_params(direction='in', axis='both')    
    ax[h].legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax[h].set_xlabel ('Time (s)', fontsize= labelfontsize)
    ax[h].set_ylabel (y_labels[h], fontsize= labelfontsize)
    if h == 0:
       ax[h].set_title('%s in the primary publication' % (prefig))

figfiles = '../%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







