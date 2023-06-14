import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilenames = ['simFig7A','simFig7B']
ofilenames = ['fig7A', 'fig7B']
# Figure name
prefig = 'Fig7'
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
t_ss =[0, 0, 0]
x_name = ['time','V']
y_name = ["Cai", "rho_vCa", ]
y_labels = ['(A) [Ca]$_i$ (nM)', r'(B) - $\rho_{vCa}$']
x_labels = ['Time (s)','Vm (mV)',]
Nai=[ 2.9836]
K_Cahalf =[3, 11, 15]
# Set subplots
subpRow, subpCol = len(prefilenames), 1

for h, plotN in enumerate(prefilenames):
    ax[h] = fig.add_subplot(subpRow, subpCol, h+1)  
    if h == 0: 
        for i in range(3):
            ofilename ='../originalData/%s%d.csv' % (ofilenames[h],i+1)
            odata = pd.read_csv(ofilename)
            ox_data = odata['x']   
            oy_data = odata['Curve1']    
            ax[h].plot(ox_data, oy_data, '.',  color=cycle[i], label = 'Bursztyn et al' ) 
            
            filename='../simulatedData/%s_%d.csv' % (prefilenames[h], i)
            data = pd.read_csv(filename)
            x_data = data[x_name[h]]-t_ss[i]      
            y_data = data[y_name[h]]*1000000   
            ax[h].plot(x_data, y_data,  color=cycle[i], label = 'K$_{Ca,1/2}$=%d mV' % K_Cahalf[i])
            ax[h].set_ylabel (y_labels[h], fontsize= labelfontsize)
            ax[h].set_xlabel (x_labels[h], fontsize= labelfontsize)
            ax[h].set_title('%s in the primary publication' % (prefig))        
        ax[h].legend(loc = 'upper center', bbox_to_anchor=(0.56, 1.0), ncol=3, fontsize=lfontsize, frameon=False) 
    else:
        for i in range(3):
            ofilename ='../originalData/%s%d.csv' % (ofilenames[h],i+1)
            odata = pd.read_csv(ofilename)
            ox_data = odata['x']   
            oy_data = odata['Curve1']    
            ax[h].plot(ox_data, oy_data, '.',  color=cycle[i], label = 'Bursztyn et al, K$_{Ca,1/2}$ = %dmV' % K_Cahalf[i]) 
            
            filename='../simulatedData/%s_%d.csv' % (prefilenames[h], i)
            data = pd.read_csv(filename)
            x_data = data[x_name[h]]      
            y_data = data[y_name[h]]   
            ax[h].plot(x_data, y_data,  color=cycle[i], label = 'K$_{Ca,1/2}$ = %dmV' % K_Cahalf[i])
            ax[h].set_ylabel (y_labels[h], fontsize= labelfontsize)
            ax[h].set_xlabel (x_labels[h], fontsize= labelfontsize) 
        
        ax[h].legend(loc = 'center right', bbox_to_anchor=(1, 0.4), fontsize=lfontsize, frameon=False)    
                   
    plt.tick_params(direction='in', axis='both')    
    

figfiles = '../%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







