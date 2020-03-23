# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:01:14 2020

@author: ivpan
Imaginary derivative example
"""

import numpy as np
import matplotlib.pyplot as plt

#%% Define derivative function
def deriv(f,x,eps=1e-10):
  """
  Function to calculate the derivative of the function f @ x

  Args:
    f (function): Function for calculating the derivative.
    x (float): Dependent variable of the function x.
    eps (TYPE, optional): Numerical tolerance. Defaults to 1e-10.

  Returns:
    float: Numerical value of f'(x).

  """
 
  return np.imag((f(x+eps*1j)-f(x))/eps)

def funci(x):
  return x**2 + 3*x + 15

def custom_der(f,x,order=1,eps=1e-10):
  if order == 1:
    der = np.imag((f(x+eps*1j)-f(x))/eps)
  if order == 2:
    der = 2*(f(x)-np.real(f(x-eps*1j)))/(eps**2)
  if order < 1 or order > 2:
    print('Undefined derivatives for requested order!')
    der = 0
  return der

# Use the custom imaginary derivative
# print(custom_der(funci,10))
# print(custom_der(funci,10,2,1e-4))

x = np.linspace(-100,100,1000)
first_num = np.array([custom_der(funci,i) for i in x])
first_anal = np.array([(2*i+3) for i in x])
rel_err = (first_num-first_anal)/first_anal

fig,ax = plt.subplots(1,3)#,subplot_kw=dict(num=[121,122],yscale=["lin","log"]))

ax[0].plot(x,funci(x))
ax[0].grid('on')
ax[0].set_title('Function')

ax[1].plot(x,first_num,'r')
ax[1].plot(x,first_anal,'k')
ax[1].grid('on')
ax[1].set_title('Derivative')

# ax[1].semilogy(x,rel_err)
ax[2].plot(x,rel_err)
ax[2].set_yscale("log")
# ax[1].set_ylim([1e-18,1e-15])
# ax[1].Axes.set_yscale('log')
ax[2].grid('on')
ax[2].set_title('Error')
plt.tight_layout()


