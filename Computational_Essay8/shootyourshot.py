#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code for shooting your own 3-pointer!

author: L.L. Arkell
date: May 2020

"""
#imports go here:
from math import cos, sin, pi
from numpy import array
import pylab as plt
M="Mens"
W="Womens"

g=9.81 #m/s/s, gravity
#calculating the kd constant for the basketball
balldiameter= 0.79 
area= 0.49 
mass=0.041 
p= 2.38e-3 
cd=0.5
kd= (cd*p*area)/(2*mass) #inut is f^-1
kd= kd/0.3048 #change unit to 1/m

#equations with z-axis pointing up
#x-axis pointing toward the basket
#y-component will always be 0

menh=1.957 #height of average mens player in m
womenh= 1.728 #height of average womens player in m

mens3 = 6.75 #3-point distances for mens in m
m3max=6.85668 #takes into account the width of a hoop, radius=0.10668m
m3min=6.64332 #takes into account the width of a hoop, radius=0.10668m
womens3 = 6.3246 #3-point distances for womens in m
w3max=6.43128 #takes into account the width of a hoop, radius=0.10668m
w3min=6.21792 #takes into account the width of a hoop, radius=0.10668m
height = 3.048 #height of basketball hoop in m
    # needs to be at height at distance    

#The fourth order Runge-Kutta method:
def f(r):
    vx=r[2] #defining x-velocity from r
    vz=r[3] #defining z-velocity from r
    v=(vx**2+vz**2)**0.5 #need v for both ax and az
    ax= -kd*v*vx #acceleration in x direction
    az= -kd*v*vx-g #acceleration in zdirection
    
    return array([vx,vz,ax,az],float) #return array with vx, vz, ax, and az

#running this code will allow you to print any trajectory with the velocity and angle you enter!
def shootyourshot(): #theta must be in radians
    x=0.0 #starting x, set location to 0
    z=menh
    counter=0
#calculating starting velocity
    v=input("Velocity:")
    angle=input("Starting angle in degrees:")
    v=float(v)
    angle=float(angle)
    theta=angle*pi/180
    vx= v*cos(theta)   
    vz= v*sin(theta)
        
    h=0.001 #step size, set becasue we dont have an a,b,N
    
    xpoints=[] #create empty array
    zpoints=[] #create empty array
    
    r=array([x,z,vx,vz],float)#starting array with initial location and velocity
    
    while r[1] >= 0:
        xpoints.append(r[0])
        zpoints.append(r[1])
        k1=h*f(r)
        k2=h*f(r+0.5*k1)
        k3=h*f(r+0.5*k2)
        k4=h*f(r+k3)
        r += (k1+2*k2+2*k3+k4)/6
    for i in range(len(xpoints)):
            if xpoints[i] < m3max and xpoints[i]> m3min and zpoints[i] > 3.038 and zpoints[i] < 3.058:
                plt.plot(xpoints,zpoints)
                plt.axis('equal')
                plt.xlabel("X")
                plt.ylabel("Z")
                plt.title("You Scored A 3-Pointer!!")
            else:
                counter=counter+1
    if counter == len(xpoints):
        print("I'm sorry, your shot didn't go in.")