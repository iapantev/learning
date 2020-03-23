# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:08:56 2020

@author: ivpan

Sudoku solver using recursion and backtracking
"""

import numpy as np


grid = [[5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]]

def possible(y,x,n):
  global grid
  # Check row
  for i in range(0,9):
    if grid[y][i] == n:
      return False
  # Check column
  for i in range(0,9):
    if grid[i][x] == n:
      return False
  # Check square
  x0 = (x//3)*3
  y0 = (y//3)*3
  for i in range(0,3):
    for j in range(0,3):
      if grid[y0+i][x0+j] == n:
        return False
  return True

def solve():
  global grid
  # Find an empty cell to start
  for y in range(9):
    for x in range(9):
      if grid[y][x] == 0:
        # Try to place a number there
        for n in range(1,10):
          # If possible, place that number
          if possible(y,x,n):
            grid[y][x] = n
            # Find another empty position and solve other square
            solve()
            # Back-tracking i.e. when solve fails, leave the square empty
            grid[y][x] = 0
        return
  print(np.matrix(grid))
  input('More solutions?')
  
solve()