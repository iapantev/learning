# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:21:04 2020

@author: ivpan

Hillel function
"""
#%% Import packages
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D

#%% Function definition
def Hillel(z,t,t0,Dh,T_avg,A0):
    d = 2*Dh*365/(2*np.pi)
    T = T_avg + A0*np.exp(-z/d)*np.sin(2.*np.pi*(t-t0)/365. -z/d -np.pi/2.)
    return T

def output_for_comsol(z,t,t0,Dh,T_avg,A0):
    outfile = open("C:\\Models\\BCs\\prefab_initial.txt",mode="w+")                    
    for depth in z:
        for time in t:
            #print(time,depth,Hillel(depth,time,t0,Dh,T_avg,A0))
            val = Hillel(depth,time,t0,Dh,T_avg,A0)
            outfile.write(f"{depth} {time} {val}\n")
    outfile.close()

def waterfall_plot(fig,ax,X,Y,Z):
    '''Input:
        fig,ax : matplotlib figure and axes to populate
        Z : n,m numpy array. Must be a 2d array even if only one line should be plotted
        X,Y : n,m array
    '''
    # Set normalization to the same values for all plots
    norm = plt.Normalize(Z.min().min(), Z.max().max())
    # Check sizes to loop always over the smallest dimension
    n,m = Z.shape
    if n>m:
        X=X.T; Y=Y.T; Z=Z.T
        m,n = n,m

    for j in range(n):
        # reshape the X,Z into pairs 
        points = np.array([X[j,:], Z[j,:]]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)        
        lc = LineCollection(segments, cmap='plasma', norm=norm)
        # Set the values used for colormapping
        lc.set_array((Z[j,1:]+Z[j,:-1])/2)
        lc.set_linewidth(2) # set linewidth a little larger to see properly the colormap variation
        line = ax.add_collection3d(lc,zs=(Y[j,1:]+Y[j,:-1])/2, zdir='y') # add line to axes

    fig.colorbar(lc) # add colorbar, as the normalization is the same for all, it doesent matter which of the lc objects we use

#%% Call function

z = np.linspace(0,15,50)
t = np.linspace(0,5*365,200)
Dh = 0.5*1e-6*24*3600
T_avg = 12
A0 = 6
t0 = 0

T = np.zeros((len(z),len(t)))
for i in range(len(t)):
    T[:,i] = Hillel(z,t[i],t0,Dh,T_avg,A0)

#%% Plotting
# fig,ax = plt.subplots(1)
# [ax.plot(T[:,i],z) for i in range(len(t))]
# ax.invert_yaxis()
# ax.grid('on')
        
#%% Waterfall plot
X,Y = np.meshgrid(t,z)
fig1 = plt.figure()
ax1 = fig1.add_subplot(111,projection='3d')
waterfall_plot(fig1,ax1,X,Y,T)
ax1.set_xlim3d(0,5*365)
ax1.set_ylim3d(0,15)
ax1.set_zlim3d(2,22)
plt.show()

#%% Output for COMSOL

#Directly output the file with temperatures for use in COMSOL
output_for_comsol(z,t,t0,Dh,T_avg,A0)