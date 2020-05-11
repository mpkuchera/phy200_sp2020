"""
file: FinalProject.py

author: ethancramer
date: 13 May 2020
brief: Final project final code submission

"""

from numpy import cos, array, sin, pi
from matplotlib.pyplot import plot, show, title, xlabel, ylabel, ylim, figure
from mpl_toolkits.mplot3d import Axes3D
from random import randrange

def chooseHole():
    """
    chooseHole returns the distance to the cup (DTC),
    which allows the point system to find how far the shot
    was from the hole, which determines how many points are given.
    chooseHole will also return a "random" wind value for each hole.
    """
    
    holes = ["Hole 1: 250 meters to the cup", "Hole 2: 180 meters to the cup", "Hole 3: 400 meters to the cup", "Hole 4: 100 meters to the cup"] 
    print("Here are the hole options: ", holes)
    hole = input("Which hole would you like to play (spell it out, e.g., \"one\" or \"two\"): ")
    DTC = 0
    wind  = 0
    if hole == "one":
        DTC = 250
        wind = randrange(0, 21) - 10
        return DTC, wind
    elif hole == "two":
        DTC = 180
        wind = randrange(0, 31) - 20
        return DTC, wind
    elif hole == "three":
        DTC = 400
        wind = randrange(0, 6) - 5
        return DTC, wind
    elif hole == "four":
        DTC = 100
        wind = randrange(21, 46)
        return DTC, wind
    elif hole == "example":
        DTC = 200
        wind = 0
        return DTC, wind
        
    
def chooseClub():
    """
    chooseClub returns the launch angle of the ball
    """
    
    bag = ["9I", "8I", "7I", "6I", "5I", "4I"]
    """
    Launch angle of the ball is:
        attack angle + loft angle
    """
    loft = array([0.3560472, 0.3159046, 0.2844887, 0.2460914, 0.2111848, 0.191986]) #all in radians
    attack = array([4.7 * (pi/180), 4.5 * (pi/180), 4.3 * (pi/180), 4.1 * (pi/180), 3.7 * (pi/180), 3.4 * (pi/180)])
    angles = loft + attack
    theta = 0.0
    
    print("Your bag: ", bag)
    club = input("Which club would you like: ")
    if club == bag[0]:
        theta = angles[0]
        return theta
    if club == bag[1]:
        theta = angles[1]
        return theta
    if club == bag[2]:
        theta = angles[2]
        return theta
    if club == bag[3]:
        theta = angles[3]
        return theta
    if club == bag[4]:
        theta = angles[4]
        return theta
    if club == bag[5]:
        theta = angles[5]
        return theta

def f(r):
    kD = 0.00231
    kL = 0.00041
    g = 9.81
    dx = r[3]
    dy = r[4]
    dz = r[5]
    vrel = (dx**2 + dy**2 + dz**2)**0.5
    dtheta = r[8]
    dphi = r[9]
    domegatheta = 0
    domegaphi = 0
    dvx = -kD*vrel*dx + kL*(dtheta*dz - dphi*dy)
    dvy = -kD*vrel*dy + kL*(dphi*dx)
    dvz = -kD*vrel*dz + kL*(-dtheta*dx) - g
    
    
    return array([dx, dy, dz, dvx, dvy, dvz, dtheta, dphi, domegatheta, domegaphi])
    
    
def RK4(x, y, z, vx, vy, vz, theta, phi, omegatheta, omegaphi):
    
    
    r = array([x, y, z, vx, vy, vz, theta, phi, omegatheta, omegaphi], float)
    h = 0.001 #seconds
    
    x = []
    y = []
    z = []
    
    while r[2] >= 0:
        k1 = h * f(r)
        k2 = h * f(r + 0.5 * k1)
        k3 = h * f(r + 0.5 * k2)
        k4 = h * f(r + k3)
        r += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x.append(r[0])
        y.append(r[1])
        z.append(r[2])
        
    return x, y, z
    
def teeOff():
    
    DTC, wind = chooseHole()
    if DTC == 200:
        theta =  4.3 * (pi/180) + 0.2844887 #which is a 7 iron
        vin = 144.9401 #mph
        omegain = 0
    else:
        theta = chooseClub()
        vin = float(input("What would you like your initial ball speed to be [mph]: "))
        print("The wind speed for this hole is ", wind, "mph (- means to the left, + means to the right)")
        omegain = float(input("Enter your desired side spin (+ for right and - for left)[rpm]: "))
    v = vin / 2.23694 #mph to m/s
    Wind = wind / 2.23694 #mph to m/s
    omegaphi = omegain * (pi/30) #rpm to rad/s
    #atmDen = 0.075 #lb/ft^3
    #ballMass = 1.62 #oz
    #ballDiam = 1.692 #inch
    vx = v*cos(theta)
    vy = Wind
    vz = v*sin(theta)
    x, y, z = RK4(0, 0, 0, vx, vy, vz, theta, 0, 0, omegaphi)
    fig = figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([DTC], [0], [0])
    ax.scatter(x, y, z)
    title("Trajectory of your golf ball (3D)")
    ax.set_xlabel('vertical Distance (m)')
    ax.set_ylabel('Horizontal Distance (m)')
    ax.set_zlabel('Height (m)')
    ylim(-40.0, 40.0)
    ax.set_facecolor('xkcd:green')
    show()
    #plot(x, z)
    #title("Trajectory of your golf ball (2D)")
    #xlabel("Distance (m)")
    #ylabel("Height (m)")
    #show()
    totDis = x[-1]
    horiDis = y[-1]
    DFC = ((totDis)**2 + (horiDis)**2)**0.5 #the distance from the cup after ball lands.
    print("your ball landed ", abs(DFC-DTC), "meters from the cup")
    """
    point counter:
    """
    print("The distance to the cup was: ", DTC)
    print("Your shot traveled", totDis, "meters.")
    points = 0
    if abs(DTC - DFC) <= 5:
        points += 10
        print("Amazing! +", points, "points!")
    
    elif abs(DTC - DFC) <= 10:
        points += 5
        print("Nice Job! +", points, "points!")
        
    elif abs(DTC - DFC) <= 20:
        points += 3
        print("Not Bad! +", points, "points!")
        
    elif abs(DTC - DFC) <= 30:
        points += 1
        print("Okay! +", points, "points!")
    else:
        print("Better Luck Next Time!")
        
    print("you have", points, "points")

def main():
    
    teeOff()
    
if __name__ == "__main__":
    main()
    
    