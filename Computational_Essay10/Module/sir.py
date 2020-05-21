"""
file: sir.py
Author: Caitlin Welch

Brief: Uses the SIR Model (susceptible, infected, recovered) to model the 
        spread of COVID 19.

Sources:
    https://www.maa.org/press/periodicals/loci/joma/the-sir-model-for-spread-of-disease-the-differential-equation-model
    https://www.hopkinsmedicine.org/health/conditions-and-diseases/coronavirus/diagnosed-with-covid-19-what-to-expect
    https://www.discovermagazine.com/health/mild-cases-of-covid-19-may-have-helped-power-the-current-pandemic-heres-why
    https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article
"""

import numpy as np
import pylab as plt

def f(r,t):
    #"High Contagiousness and Rapid Spread of Severe Acute Respiratory Syndrome
    #Coronavirus 2" claims that the basic reproductive number for coronavirus
    #is between 2.2 and 2.7. So, we will usea basic reproductive number of 2.45.
    b = 2.45 #number of contacts per day that are sufficient to spread the virus
    
    #Hopkins Medicine claims that mild cases take 2 weeks to recover, while
    #severe cases take 6 weeks to recover.
    #Discover Magazine claims that around 80% of cases are mild and around 20%
    #of cases are severe.
    k = .8*1/(2*7) + .2*1/(6*7) #fraction k of the infected group recovers per day
    
    #arumgent "r" is a vector <susceptible, recovered, infected>
    susceptible = r[0]
    infected = r[1]
    recovered = r[2]
    
    #Set of differential equations
    fs = -b * susceptible * infected # equals ds/dt
    fr = k * infected # equals dr/dt
    fi = b * susceptible * infected - k * infected # equals di/dt
    
    #Returns the differential equations in an array
    return np.array([fs,fi,fr], float)
    

#Runge-Kutta 4 ODE solver
def rk4(r,t,h):
    k1 = h*f(r,t)
    k2 = h*f(r+1/2*k1,t+1/2*h)
    k3 = h*f(r+1/2*k2,t+1/2*h)
    k4 = h*f(r+k3,t+h)
    r = (k1+2*k2+2*k3+k4)/6
    
    return r

def sir(i0,num_days):
    #starts at day 0 and goes to num_days
    a = 0
    b = num_days
    N = 10000
    h = (b-a)/N
    
    #the numbers for susceptible, recovered and infected are a fraction of the
    #total US population
    us_population = 3.282e8 #found by google the US population
    #assumes no one is recovered to start
    s0 = us_population - i0
    
    t_points = np.arange(a,b,h)
    s_points = []
    i_points = []
    r_points = []
    
    #initial conditions: s0 susceptible, i0 infected, 0 recovered
    r = np.array([s0/us_population,i0/us_population,0],float)
    
    for t in t_points:
        s_points.append(r[0])
        i_points.append(r[1])
        r_points.append(r[2])
        
        r += rk4(r,t,h)
        
    #Converts the three population lists to arrays, which will be easier to
    #work with.
    s_points = np.array(s_points)
    i_points = np.array(i_points)
    r_points = np.array(r_points)
        
    return s_points,i_points,r_points
        

def main():
    #Initializes the infected population and number of days to model for if
    #we run the code just within this file.
    i0 = 10
    num_days = 100
    
    #Susceptible, infected and recovered arrays
    s_points,i_points,r_points = sir(i0,num_days)
    
    #Since we evaluate at so many more points for a differential equation, we
    #need to scale the length of the population evaluations down to fit the 
    #number of days we are modelling.
    T = np.linspace(0,num_days,len(s_points))
        
    #Plots all three populations on the same graph
    plt.plot(T,s_points,label='Susceptible')
    plt.plot(T,i_points,label='Infected')
    plt.plot(T,r_points,label='Recovered')
    plt.legend()
    plt.xlabel('days')
    plt.ylabel('percent of population')
    plt.title('SIR Model')
    
    #Finds the peak of the infected curve
    max_infected = max(i_points)
    print("Maximum percent of population to be infected is", max_infected)
    
if __name__ == "__main__":
    main()