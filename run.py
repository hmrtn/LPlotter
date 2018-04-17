####################################
####  University of Washington  ####
####  Advanced Propulsion Lab   ####
####       Hans Martin          ####
####  Last Edit: Apr 17, 2018   ####
####################################


import os
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

temp = 10*1.16E4
boltz = 1.38E-23
area = 1.749E-5
elec = 1.602E-19
mass = 6.67E-26
correct = 0.004
const = 0.6*elec*area*np.sqrt(boltz*temp/mass)
window = 500
    
if 'data' in os.listdir(): 
    os.chdir('data')
    
class Folder:
    
    _CONT = []
    _DATA = []
    _RMS = []
    _AVG = []
    _DENS = []
    
    def __init__(self, name):

        self.name = name
        self.files = Folder._CONT
        self.data = Folder._DATA
        self.rms = Folder._RMS
        self.avg = Folder._AVG
        self.density = Folder._DENS
    
    def get_files(self):
        
        if not []: self.files.clear()
        for k in os.listdir(self.name):
            self.files.append(k)
    
    def get_data(self):
        
        if not []: self.data.clear()
        for j in os.listdir(self.name):
            self.data.append(np.ndfromtxt(self.name+'/'+j, delimiter = '\t'))
    
    def get_rms(self):
        
        if not []: self.rms.clear()
        for p in range(len(self.data)):
            v = self.data[p][:,1]
            self.rms.append(correct*np.sqrt(np.convolve(np.square(v), 
                            np.ones((window,))/window, mode='same')))
    
    def get_avg(self):
        
        if not []: self.avg = []
        self.avg = sum(self.rms)/ len(self.rms)
    
    def get_density(self):

        self.density = self.avg/ const

expo = dict()

for folders in os.listdir(): 

    inst = Folder(folders)
    inst.get_files()
    inst.get_data()
    inst.get_rms()
    inst.get_avg()
    inst.get_density()

    time_axis = inst.data[0][:,0]*1E6
    expo.update({inst.name : inst.density})

pd.DataFrame(expo).to_csv('../export/density_export.csv', index=False)

for key in expo.keys():
    plt.plot(time_axis, expo[key], label = key)

plt.title('Plasma Density ' + ('Comparison' if len(expo) > 1 else ''))
plt.grid( which = 'major', alpha = 0.5); plt.grid( which = 'minor', alpha = 0.2)
plt.minorticks_on()
plt.ylabel('$n_{e}$ ($m^{-3}$)'); plt.xlabel('Time ($\mu$s)')
plt.legend()
plt.show(block=True)
