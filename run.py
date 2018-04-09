'''
Hans Martin
University of Washington
APL

Last Edited: April 8, 2018
'''

import os
import numpy as np
import matplotlib.pyplot as plt                                   

'''
CONSTANTS
'''
k = 1.38E-23
T = 10*1.16E4
area = 1.749E-5
e = 1.602E-19
mass = 6.67E-26
crctn = 0.004
c = (0.6*e*area*np.sqrt(k*T/mass))
N = 500

'''
RMS, mean, density functions
'''
def rms(v):
    rms = crctn*np.sqrt(np.convolve(
        np.square(v), np.ones((N,))/N, mode='same'))
    return(rms)

def mean(rms): 
    for i in range(0,len(RMS)):
        m =+ RMS[i]/len(RMS)
    return(m)

density = []
def dens(mean):
    d = np.divide(mean, c, 
        out=np.zeros_like(mean), where=c!=0)
    density.append(d)
    return(d)

if (os.getcwd != 'data'): 
    os.chdir('data')

dirpath = {}
for f in os.listdir():
    dirpath[f] = []

for f, data in dirpath.items():
    for t in os.listdir(f):
        data.append(t)

vt = []
for f, data in dirpath.items():
    df = []
    for i in data:
        df.append(np.ndfromtxt(
            f+'/'+i, delimiter='\t'))
    vt.append(df)

'''
vt[folder][txt file][time, voltage]
'''
RMS = []
for k in range(0,len(vt)):
    for i in range(0,len(vt[k])):
        RMS.append(rms(vt[k][i][:,1]))
        t = vt[k][i][:,0]

    plt.figure()
    plt.ion()
    for r in range(0,len(RMS)):
        plt.plot(t,RMS[r])
    plt.title(str(os.listdir()[k])+' RMS')
    plt.xlabel('Seconds')

    plt.figure()
    plt.ion()
    plt.plot(t,mean(RMS))
    plt.title(str(os.listdir()[k])+' Average')
    plt.xlabel('Seconds')

    plt.figure()
    plt.ion()
    plt.plot(t,dens(mean(RMS)))
    plt.title(str(os.listdir()[k])+' Density')
    plt.xlabel('Seconds')
    plt.ylabel('$m^-3$')

'''
PLOT MULTIPLE DENSITY PLOTS IFF DATA > 1
'''
if len(vt) > 1:
    plt.figure()
    for h in range(0, len(density)):
        plt.ion()
        plt.plot(t, density[h], label=str(os.listdir()[h]))
    plt.title('Density Comparison')
    plt.legend()
    plt.xlabel('Seconds')
    plt.ylabel('$m^-3$')


plt.show(block=True)

