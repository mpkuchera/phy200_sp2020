"""
file: basic_methods.py
Author: Caitlin Welch

Brief: This file contains the three basic methods used to model infection:
        a linear model, exponential model and logistic model. While these 
        methods are known to be less accurate than the models involving 
        differential equations, I am still graphing them to compare to the 
        reported data.

Sources:
    https://www.wired.com/story/the-promising-math-behind-flattening-the-curve/
    https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article
"""

import pylab as plt
import numpy as np

us_population = 3.282e8 #found by googling the US population

#Linear Model for spread of infectious disease
def linear(i0,num_days):
    di = 100 #change in infected per day
    
    infected = []
    
    for i in range(num_days+1):
        #The number of humans infected on a given day for a linear model is
        #equal to the number of humans infected the day before plus some 
        #constant.
        today_infected = i0 + di
        infected.append(today_infected)
        #Set the variable for the "day before" equal to the current day's 
        #number of infected before moving on to the next day.
        i0 = today_infected
        
    #Converts the infected list to an array, which will be easier to work with.
    infected = np.array(infected)
    #Looks at the infected population as a percent of the total US population.
    infected = infected/us_population
        
    return infected


#Exponential Model for spread of infectious disease
def exponential(i0,num_days):
    #"High Contagiousness and Rapid Spread of Severe Acute Respiratory Syndrome
    #Coronavirus 2" claims that the basic reproductive number for coronavirus
    #is between 2.2 and 2.7. So, we will usea basic reproductive number of 2.45.
    a = 2.45 #rate of infection
    
    infected = []
    
    for i in range(num_days+1):
        #The number of humans infected on a given day for an exponential model
        #is equal to the number of humans infected the day before times some
        #constant.
        today_infected = i0 + a*i0
        infected.append(today_infected)
        #Set the variable for the "day before" equal to the current day's
        #number of infected before moving on to the next day.
        i0 = today_infected
    
    #Converts the infected list to an array, which will be easier to work with.
    infected = np.array(infected)
    #Looks at the infected population as a percent of the total US population.
    infected = infected/us_population
    
    return infected


#Logistic Model for spread of infectious disease
def logistic(i0,num_days):
    a = 1 #rate of infection
    max_infected = 1e8 #maximum number of humans that can be infected
    
    infected = []
    
    for i in range(num_days+1):
        #The number of humans infected on a given day for a logistic model is
        #equal to the logistic function. 
        today_infected = i0 + a*(1-i0/max_infected)*i0
        infected.append(today_infected)
        i0 = today_infected
        
    #Converts the infected list to an array, which will be easier to work with.
    infected = np.array(infected)
    #Looks at the infected population as a percent of the total US population.
    infected = infected/us_population
    
    return infected


def main():
    #Initializes the infected population and number of days to model for if
    #we run the code just within this file.
    i0 = 10
    num_days = 40
    
    #Infected array for each modelling type
    infected_linear = linear(i0,num_days)
    infected_exponential = exponential(i0,num_days)
    infected_logistic = logistic(i0,num_days)
    
    #Plots each modelling type on different graphs
    plt.figure()
    plt.plot(range(num_days+1),infected_linear)
    plt.xlabel('days')
    plt.ylabel('percent infected')
    plt.title('Linear Model')
    plt.figure()
    plt.plot(range(num_days+1),infected_exponential)
    plt.xlabel('days')
    plt.ylabel('percent infected')
    plt.title('Exponential Model')
    plt.figure()
    plt.plot(range(num_days+1),infected_logistic)
    plt.xlabel('days')
    plt.ylabel('percent infected')
    plt.title('Logistic Model')
    
    
if __name__ == "__main__":
    main()