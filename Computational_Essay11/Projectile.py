#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Daniel Valmassei
Time Spent: 6 hours
Created: 3-26-2020
Last Edited: 4-6-2020

"""
import numpy as np
import math
import pylab as plt


#Model parameters

h = 1
r = 4
rho = 2.5
A = math.pi*r**2
M = rho * h *r**2         # Mass of projectile in kg
g = 980          # Acceleration due to gravity (m/s^2)
V = 1000         # Initial velocity in m/s
beta = 0.0       # Angle of initial velocity in degrees
alpha = 0.1
Cd = 0.5       # Drag coefficient
dt = 0.01        # time step in s
rair = 0.00122



# Set up the lists to store variables
# Initialize the velocity and position at t=0

t = [0]                         # list to keep track of time
vx = [V*np.cos(beta)]  # list for velocity x and y components
vy = [V*np.sin(beta)]
x = [0]                         # list for x and y position
y = [50]
skipCount = 0
counter = 0

# Drag force
drag=0.5*rair*Cd*A*(V**2)                      # drag force 

# Acceleration components
ax = [-(drag*np.cos(beta))/M ]          
ay = [-g-(drag*np.sin(beta)/M) ]


def move(x,y,vx,vy,counter,alpha,beta,skipCount):
    """
    Recursive helper which appends x and y positions to x[] and y[] for one
    skip, then calculates the initial conditions for the next skip. Continues
    until the stopping condition is met.
    
    param:
        x (list)- x coordinates
        y (list)- y coordinates
        vx (list)- x velocities
        vy (list)- y velocities
        counter (int) - current last index of x, y, vx, and vy
        alpha (int) - angle of stone relative to the horizon
        SkipCount (int) - number of skips that have occured
    """
    ymax = 0
    
    def xvel(counter):
        """
        Calculate the x velocity
        
        param:
            counter (int) - last index of vx
            
        return:
            int - next x velocity
        """
        return vx[counter]+dt*ax[counter]
    
    def yvel(counter):
        """
        Calculate the y velocity
        
        param:
            counter (int) - last index of vy
            
        return:
            int - next y velocity
        """
        return vy[counter]+dt*ay[counter]
    
    def xpos(counter):
        """
        Calculate the x position
        
        param:
            counter (int) - last index of x
            
        return:
            int - next x position
        """
        return x[counter]+dt*vx[counter]
    
    def ypos(counter):
        """
        Calculate the y position
        
        param:
            counter (int) - last index of y
            
        return:
            int - next x position
        """
        return y[counter]+dt*vy[counter]


    # Use Euler method to update variables
    while (y[-1] >= 0):                   # Check that the last value of y is >= 0
        t.append(t[counter]+dt)                # increment by dt and add to the list of time 
    
    
    
        # Update velocity
        vx.append(xvel(counter))  
        vy.append(yvel(counter))

        # Update position
        x.append(xpos(counter))    
        y.append(ypos(counter))
        
        #keep track of the ymax for stopping condition
        if(ypos(counter) > ymax):
            ymax = ypos(counter)

        # With the new velocity calculate the drag force and update acceleration
        vel = np.sqrt(vx[counter+1]**2 + vy[counter+1]**2)   # magnitude of velocity
        drag = 0.5*rair*Cd*A*(vel**2)                                   # drag force 
        ax.append(-(drag*np.cos(beta))/M)     
        ay.append(-g-(drag*np.sin(beta)/M))
                
    
        # Increment the counter
        counter = counter +1
    
    
    #collision
    beta1 = math.atan(vy[counter]/vx[counter])
    vout = vel*math.cos(-beta1+alpha)
    
    vxout = vout*math.cos(alpha)
    vyout = vout*math.sin(alpha)
    
    #only continue if the stone will be able to leave the water
    if(vyout**2 - 2*g*r*math.sin(alpha) > 0):
        skipCount += 1
        
        vygrav = math.sqrt(vyout**2 - 2*g*r*math.sin(alpha))
    
        vout = math.sqrt(vygrav**2 + vxout**2)
        beta1 = math.atan(vygrav/vxout)
    
        #remov the last values in each list(except x). Replace with the 
        #   values found by calculating the collision
        y.pop()
        y.append(0.0)
        vy.pop()
        vy.append(vygrav)
        vx.pop()
        vx.append(vxout)
        
        if(ymax > 0.5):
            move(x,y,vx,vy,counter, alpha, beta, skipCount)
    
        
def main():
    move(x,y,vx,vy,counter,alpha,beta,skipCount)
    plt.plot(x,y)
    print(x[-1])
    
if __name__ == '__main__':
    main()
