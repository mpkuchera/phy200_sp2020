# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:27:28 2020

Final Project Physics 200
Professor: Dr. Kuchera
Author: Louisa Winkler

The Program is animating a skier on a slope and determines whether
the skier comes to a stop on the slope

@author: lwink
"""
import math 
import numpy as np
from scipy.constants import g
import vpython as vp
from vpython import *

# the interval for the slope on which the skier is tested 
# the skier start at interval1. If he slides until interval2 the slope is 
# managable
interval1 = 2
interval2 = 30
        
# constants 
m = 70          #kg 
my = 0.05       #friction coefficient, (waxed Ski on Snow kinetic = 0.05)
rho = 1.225     #kg/m^3  air density
A = 0.5         #m^2 surface area skier estimated to 0.5
c = 1.1         #drag coefficient for a skier 

#accuracy
N = 10000
h = (interval2-interval1)/N

class Skierc:
    
    """ Class that includes a function to define the slope and animates the 
        skiers movement on the given interval 
        
        Parameter: vstart: start velocity of the skier at interval1
        
        Return: a string whether or not the slope is manageable and the maximal 
                velocity during the skiers ride
    """
    
    def __init__(self, vstart):
        self.vo = vstart
        return 
    
    def f(self, x): 
    
        """ evaluates the function (later maybe as input) 
            and returns the f(x) value. This is used to calculate the derivative
        """
        
        return 10*math.sin(x) * x**(-0.3)  #example function
        
    
    def theta(self, x):
        """ 
        Calculates the derivative of the function 
            
        Parameters: x - position of the skier on the x-axes
        
        Returns the angle Theta as the arctan(fp(x))
        """
        # implements derivative method to find derivative value
        fp = (self.f(x + h)-self.f(x))/h 
        Theta = (np.arctan(fp)) # in radian
        
        return Theta
    
    
    def force_friction(self, x):
        """ function that calculates the kinetic friction at the skier's position
            Parameter: x - position of skier
            Return: kinetic friction fr
        """
        return my * math.cos(self.theta(x)) * m * g
    
    def force_grav(self, x):
        """ function that calculates the force in the skier's direction 
            caused by gravitation
            Parameter: x - position of skier
            Return: gravitation force
        """
        return math.sin(self.theta(x))*m*(-g)
    
    def force_drag(self, v):
        """ function that calculates the drag on the skier
            Parameter: v - velocity of skier (depends only on velocity)
            Return: drag force
        """
        c = 1.1                     #for skier maybe change
        return 1/2*rho*c*A*v**2
    
    
    def v2(self, xstart, vstart, tstart, v, t):
        """ function that calculates the velocity of the skier"""
        
        return -(t-tstart)*rho*A/(2*m)*v**2 + vstart + \
            h*(self.force_grav(xstart)-self.force_friction(xstart))/m 
                
    def runge_kutta(self):
        """ function applies RK4 
            Return: xpoints: list for x points of the skier
                    foffxpoints:list for y points of the skier
                    vpython will use the two lists to animate the skier 
                    on the slope
        """
        
        tpoints = []        # list for time points 
        vpoints = []        # list for velocity points
        xpoints = []        # list for x points
        foffxpoints = []    # list for y points of the skier
        vstart = self.vo    #vstart is start velocity entered by the user
        xstart = interval1  #start position x
        
        #solve DGL with Runge Kutta
        for t in np.arange(0,10000,h): 
            tpoints.append(t)
            vpoints.append(vstart)
            xpoints.append(xstart)
            foffxpoints.append(self.f(xstart))
            # calculate Runge kutta coefficients 
            k1 = self.v2(xstart, vstart, t, vstart, t)
            k2 = self.v2(xstart, vstart, t,  vstart + 0.5*k1, t+0.5*h)
            k3 = self.v2(xstart, vstart, t,  vstart + 0.5*k2, t+0.5*h)
            k4 = self.v2(xstart, vstart, t, vstart + k3, t+h)
            
            vnext = (k1+2*k2+2*k3+k4)/6
        
            #stop when v becomes zero (skier stops)
            if vnext < 0: 
                print('The skier stops at position x = ', format(xstart, '.2f'))
                break
            
            #traveled distance
            d = (vstart + vnext)/2 * h
            #convert with angle to next position x 
            dx = math.cos(self.theta(xstart))*d
            # the next position x ist the previous one with the traveled one 
            # under average velocity in a time h
            xnext = xstart + dx
            
            # if the skier does not stop on the slope, the slope is manageable
            if xnext >= interval2:
                print('The skier can manage the slope in the given interval')
                break 
        
            # define for next loop iteration the next velocity and position 
            # become the start values
            vstart = vnext
            xstart = xnext
            
        # determine the maximal speed
        v_max = format(max(vpoints), '.2f')
        print('the skier reaches a maximal speed of ', v_max, 'm/s')
        
        return xpoints, foffxpoints
    
    def plot_slope(self): 
        """ returns two lists to plot the function 
        """
        x = np.linspace(interval1, interval2,N)
        y = []
        for i in x:
            y.append(self.f(i))
        return x,y
    
    def animation(self):
        # get the lists to animate the skiers movement
        [xpoints, foffxpoints] = self.runge_kutta()
        # get the lists to model the slope
        [x, y] = self.plot_slope()
    
        # define canvas where the animation takes place
        mountain = vp.canvas(title = 'GOOO Skier', center = vp.vector(20,0,0),\
            background = vp.color.white, width = 1000, hight = 200)
        skier = vp.sphere(canvas = mountain , radius = .1, color = vp.color.black)
        
        # models the slope in the animation 
        for i in range(len(x)):
            slope = vp.sphere(canvas = mountain, radius = 0.01, \
                color = vp.color.red, pos = vp.vector(x[i], y[i]-0.1, 0))
        vp.rate(1)
        
        x = 100
        # models the skiers movement
        for i in range(len(xpoints)):
            vp.rate(x)
            skier.pos = vp.vector(xpoints[i], foffxpoints[i], 0)
            
        
    
        
        
        
        
        
        
        
    
