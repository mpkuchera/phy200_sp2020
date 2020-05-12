"""
file: sei.py
Author: Caitlin Welch

Brief: Brief: Uses the SEI Model (susceptible, exposed, infected) to model the 
        spread of COVID 19.

Sources:
    https://triplebyte.com/blog/modeling-infectious-diseases
    https://www.hopkinsmedicine.org/health/conditions-and-diseases/coronavirus/diagnosed-with-covid-19-what-to-expect
    https://www.discovermagazine.com/health/mild-cases-of-covid-19-may-have-helped-power-the-current-pandemic-heres-why
    https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article
"""

import numpy as np
import pylab as plt
import random

def f(r,t):    
    N = 1 #total population - we will do 1 to see the percent of the total
            #population
    
    #"High Contagiousness and Rapid Spread of Severe Acute Respiratory Syndrome
    #Coronavirus 2" claims that the basic reproductive number for coronavirus
    #is between 2.2 and 2.7. So, we will usea basic reproductive number of 2.45.
    R0 = 2.45 #basic reproductive number
    
    #Hopkins Medicine claims that mild cases take 2 weeks to recover, while
    #severe cases take 6 weeks to recover.
    #Discover Magazine claims that around 80% of cases are mild and around 20%
    #of cases are severe.
    Di = .8*(2*7) + .2*(6*7) #mean infectious period
    
    #NOTE: I could not find any data on this. So, I arbitrarily chose that
    #.5% of the US population travels inbound in a day and .5% of the US 
    #population travels outbound in a day
    Lii = .005 #average daily number of international inbound travellers
    Lio = .005 #average daily number of international outbound travellers
    
    #Since we are looking at the US as a whole, this value is 0 because domestic
    #travellers are included in the population. If we were to look at a specific
    #state or city, then we would have to account for domestic travellers.
    Ldi = 0 #average daily number of domestic inbound travellers
    Ldo = 0 #average daily number of domestic outbound travellers
    
    z = 0 #number of people infected by animal source - 0 for US
    
    #Hopkins Medicine claims that it takes 14 days for symptoms to show, so we
    #will set the latent period equal to some random number between 1 and 14.
    De = random.randrange(1,14) #mean latent period
    
    #arumgent "r" is a vector <susceptible, recovered, infected>
    susceptible = r[0]
    exposed = r[1]
    infected = r[2]
    
    #Set of differential equations
    fs = (-((susceptible/N)*(((R0/Di)*infected+z))) + Lii+Ldi - 
          (Lio/N+Ldo/N)*susceptible) #equals ds/dt
    fe = (((susceptible/N)*(R0/Di)*infected-z) - (exposed/De) - 
          (Lio/N+Ldo/N)*exposed) #equals de/dt
    fi = (exposed/De) - (infected/Di) - (Lio/N+Ldo/N)*infected #equals di/dt
    
    
    #Returns the differential equations in an array
    return np.array([fs,fe,fi], float)
    

#Runge-Kutta 4 ODE solver
def rk4(r,t,h):
    k1 = h*f(r,t)
    k2 = h*f(r+1/2*k1,t+1/2*h)
    k3 = h*f(r+1/2*k2,t+1/2*h)
    k4 = h*f(r+k3,t+h)
    r = (k1+2*k2+2*k3+k4)/6
    
    return r

def sei(i0,num_days):
    #starts at day 0 and goes to num_days
    a = 0
    b = num_days
    N = 10000
    h = (b-a)/N
    
    #the numbers for susceptible, recovered and infected are a fraction of the
    #total US population
    us_population = 3.282e8
    #assumes no one is recovered to start
    e0 = us_population - i0
    
    t_points = np.arange(a,b,h)
    s_points = []
    e_points = []
    i_points = []
    
    #initial conditions: s0 susceptible, i0 infected, 0 recovered
    r = np.array([0,e0/us_population,i0/us_population],float)
    
    for t in t_points:
        s_points.append(r[0])
        e_points.append(r[1])
        i_points.append(r[2])
        
        r += rk4(r,t,h)
        
    return s_points,e_points,i_points
        

def main():
    #Initializes the infected population and number of days to model for if
    #we run the code just within this file.
    i0 = 10
    num_days = 100
    
    #Susceptible, infected and recovered arrays
    s_points,e_points,i_points = sei(i0,num_days)
    
    #Since we evaluate at so many more points for a differential equation, we
    #need to scale the length of the population evaluations down to fit the 
    #number of days we are modelling.
    T = np.linspace(0,num_days,len(s_points))
    
    #Plots all three populations on the same graph
    plt.plot(T,s_points,label='Susceptible')
    plt.plot(T,e_points,label='Exposed')
    plt.plot(T,i_points,label='Infected')
    plt.legend()
    plt.xlabel('days')
    plt.ylabel('percent of population')
    plt.title('SEI Model')
    
    max_infected = max(i_points)
    print("Maximum percent of population to be infected is", max_infected)
    
if __name__ == "__main__":
    main()