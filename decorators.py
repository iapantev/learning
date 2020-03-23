# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:30:05 2020

@author: ivpan

Decorators example
"""

#%% Simple decorator
def doubler(func):
  def wrapper(*args,**kwargs):
    func(*args,**kwargs)
    return 2*func(*args,**kwargs)
  return wrapper

def tripler(func):
  def wrapper(*args,**kwargs):
    func(*args,**kwargs)
    return 3*func(*args,**kwargs)
  return wrapper


def addme(x,y):
  return x+y

# Define the wrapped/decorated function
addme2x = doubler(addme)

addme3x = tripler(addme)