import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilenames = ['simFig12']
ofilenames = ['fig12A', 'fig12B','fig12C']
# Figure name
prefig = 'Fig12'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 8
fig = plt.figure(figsize=(fw,fh))
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 11, 12 # legend, label fontsize
# Read data from the files
x_name = ['time']
y_name = ['V','Cai','stress',]
y_labels = ['(A) Vm (mV)','(B) [Ca]$_i$ (nM)','(C) Stress (%)', ]
x_labels = ['Time (s)','Time (s)','Time (s)',]

# Set subplots
subpRow, subpCol = len(y_name), 1

for h, plotN in enumerate(prefilenames):         
    for i in range(3):
        ax[h*2+i] = fig.add_subplot(subpRow, subpCol, h*2+i+1)
        ofilename ='../originalData/%s.csv' % (ofilenames[i])
        odata = pd.read_csv(ofilename)
        ox_data = odata['x']   
        oy_data = odata['Curve1']    
        ax[h*2+i].plot(ox_data, oy_data, '.',  color=cycle[i], label = 'Bursztyn et al') 
        
        filename='../simulatedData/%s.csv' % (prefilenames[h])
        data = pd.read_csv(filename)
        x_data = data[x_name[h]]
        if i ==1:
            y_data = data[y_name[i]]*1000000            
        elif i ==2:      
            y_data = data[y_name[i]]/max(data[y_name[i]])*100
            ax[h*2+i].set_xlabel (x_labels[i], fontsize= labelfontsize) 
        else:
            y_data = data[y_name[i]]           

        ax[h*2+i].plot(x_data, y_data,  color=cycle[i], label = 'CellML')
        ax[h*2+i].set_ylabel (y_labels[i], fontsize= labelfontsize)
        
        if h+i == 0:
            ax[h*2+i].set_title('%s in the primary publication' % (prefig))
    
        ax[h*2+i].legend(loc = 'best', fontsize=lfontsize, frameon=False)

    plt.tick_params(direction='in', axis='both')    
    

figfiles = '../%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







