"""
file: seir.py
Author: Caitlin Welch

Brief: Uses the SEIR Model (susceptible, exposed, infected, recovered) to 
        model the spread of COVID 19.

Sources:
    https://www.discovermagazine.com/health/mild-cases-of-covid-19-may-have-helped-power-the-current-pandemic-heres-why
    https://www.medrxiv.org/content/10.1101/2020.04.02.20050674v2.full.pdf+html
    https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article
"""
import numpy as np
import pylab as plt
import random

def f(r,t):
    #"High Contagiousness and Rapid Spread of Severe Acute Respiratory Syndrome
    #Coronavirus 2" claims that the basic reproductive number for coronavirus
    #is between 2.2 and 2.7. So, we will usea basic reproductive number of 2.45.
    #Note: B = b0*k where b0 is the probability of infection per encounter with
    #an infected individual and k is the number of people encountered per day
    B = 2.45 #infection rate
    
    #Hopkins Medicine claims that it takes 14 days for symptoms to show, so we
    #will set the latent period equal to some random number between 1 and 14.
    Te = random.randrange(1,14) #latent period
    w = 1/Te
    
    #Hopkins Medicine claims that mild cases take 2 weeks to recover, while
    #severe cases take 6 weeks to recover.
    #Discover Magazine claims that around 80% of cases are mild and around 20%
    #of cases are severe.
    Ti = .8*(2*7) + .2*(6*7) #average recovery time of infectives
    gamma = 1/Ti
    
    N = 1 #population size - we will do 1 to see the percent of the total 
            #population
    
    #arumgent "r" is a vector <susceptible, exposed, recovered, infected>
    susceptible = r[0]
    exposed = r[1]
    infected = r[2]
    recovered = r[3]
    
    #Set of differential equations
    fs = -B*(susceptible/N)*infected #equals ds/dt
    fe = B*(susceptible/N)*infected - w*exposed #equals de/dt
    fi = w*exposed - gamma*infected #equals di/dt
    fr = gamma*infected #equals dr/dt
    
    #Returns the differential equations in an array
    return np.array([fs,fe,fi,fr], float)
    

#Runge-Kutta 4 ODE solver
def rk4(r,t,h):
    k1 = h*f(r,t)
    k2 = h*f(r+1/2*k1,t+1/2*h)
    k3 = h*f(r+1/2*k2,t+1/2*h)
    k4 = h*f(r+k3,t+h)
    r = (k1+2*k2+2*k3+k4)/6
    
    return r

def seir(i0,num_days):
    #starts at day 0 and goes to num_days
    a = 0
    b = num_days
    N = 10000
    h = (b-a)/N
    
    #the numbers for susceptible, exposed, infected and recovered are a 
    #fraction of the total US population
    us_population = 3.282e8 #found by googling the US population
    #assumes no one is recovered to start
    e0 = us_population - i0
    
    t_points = np.arange(a,b,h)
    s_points = []
    e_points = []
    i_points = []
    r_points = []
    
    #initial conditions: s0 susceptible, i0 infected, 0 recovered
    r = np.array([0,e0/us_population,i0/us_population,0],float)
    
    for t in t_points:
        s_points.append(r[0])
        e_points.append(r[1])
        i_points.append(r[2])
        r_points.append(r[3])
        
        r += rk4(r,t,h)
        
    #Converts the four population lists to arrays, which will be easier to
    #work with.
    s_points = np.array(s_points)
    e_points = np.array(e_points)
    i_points = np.array(i_points)
    r_points = np.array(r_points)
        
    return s_points,e_points,i_points,r_points
        

def main():
    #Initializes the infected population and number of days to model for if
    #we run the code just within this file.
    i0 = 10
    num_days = 100
    
    #Susceptible, infected and recovered arrays
    s_points,e_points,i_points,r_points = seir(i0,num_days)
    
    #Since we evaluate at so many more points for a differential equation, we
    #need to scale the length of the population evaluations down to fit the 
    #number of days we are modelling.
    T = np.linspace(0,num_days,len(s_points))
    
    #Plots all three populations on the same graph
    plt.plot(T,s_points,label='Susceptible')
    plt.plot(T,e_points,label='Exposed')
    plt.plot(T,i_points,label='Infected')
    plt.plot(T,r_points,label='Recovered')
    plt.legend()
    plt.xlabel('days')
    plt.ylabel('percent of population')
    plt.title('SEIR Model')
        
    #Finds the peak of the infected curve
    max_infected = max(i_points)
    print("Maximum percent of population to be infected is", max_infected)
    
if __name__ == "__main__":
    main()