import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilename = 'simFig13_'
# Figure name
prefig = 'Fig13'
figfile = 'sim%s.png' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 12, 10
fig = plt.figure(figsize=(fw,fh))
fig.tight_layout()
# Set subplots
subpRow, subpCol = 3, 2
ax, lns = {}, {}
lfontsize, labelfontsize = 12, 12 # legend, label fontsize
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Read data from the files
gnames = ['g_Kv', 'g_BK', 'g_Na', 'g_CaL']
fileindex = ['a', 'b', 'c', 'd', 'e']
labels= ['CellML model control','CellML model +50%','CellML model -50%',]

plotindex = [1, 2, 3, 4, 5, 6 ]

x_name = 'time'
y_name = ['V', 'Cai']

for i, ifile in enumerate(fileindex):
    for n in range(3):
       if n==0:
          filename='%s%d.csv' % (prefilename,n)
          ax[i] = fig.add_subplot(subpRow, subpCol, plotindex[i])
          ofilename ='fig13%s%d.csv' % (fileindex[i],n)
          odata = pd.read_csv(ofilename)
          ox_data = odata['x']   
          oy_data = odata['Curve1']    
          ax[i].plot(ox_data, oy_data, '.',  color=cycle[n])
       else:
          if i < 4:
             filename='%s%s%d.csv' % (prefilename,fileindex[i],n)            
          else:
             filename='%s%s%d.csv' % (prefilename,fileindex[3],n)
          if i in [0, 4]: 
                ofilename ='fig13%s%d.csv' % (fileindex[i],n)
                odata = pd.read_csv(ofilename)
                ox_data = odata['x']   
                oy_data = odata['Curve1']    
                ax[i].plot(ox_data, oy_data, '.',  color=cycle[n])

       data = pd.read_csv(filename)
       x_data = data[x_name]/1000
       if i < 4:   
          y_data = data[y_name[0]]
       else:
          y_data = data[y_name[1]]*10**6

       ax[i].plot(x_data, y_data, color=cycle[n], label = labels[n] )

    ax[i].tick_params(direction='in', axis='both')  
    if i < 4:   
          ax[i].set_ylabel ('Voltage (mV)', fontsize= labelfontsize)
          ax[i].set_title(gnames[i])
    else:
          ax[i].set_ylabel ('[Ca]$_i$ (nM)', fontsize= labelfontsize)
          ax[i].set_title(gnames[3])
          ax[i].legend(bbox_to_anchor=(1.04,1), loc="upper left", fontsize=lfontsize, frameon=False)
    if plotindex[i] in [5, 4]: 
        ax[i].set_xlabel ('time(ms)', fontsize= labelfontsize)
    else:
        ax[i].set_xticklabels([])

ax[i].set_title('%s in the paper' % (prefig))
 
    
plt.savefig(figfile)        
plt.show()




