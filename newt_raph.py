# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:39:59 2019

@author: ivpan

Newton-Raphson method example
"""
#%% Import packages
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

#%% Define functions
def eq1(x,y):
  return 1*x**-2 + 3*y**3

def eq2(x,y):
  return 1*x**1 - 2*y**1

def der(x,y):
  eps = 1e-10
  d1dx = np.imag(eq1(x+eps*1j,y))/eps
  d1dy = np.imag(eq1(x,y+eps*1j))/eps

  d2dx = np.imag(eq2(x+eps*1j,y))/eps
  d2dy = np.imag(eq2(x,y+eps*1j))/eps
  return np.array([[d1dx,d1dy],[d2dx,d2dy]],dtype='float64')

#%% Initial guesses
vector = np.array([2,2],dtype='float64')
tol = 1
its = 0
error = []
vector_hist = []

#%% Newton-Raphson solution
while(tol>1e-8):
  funct =  np.array([eq1(vector[0],vector[1]),eq2(vector[0],vector[1])])
  jac = der(vector[0],vector[1])
  vector = vector - np.dot(np.linalg.inv(jac),funct)
  vector_hist.append(vector)
  tol = np.linalg.norm(np.matmul(np.linalg.inv(jac),funct))
  error.append(tol)
  its = its + 1

#%% Plotting
xs = [vector_hist[i][0] for i in range(its)]
ys = [vector_hist[j][1] for j in range(its)]
its = [i+1 for i in range(its)]

fig,ax = plt.subplots(2)
ax[0].plot(its,error)
ax[0].set_yscale("log")
ax[0].grid("on")


ax[1].plot(xs,ys)
#ax[1].set_xscale("log")
#ax[1].set_yscale("log")
ax[1].grid()
for x,y,it in zip(xs,ys,its):

    label = "{:}".format(it)

    ax[1].annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center
del x,y,xs,ys
