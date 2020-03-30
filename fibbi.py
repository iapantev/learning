# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:13:42 2020

@author: ivpan
"""

def fibonacci(n):
  # Function with simultaneous updating of states
  x,y = 0,1
  for i in range(n):
    print(x)
    x,y = y, x+y

fibonacci(15)