import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilenames = ['simFig11A','simFig11B']
ofilenames = ['fig11A', 'fig11B']
# Figure name
prefig = 'Fig11'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 8
fig = plt.figure(figsize=(fw,fh))
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 11, 12 # legend, label fontsize
duration = [160]
# Read data from the files
t_ss =[0, 0]
x_name = ['time','time']
y_name = ["stress","Cai"]
y_labels = ['(A) Stress (%)', '(A) [Ca]$_i$ (nM)','(B) Stress (%)', '(B) [Ca]$_i$ (nM)']
x_labels = ['Time (s)','Time (s)',]
Nai=[ 16.55]
# Set subplots
subpRow, subpCol = len(prefilenames)*2, 1

for h, plotN in enumerate(prefilenames):
         
    for i in range(2):
        ax[h*2+i] = fig.add_subplot(subpRow, subpCol, h*2+i+1)
        ofilename ='../originalData/%s%d.csv' % (ofilenames[h],i+1)
        odata = pd.read_csv(ofilename)
        ox_data = odata['x']   
        oy_data = odata['Curve1']    
        ax[h*2+i].plot(ox_data, oy_data, '.',  color=cycle[i], label = 'Bursztyn et al') 
        
        filename='../simulatedData/%s.csv' % (prefilenames[h])
        data = pd.read_csv(filename)
        x_data = data[x_name[i]]-t_ss[i]
        if i ==0:
            y_data = data[y_name[i]]/0.8*100
        else:      
            y_data = data[y_name[i]]*1000000
            ax[h*2+i].set_xlabel (x_labels[i], fontsize= labelfontsize)

        ax[h*2+i].plot(x_data, y_data,  color=cycle[i], label = 'CellML')
        ax[h*2+i].set_ylabel (y_labels[h*2+i], fontsize= labelfontsize)
        
        if h+i == 0:
            ax[h*2+i].set_title('%s in the primary publication' % (prefig))
        
        ax[h*2+i].legend(loc = 'best', fontsize=lfontsize, frameon=False)
                
    plt.tick_params(direction='in', axis='both')    
    

figfiles = '../%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







