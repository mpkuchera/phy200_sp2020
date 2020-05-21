#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 20:50:27 2020

@author: jaime
"""

import numpy as np
import matplotlib.pyplot as mpl

#constants
R = 0.00365 #baseball radius (m)
g = 9.8 # gravitational acceleration (m/s^2)
m = 0.145E-3 #in kilograms


distance = float(input("enter the distance from the release point of the pitch to the plate in meters between 16.5 and 17:  ")) # m (distance from pitcher to home plate) 16.5, 18.66 is from mound to plate
ro = float(input("enter the air density of the pitch between 0.8 and 1.3 (average is 1.23):  ")) # density of air (kg/m^3) 0.8-1.3, average 1.23
C = float(input("enter the drag constant of the pitch between 0.4 and 0.5:  ")) # drag constant which can be CHANGED!!! 0.4-0.5 ,  try: 0.47
CM = float(input("enter the magnus constant of the pitch between 0.2 and 0.3:  ")) #magnus constant!  0.2  -  0.3
height = float(input("enter the height of the release point in meters between 2 and 2.5:  ")) # m (height of ball release point of pitcher) average baseball player height is 6ft 2in and release point is above head


ARC =  np.pi*(R**2)*ro*C   #ro * A * C   ###air res constant
ARCM = np.pi*(R**2)*ro*CM  ###mag force constant

def f(r):
    """
    This function returns the first-order and second-order derivatives.
    
    Parameters:
        r - array of x, y, vx, and vy
    
    Returns:
        array of time derivatives vx, vy, ax, and ay
    """
    vx = r[2]  #assigning vx to equal to 3rd item in r array which the value changes each time it goes through while loop
    vy = r[3]  #assigning vy to equal to 4rd item in r array which the value changes each time it goes through while loop
    ax = -(ARC/(2*m))*vx*np.sqrt(vx**2 + vy**2) + (ARCM/(2*m))*np.sqrt(vx**2 + vy**2)*vx*np.sin(np.pi/2)    #F/m = a   #air res equation
    ay = - g - (ARC/(2*m))*vy*np.sqrt(vx**2 + vy**2) + (ARCM/(2*m))*np.sqrt(vx**2 + vy**2)*vy*np.sin(np.pi/2)  #gravitational force - air res
    return np.array([vx,vy,ax,ay])
    
def RK4(v,theta):
    """
    This function solves for the x and y positions for a trajectory using
    fourth-order Runge Kutta. 
    
    Parameters:
        v - initial velocity
        theta - initial angle
    
    Returns:
        xs - list of x position values
        ys - list of y position values
    """   

    dt = 0.001  #hard code h to be delta t per iteration, width of each iteration
    
    x = 0  #initial x position
    y = height  #initial y position
    theta *= np.pi/180  #converting degrees in to radians
    vx = v*np.cos(theta)   #x component of initial velocity
    vy = v*np.sin(theta)  #y component of initial velocity
    #omega = 
    xs = []  #empty list of x position that updates per iteration to keep track of x position
    ys = []  #empty list of y position that updates per iteration to keep track of y position 
    r = np.array([x,y,vx,vy],float) #creating r array with initial position and velocity components which updates within loop
    while r[0] <= distance: #while x position is less than or equal to the distance from the mound to home plate run the loop
        xs.append(r[0]) 
        ys.append(r[1])
        k1 = dt*f(r)   #derivative is a marginal change so updating per each small change
        k2 = dt*f(r+(0.5*k1))
        k3 = dt*f(r+(0.5*k2))
        k4 = dt*f(r+k3)
        r += (k1+2.*k2+2.*k3+k4)/6  #updating pos and vel given time derivatives based on k's
    return xs, ys  #adds new value to list

#def vplot(v,theta):
#
#    dt = 0.001 #linspace???
#    x = 0  #initial x position
#    y = height  #initial y position
#    theta *= np.pi/180  #converting degrees in to radians
#    vx = v*np.cos(theta)   #x component of initial velocity
#    vy = v*np.sin(theta)  #y component of initial velocity
#    vxs = []  #empty list of x position that updates per iteration to keep track of x position
#    vys = []  #empty list of y position that updates per iteration to keep track of y position 
#    r = np.array([x,y,vx,vy],float) #creating r array with initial position and velocity components which updates within loop
#    while r[0] <= distance: #while x position is less than or equal to the distance from the mound to home plate run the loop
#        vxs.append(r[2]) 
#        vys.append(r[3])
#        k1 = dt*f(r)   #derivative is a marginal change so updating per each small change
#        k2 = dt*f(r+(0.5*k1))
#        k3 = dt*f(r+(0.5*k2))
#        k4 = dt*f(r+k3)
#        r += (k1+2.*k2+2.*k3+k4)/6  #updating pos and vel given time derivatives based on k's
#    return vxs, vys  #adds new value to list
#    
#def aplot(v,theta):
#    
#    dt = 0.001
#    x = 0  #initial x position
#    y = height  #initial y position
#    theta *= np.pi/180  #converting degrees in to radians
#    vx = v*np.cos(theta)   #x component of initial velocity
#    vy = v*np.sin(theta)  #y component of initial velocity
#    axs = []  #empty list of x position that updates per iteration to keep track of x position
#    ays = []  #empty list of y position that updates per iteration to keep track of y position 
#    r = np.array([x,y,vx,vy],float) #creating r array with initial position and velocity components which updates within loop
#    while r[0] <= distance: #while x position is less than or equal to the distance from the mound to home plate run the loop
#        axs.append(f(r[2]))
#        ays.append(f(r[3]))
#        k1 = dt*f(r)   #derivative is a marginal change so updating per each small change
#        k2 = dt*f(r+(0.5*k1))
#        k3 = dt*f(r+(0.5*k2))
#        k4 = dt*f(r+k3)
#        r += (k1+2.*k2+2.*k3+k4)/6  #updating pos and vel given time derivatives based on k's
#    return axs, ays  #adds new value to list

def plot_trajectory(v,theta):
    """
    This function plots the trajectory of the baseball.
    
    Parameters:
        v - initial velocity
        theta - initial angle
    """
    xs, ys = RK4(v,theta)  #setting xs and ys to the values returned to the RK4 function
    mpl.plot(xs,ys)  #plotting the x and y position values
    mpl.xlabel('x in meters')
    mpl.ylabel('y in meters')
    mpl.title('Trajectory of baseball')
    mpl.ylim(0,4) #strike zone is between kneecap and mid torso (average: 0.5m - 1.5m)
    mpl.xlim(0,17)
    mpl.show()
    
#    vxs, vys = vplot(v,theta)
#    mpl.plot(vxs,vys)
#    mpl.xlabel('vx')
#    mpl.ylabel('vy')
#    mpl.title('Velocity of baseball')
#    mpl.show()
    
    #axs, ays = aplot(v,theta)
    #mpl.plot(axs,ays)
    

def main():
    velocity_not = float(input("enter the velocity of the pitch between 20 m/s and 45 m/s:  ")) 
    angle = float(input("enter the angle of the pitch between 1 degrees and 15 degrees:  ")) 
    
    plot_trajectory(velocity_not,angle)  #velocity and angle in degrees (20-45m/s for velocity and 1-15 degrees depending on velocity , to be in strikezone)

if __name__ == "__main__":
    main()