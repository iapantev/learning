# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:44:55 2020

@author: ivpan
"""
import unittest

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

#%% Challi
def consecutive_combo(lst1,lst2):
    grand = lst1 + lst2
    grand.sort()
    grand = [(grand[i+1]-grand[i])==1 for i in range(len(grand)-1)]
    return True if all(grand) else False

print(consecutive_combo([1,2,3], [6,5,4]))

#%% Filters
months = { "1": "A", "2": "B", "3": "C", "4": "D", "5": "E", "6": "H",
"7": "L", "8": "M", "9": "P", "10": "R", "11": "S", "12": "T" }


def fiscal_code(person):
    name,surname = person["name"],person["surname"]
    fin = []
    vowels = lambda x: x in "aeiouy"
    consons = lambda x : x not in "aeiouy"
    for word in (surname,name):
        code = list(filter(consons,word.lower())) + list(filter(vowels,word.lower())) + ["X","X","X"]
        fin = fin + code[:3]
    nxt = person["dob"].split("/")
    if person["gender"]=="M":
        if int(nxt[0])<10:
            day = '0'+nxt[0]
        else:
            day = nxt[0]
    else:
        day = str(int(nxt[0])+40)
    mth = months[nxt[1]]
    return "".join(fin).upper()+nxt[2][-2:]+mth+day

print(fiscal_code({ "name": "Brendan", "surname": "Eich", "gender": "M", "dob": "1/12/1961"}))
print(fiscal_code({ "name": "Helen", "surname": "Yu", "gender": "F", "dob": "1/12/1950"}))
print(fiscal_code({ "name": "Al", "surname": "Capone", "gender": "M", "dob": "17/1/1899"}))
print(fiscal_code({ "name": "Marie", "surname": "Curie", "gender": "F", "dob": "7/11/1867"}))

#%% Soup
def alphabet_soup(txt):
	return "".join(sorted(list(txt)))

wa = alphabet_soup("hello")

#%% Digits
import numpy as np
def is_economical(n):
    num_dig = int(np.floor(np.log10(n))+1)
    primfac = {}
    d = 2
    while d*d <= n:
        nom=0
        while (n % d) == 0:
            nom += 1
            primfac[d] = nom
            n //= d
        d += 1
    num_fac = len(primfac.keys()) + len(list(filter(lambda x: x>1,primfac.values())))
    return "Equidigital" if num_fac==num_dig else "Frugal" if num_fac<num_dig else "Wasteful"
    # return primfac, num_dig

print(is_economical(81))