import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig10'
# Figure name
prefig = 'Fig10'
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
x_name = 'Time'
y_name = ['Iion']
current= r'$I_{ion}$'
y_labels = ['Current %s' % current]
Vtest = range (-5, 25, 5)
suffix = ['h','g', 'f', 'e', 'd', 'c', 'b', 'a']
T=297
Cai=5.38843941249284e-5*1000000
Nai= 40
ax[0] = fig.add_subplot(subpRow, subpCol, 1) 
for i, V in enumerate(Vtest): 
    filename='%s_%d.csv' % (prefilename,i)     
    data = pd.read_csv(filename)
    x_data = data[x_name]-2000
    y_data = data[y_name]  
    ax[0].plot(x_data, y_data,  color=cycle[i%7], label = 'CellML@ %d mV, T=%dK' % (V,T))
   
    if i < len(suffix):
       ofilename ='fig10(-70)_%s.csv' % suffix[i]
       odata = pd.read_csv(ofilename)
       ox_data = odata['x']   
       oy_data = odata['Curve1']    
       ax[0].plot(ox_data, oy_data, '.',  color=cycle[i], label = 'Poh_et_al_hJSMC')

    plt.tick_params(direction='in', axis='both') 
    ax[0].legend(loc = 'best', fontsize=lfontsize, frameon=False)

ax[0].set_xlabel ('Time (ms)', fontsize= labelfontsize)
ax[0].set_ylabel (y_labels[0], fontsize= labelfontsize)
ax[0].set_title('%s in the paper @$Ca_i$=%.4f nM, $Na_i$=%.2f mM, T=%dK' % (prefig, Cai, Nai, T)) 

figfiles = '%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







