import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilenames = ['simFig8A','simFig8B']
ofilenames = ['fig8A', 'fig8B']
# Figure name
prefig = 'Fig8'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 7, 10
fig = plt.figure(figsize=(fw,fh))
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 10, 12 # legend, label fontsize
duration = [160]
# Read data from the files
t_ss =[0, 0, 0, 0, 0]
x_name = ['time','Nai']
y_name = ["Cai", "J_NaCa", ]
y_labels = ['(A) [Ca]$_i$ (nM)', '(B) $J_{Na/Ca}$ (nM/s)']
x_labels = ['Time (s)','Nai (mM)',]
Nai=[2.9836, 10, 20, 30, 45]
Cai=[200, 450, 700]
# Set subplots
subpRow, subpCol = len(prefilenames), 1

for h, plotN in enumerate(prefilenames):
    ax[h] = fig.add_subplot(subpRow, subpCol, h+1)  
    if h == 0: 
        for i in range(5):
            ofilename ='../originalData/%s%d.csv' % (ofilenames[h],i+1)
            odata = pd.read_csv(ofilename)
            ox_data = odata['x']   
            oy_data = odata['Curve1']    
            ax[h].plot(ox_data, oy_data, '.',  color=cycle[i], label = '[Na]$_i$=%.2f mM' % Nai[i]) 
            
            filename='../simulatedData/%s_%d.csv' % (prefilenames[h], i)
            data = pd.read_csv(filename)
            x_data = data[x_name[h]]-t_ss[i]      
            y_data = data[y_name[h]]*1000000   
            ax[h].plot(x_data, y_data,  color=cycle[i], label = '[Na]$_i$=%.2f mM' % Nai[i])
            ax[h].set_ylabel (y_labels[h], fontsize= labelfontsize)
            ax[h].set_xlabel (x_labels[h], fontsize= labelfontsize)
            ax[h].set_title('%s in the primary publication' % (prefig))
        ax[h].legend(loc = 'upper center', bbox_to_anchor=(0.32, 1.04), ncol=2, fontsize=lfontsize, frameon=False)
    else:
        for i in range(3):
            ofilename ='../originalData/%s%d.csv' % (ofilenames[h],i+1)
            odata = pd.read_csv(ofilename)
            ox_data = odata['x']   
            oy_data = odata['Curve1']    
            ax[h].plot(ox_data, oy_data, '.',  color=cycle[i], label = 'Bursztyn et al, [Ca]$_i$ = %dmM' % Cai[i]) 
            
            filename='../simulatedData/%s_%d.csv' % (prefilenames[h], i)
            data = pd.read_csv(filename)
            x_data = data[x_name[h]]      
            y_data = data[y_name[h]]*1000000   
            ax[h].plot(x_data, y_data,  color=cycle[i], label = '[Ca]$_i$ = %dmM' % Cai[i])
            ax[h].set_ylabel (y_labels[h], fontsize= labelfontsize)
            ax[h].set_xlabel (x_labels[h], fontsize= labelfontsize)      
        ax[h].legend(loc = 'best', fontsize=lfontsize, frameon=False)

    plt.tick_params(direction='in', axis='both')    
    

figfiles = '../%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







