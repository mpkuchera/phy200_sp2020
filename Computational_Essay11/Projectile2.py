#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:46:33 2020

@author: daniel
"""
import pylab as plt
import numpy as np
import math

h = 1
radius = 4
rho = 2.5
A = np.pi*radius**2
M = rho * h *radius**2         # Mass of projectile in kg
g = 980          # Acceleration due to gravity (m/s^2)
V = 1000         # Initial velocity in cm/s
beta = 0.0       # Angle of initial velocity in degrees
alpha = 0.10
Cd = 0.5       # Drag coefficient
dt = 0.01        # time step in s
rair = 0.00122



# Set up the lists to store variables
# Initialize the velocity and position at t=0

t = [0]                         # list to keep track of time
x = [0]                         # list for x and y position
y = [50]


# Drag force
drag=0.5*rair*Cd*A*(V**2)                      # drag force 

r = [0,50,V*np.cos(beta),V*np.sin(beta)]


    
def f(r,beta):
    
    V = np.sqrt(r[2]**2 + r[3]**2)
    drag=0.5 * rair * Cd * radius**2 * (V**2)
    
    dvx = -(drag*np.cos(beta))/M
    dvy = -g-(drag*np.sin(beta)/M)
    dx = r[2]
    dy = r[3]
    
    return np.array([dx,dy,dvx,dvy])


def move(r,x,y,alpha,beta):
    """
    Recursive helper which appends x and y positions to x[] and y[] for one
    skip, then calculates the initial conditions for the next skip. Continues
    until the stopping condition is met.
    
    param:
        r (numpy array) - x position, y position, x velocity, y velocity
        x (list)- x coordinates
        y (list)- y coordinates
        alpha (int) - angle of stone relative to the horizon
        beta (int) - angle of initial velocity
    """

    
    ymax = 0.0

    
    while y[-1] >= 0:
        if(y[-1] > ymax):
            ymax = y[-1]
        
        k1 = dt*f(r,beta)
        k2 = dt*f(r+k1/2,beta)
        k3 = dt*f(r+k2/2,beta)
        k4 = dt*f(r+k3,beta)
        r = r + (k1 + 2*k2 + 2*k3 + k4)/6
        
        x.append(r[0])
        y.append(r[1])
        t.append(t[-1]+dt)
        
        
        
        
    #collision
    
    V = np.sqrt(r[2]**2 + r[3]**2)
    beta1 = math.atan(r[3]/r[2])
    vout = V*np.cos(-beta1+alpha)
    vxout = vout*np.cos(alpha)
    vyout = vout*np.sin(alpha)
    
    #only continue if the stone will be able to leave the water
    if(vyout**2 - 2*g*radius*np.sin(alpha) > 0):
        
        vygrav = np.sqrt(vyout**2 - 2*g*radius*np.sin(alpha))
    
        vout = np.sqrt(vygrav**2 + vxout**2)
        beta1 = math.atan(vygrav/vxout)
    
        #remov the last values in each list(except x). Replace with the 
        #   values found by calculating the collision
        y.pop()
        y.append(0.0)
        r[1] = 0.0
        r[3] = vygrav
        r[2] = vxout
        
    
        if(ymax > 0.5):
            move(r,x,y,alpha, beta1)
    
    

def main():
    move(r,x,y,alpha,beta)
    plt.plot(x,y)
    print(x[-1])
    
    
        
if __name__ == '__main__':
    main()