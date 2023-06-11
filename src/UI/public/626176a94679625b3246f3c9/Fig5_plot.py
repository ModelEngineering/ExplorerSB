import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# The prefix of the saved output file name 
prefilenames = ['simFig5A','simFig5B']
ofilenames = ['fig5AJ_CaPump', 'fig5AJ_NaCa','fig5BJ_CaPump','fig5BJ_NaCa','fig5BJ_VOCC']
# Figure name
prefig = 'Fig5'
figfile = 'sim%s' % prefig
# Set figure dimension (width, height) in inches.
fw, fh = 6, 8
fig = plt.figure(figsize=(fw,fh))
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 11, 12 # legend, label fontsize
t_ss = [16, 0]
duration = [0, 0.2]
# Read data from the files
x_name = 'time'
y_name = ["J_CaPump", "J_NaCa", "J_VOCC"]
y_labels = ['(A) J$_{Ca^{2+}}$ (nM/s)', '(B) J$_{Ca^{2+}}$ (nM/s)']
Nai=[ 16.55, 2.9836]
# Set subplots
subpRow, subpCol = len(prefilenames), 1

for h, plotN in enumerate(prefilenames):
    ax[h] = fig.add_subplot(subpRow, subpCol, h+1)  
    if h == 0: 
       ofilename ='../originalData/%s.csv' % ofilenames[h]
       odata = pd.read_csv(ofilename)
       ox_data = odata['x']   
       oy_data = odata['Curve1']    
       ax[h].plot(ox_data, oy_data, '.',  color=cycle[0], label = 'Bursztyn et al, J$_{Ca,Pump}$') 
       ofilename ='../originalData/%s.csv' % ofilenames[h+1]
       odata = pd.read_csv(ofilename)
       ox_data = odata['x']   
       oy_data = odata['Curve1']    
       ax[h].plot(ox_data, oy_data, '.',  color=cycle[1], label = 'Bursztyn et al, J$_{Na/Ca}$ ') 
       
       filename='../simulatedData/%s.csv' % (prefilenames[h])
       data = pd.read_csv(filename)
       x_data = data[x_name]      
       y_data = data[y_name[0]]*1000000   
       ax[h].plot(x_data, y_data,  color=cycle[0], label = 'J$_{Ca,Pump}$')
       y_data = data[y_name[1]]*1000000   
       ax[h].plot(x_data, y_data,  color=cycle[1], label = 'J$_{Na/Ca}$') 
   
    else:
       ofilename ='../originalData/%s.csv' % ofilenames[h+1]
       odata = pd.read_csv(ofilename)
       ox_data = odata['x']   
       oy_data = odata['Curve1']    
       ax[h].plot(ox_data, oy_data, '.',  color=cycle[0], label = 'Bursztyn et al, J$_{Ca,Pump}$') 
       ofilename ='../originalData/%s.csv' % ofilenames[h+2]
       odata = pd.read_csv(ofilename)
       ox_data = odata['x']   
       oy_data = odata['Curve1']    
       ax[h].plot(ox_data, oy_data, '.',  color=cycle[1], label = 'Bursztyn et al, J$_{Na/Ca}$') 
       ofilename ='../originalData/%s.csv' % ofilenames[h+3]
       odata = pd.read_csv(ofilename)
       ox_data = odata['x']   
       oy_data = odata['Curve1']    
       ax[h].plot(ox_data, oy_data, '.',  color=cycle[2], label = 'BBursztyn et al, J$_{VOCC}$') 
       
       filename='../simulatedData/%s.csv' % (prefilenames[h])
       data = pd.read_csv(filename)
       x_data = data[x_name]- t_ss[h]      
       y_data = data[y_name[0]]*1000000   
       ax[h].plot(x_data, y_data,  color=cycle[0], label = 'J$_{Ca,Pump}$') 
       y_data = data[y_name[1]]*1000000   
       ax[h].plot(x_data, y_data,  color=cycle[1], label = 'J$_{Na/Ca}$') 
       y_data = data[y_name[2]]*1000000   
       ax[h].plot(x_data, y_data,  color=cycle[2], label = 'J$_{VOCC}$') 
                
    plt.tick_params(direction='in', axis='both')    
    ax[h].legend(loc = 'best', fontsize=lfontsize, frameon=False)
    ax[h].set_xlabel ('Time (s)', fontsize= labelfontsize)
    ax[h].set_ylabel (y_labels[h], fontsize= labelfontsize)
    if h == 0:
       ax[h].set_title('%s in the primary publication' % (prefig))

figfiles = '../%s.png' % (figfile)
plt.savefig(figfiles)        
plt.show()







