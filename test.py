# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:44:55 2020

@author: ivpan
"""

class IceCreamMachine:
  
  def __init__(self,ingredients,toppings):
    self.ingredients = ingredients
    self.toppings = toppings
    
  def scoops(self):
    skp = []
    for ingredient in self.ingredients:
      for topping in self.toppings:
        skp.append([topping,ingredient])
    return skp
  
machine = IceCreamMachine(['vanilla','chocolate'],['chocolate sauce'])
print(machine.scoops())

machine2 = IceCreamMachine([],[])
print(machine2.scoops())

#%%
files = {
        'Input.txt': 'Randy',
        'Code.py': 'Stan',
        'Output.txt': 'Randy'
        }

def group_by_owners(files):
    owners = {}
    for file,owner in files.items():
      try:
        owners[owner].append(file)
      except:
        owners[owner] = [file]
    return owners

print(group_by_owners(files))

#%% 

def find_missing(x,y):
  if len(x)>=len(y):
    out = x[not x==y]
  else:
    out = y[not y==x]
  return out

print(find_missing([4,5,6,7],
                   [4,5,6,7,8]))