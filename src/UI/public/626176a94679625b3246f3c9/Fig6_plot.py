import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilenames = ['simFig6']
ofilenames = ['fig6']
# Figure name
prefig = 'Fig6'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 6
fig = plt.figure(figsize=(fw,fh))
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 11, 12 # legend, label fontsize
t_ss = [0]
# Read data from the files
x_name = 'time'
y_name = ["Cai", "V"]
y_labels = ['[Ca]$_i$ (nM)', 'Vm (mV)']
Nai=[ 16.55]
# Set subplots
subpRow, subpCol = len(y_name), 1

for h, plotN in enumerate(y_name):
    if h ==0 :
       ax[h] = fig.add_subplot(subpRow, subpCol, h+1)
       ax[h].set_title('%s in the primary publication' % (prefig))  
       ofilename ='../originalData/%s.csv' % ofilenames[h]
       odata = pd.read_csv(ofilename)
       ox_data = odata['x']   
       oy_data = odata['Curve1']    
       ax[h].plot(ox_data, oy_data, '.',  color=cycle[0], label = 'Bursztyn et al')     
       filename='../simulatedData/%s.csv' % (prefilenames[h])
       data = pd.read_csv(filename)
       x_data = data[x_name]      
       y_data = data[y_name[h]]*1000000   
       ax[h].plot(x_data, y_data,  color=cycle[0], label = 'CellML model ' )        
    else:
       ax[h] = fig.add_subplot(subpRow, subpCol, h+1)       
       filename='../simulatedData/%s.csv' % (prefilenames[h-1])
       data = pd.read_csv(filename)
       x_data = data[x_name]      
       y_data = data[y_name[h]]   
       ax[h].plot(x_data, y_data,  color=cycle[0], label = 'V')   
             
    plt.tick_params(direction='in', axis='both')    
    ax[h].legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax[h].set_xlabel ('Time (s)', fontsize= labelfontsize)
    ax[h].set_ylabel (y_labels[h], fontsize= labelfontsize)

figfiles = '../%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







