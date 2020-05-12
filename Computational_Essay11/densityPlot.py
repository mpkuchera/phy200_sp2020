#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: Daniel Valmassei
Time Spent: 1 hour
Created: 3-27-2020
Last Edited: 4-6-2020
"""
import numpy as np
import StoneSkip as sk2
import pylab as plt



def plotDensity():
    
    maxA = 0.0
    maxB = 0.0
    maxSkips = 0.0
    maxDist = 0.0
    
    #build lists of skips and distance for the range of alpha and beta
    div = 100
    a = np.linspace(0.0,0.3,div)
    b = np.linspace(-0.3,0.2,div)
    skips = np.empty((div,div))
    dist = np.empty((div,div))
    
    for i in range(div):
        for j in range(div):
            skips[i][j], dist[i][j] = (sk2.skipToEnd(a[i], b[j], 0.0, 50.0, 1000))
            
            #optimize skips and distance simultaneously
            if(skips[i][j] >= maxSkips and dist[i][j] >= maxDist):
                maxSkips = skips[i][j]
                maxDist = dist[i][j]
                maxA = a[i]
                maxB = b[j]
            
    
    #make density plots for both Distance and Skips
    plt.figure(figsize = [6.4,4.8])        
    plt.imshow(dist, vmax = np.amax(dist),origin = 'lower', 
               extent = [-0.3,0.2,0.0,0.3])
    plt.colorbar()
    plt.title('Distance in cm')
    plt.xlabel("beta (rad)")
    plt.ylabel("alpha (rad)")
    plt.show()
    
    plt.figure(figsize = [6.4,4.8])        
    plt.imshow(skips, vmax = np.amax(skips),origin = 'lower', 
               extent = [-0.3,0.2,0.0,0.3])
    plt.colorbar()
    plt.title('Skips')
    plt.xlabel("beta (rad)")
    plt.ylabel("alpha (rad)")
    plt.show()
    
    
    #print the optimized case
    print("For the optimized case, alpha = ", maxA,", beta = ", maxB, ":")
    skip, dist = sk2.skipPlot(maxA,maxB, 0.0, 50.0, 1000)
    print("The stone skips", skip, "times over", dist, "cm.")
    
def main():
    #print some example graphs
    print(sk2.skipPlot(0.45, 0.0, 0.0, 50.0, 1000))
    print(sk2.skipPlot(0.35, 0.0, 0.0, 50.0, 1000))
    print(sk2.skipPlot(0.25, 0.0, 0.0, 50.0, 1000))
    print(sk2.skipPlot(0.10, 0.0, 0.0, 50.0, 1000))
    print(sk2.skipPlot(0.1,-0.2, 0.0, 50.0, 1000))
    
    plotDensity()

if __name__ == '__main__':
    main()