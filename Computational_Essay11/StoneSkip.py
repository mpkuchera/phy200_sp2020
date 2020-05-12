#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Daniel Valamssei
Time Spent: 2 hours
Created: 3-26-2020
Last Edited: 4-6-2020
"""

import math
import Projectile as pj
import pylab as plt


def skipToEnd(alpha, beta, x0, y0, v0):
    """
    Initialize and handle the recursive method from Projectile. Then, find 
    the number of times the stone skipped.
    
    param:
        alpha (int) - angle of stone relative to the horizon in radians
        beta (int) - ngle of initial velocity in radians
    
    return:
        skipCount (int) - number of skips that have occured
        x[len(x)-1] (int) - the distance which the stone traveled before 
                reaching the stopping condition in cm
       
    """

    vx0 = v0 * math.cos(beta)
    vy0 = v0 * math.sin(beta)


    x = [x0]
    y = [y0]
    vx = [vx0]
    vy = [vy0]
    counter = 0
 
    skipCount = 0
    
    pj.move(x,y,vx,vy,counter,alpha,beta,skipCount)
    
    #count up the skips (skips are indicated by 0.0 entries in y[])

    for i in range(len(y)):
        if (y[i] <= 0.0):
            skipCount+=1

    #return some stuff so I can analyze the optimization problem
    # number of skips and distance skipped
    return skipCount, x[len(x)-1]



#the only diference in this functionis that it makes a plot of the skips
def skipPlot(alpha, beta, x0, y0, v0):
    """
    Initialize and handle the recursive method from Projectile. Then, find 
    the number of times the stone skipped and plot the skips.
    
    param:
        alpha (int) - angle of stone relative to the horizon in radians
        beta (int) - ngle of initial velocity in radians
    
    return:
        skipCount (int) - number of skips that have occured
        x[len(x)-1] (int) - the distance which the stone traveled before 
                reaching the stopping condition in cm
       
    """

    vx0 = v0 * math.cos(beta)
    vy0 = v0 * math.sin(beta)


    x = [x0]
    y = [y0]
    vx = [vx0]
    vy = [vy0]
    counter = 0
 
    skipCount = 0
    
    pj.move(x,y,vx,vy,counter,alpha,beta,skipCount)
    
    for i in range(len(y)):
        if (y[i] == 0.0):
            skipCount+=1
        
    plt.plot(x,y)
    plt.show()
    

    return skipCount, x[len(x)-1]

def main():
    skipPlot(0.1, 0.0, 0.0, 50, 1000)
    
if __name__ == '__main__':
    main()