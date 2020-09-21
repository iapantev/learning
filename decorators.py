# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 13:30:05 2020

@author: ivpan

Decorators example
Application with dataclass for points in 3d, forming lines and triangles
"""


# #%% Simple decorator
# def doubler(func):
#   def wrapper(*args,**kwargs):
#     func(*args,**kwargs)
#     return 2*func(*args,**kwargs)
#   return wrapper

# def tripler(func):
#   def wrapper(*args,**kwargs):
#     func(*args,**kwargs)
#     return 3*func(*args,**kwargs)
#   return wrapper


# def addme(x,y):
#   return x+y

# # Define the wrapped/decorated function
# addme2x = doubler(addme)

# addme3x = tripler(addme)

#%% Dataclass standard class for data
from dataclasses import dataclass, field
from typing import List
import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import numpy as np

@dataclass
class Point:
    """Class representing a point in 3d space."""
    
    x: float
    y: float
    z: float
    coords: List[float] = field(init = False,repr = False)
    def __post_init__(self):
        self.coords = [self.x, self.y, self.z]
    def dist_to(self,other):
        """Calculate the distance between two points."""
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2)
    
@dataclass
class Line:
    """Class prepresenting a line made up of points."""
    
    points: List[Point] # Takes in a list of Point-objects
    length: float = field(init = False, repr = False)
    
    def __post_init__(self):
        """Post-initialization automatic calculation of line length."""
        self.length = self.points[0].dist_to(self.points[1])

@dataclass
class Triangle:
    vertices: List[Point]
    sides: List[Line] = field(init = False)
    perimeter: float = field(init = False)
    area: float = field(init = False)
    
    def __post_init__(self):
        self.sides = [Line([self.vertices[0],self.vertices[1]]),
                      Line([self.vertices[1],self.vertices[2]]),
                      Line([self.vertices[2],self.vertices[0]])]
        self.perimeter = sum(i.length for i in self.sides)
        self.area = math.sqrt(self.perimeter *
                              (0.5*self.perimeter-self.sides[0].length) *
                              (0.5*self.perimeter-self.sides[1].length) *
                              (0.5*self.perimeter-self.sides[2].length))
        
    def show(self):
        verts = [self.vertices[0].coords, 
                 self.vertices[1].coords, 
                 self.vertices[2].coords]
        tri = mplot3d.art3d.Poly3DCollection(verts)
        tri.set_color('r')
        tri.set_edgecolor('k')
        fig = plt.figure()
        ax = mplot3d.Axes3D(fig)
        ax.add_collection3d(tri)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim([0,10])
        ax.set_ylim([0,10])
        ax.set_zlim([0,10])

#%% Make random stuff

pt1 = Point(3.5,5.2,5.3)
pt2 = Point(0,0,0)
pt3 = Point(2,6.2,4.3)

tr1 = Triangle([pt1,pt2,pt3])
tr1.show()