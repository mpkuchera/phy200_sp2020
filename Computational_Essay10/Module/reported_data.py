"""
file: reported_data.py
Author: Caitlin Welch

Sources:
    https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/previouscases.html
"""

import pylab as plt

#I couldn't find any way to scrape this data with my capabiltiies, so I
#had to manually enter it.
#Data covers January 22, 2020 to April 29, 2020
reported_total = [1,1,2,2,5,5,5,5,5,7,8,8,11,11,11,11,11,11,11,11,12,12,13,13,
                  13,13,13,13,13,13,15,15,15,15,15,15,16,16,24,30,53,78,98,164,
                  211,275,422,647,937,1215,1629,1896,2234,3471,4226,7023,10442,
                  15219,18747,24583,33404,44338,54453,68440,85356,103321,
                  122653,140904,163539,186101,213144,239279,258098,267436,
                  330891,374329,395926,427460,459165,492416,525704,554849,
                  579005,605390,632548,661712,690714,720630,746625,776093,
                  802583,828441,865586,895766,928619,962491,981246,1005147]

def reported():
    reported_by_day = []
    
    #reported_total is a list of the total infected humans on each given day.
    #So, we must solve for the difference between each subsequent day to see
    #how many were infected on a given day.
    for i in range(len(reported_total)-1):
        reported_by_day.append(reported_total[i+1]-reported_total[i])
        
    return reported_by_day


def main():
    reported_by_day = reported()
    plt.plot(range(len(reported_by_day)),reported_by_day)
    plt.xlabel('days')
    plt.ylabel('number infected')
    plt.title('CDC Reported')
    
    
if __name__ == "__main__":
    main()