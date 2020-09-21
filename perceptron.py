# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 19:48:33 2020

@author: ivpan
"""
import numpy as np

def sigmoid(x):
  return 1./(1. + np.exp(-x))

def sigmoid_der(x):
  return x + (1.-x)

train_inputs = np.array([[0,0,1],
                         [1,1,1],
                         [1,0,1],
                         [0,1,1]])

train_outputs = np.array([[0,1,1,0]]).T

np.random.seed(1)

syn_weigths = 2 * np.random.random((3,1)) - 1

print('Random starting synapse weights: ')
print(syn_weigths)

for iteration in range(50000):
  input_layer = train_inputs
  
  outputs = sigmoid(np.dot(input_layer, syn_weigths))
  
  error = train_outputs - outputs
  
  adjustments  = error * sigmoid_der(outputs)
  
  syn_weigths += np.dot(input_layer.T,adjustments)

print('Synaptic weigths after training')
print(syn_weigths)

print("Output after training: ")
print(outputs)