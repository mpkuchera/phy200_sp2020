import numpy as np
import pylab as plt
import vpython as vp
from mpl_toolkits.mplot3d import Axes3D
"""
This program plots the trajectory of a cricket ball from the bowler to the batsman. 

We use the fourth order Runge Kutta method for solving the second order differential
equations. We can vary the components of velocity and spin and plot the bowling 
trajectories to observe the differences.

Author: Rida Shahid
Time taken: 10 hours
"""
def before_bounce(vx_0,vy_0,vz_0,wx,wy,wz):
    """
    This function plots the trajectory of the ball before it hits the ground.
    
    Returns final x, y, z, vx, vy, vz values and lists of x, y, and z values
    """
    # We define all the constants that we need to use
    g = 32.2 # gravitational constant in ft/ sec^2 
    radius = 0.116 # of the cricket ball in ft

    # We use the following two constants to calculate the value of constant_1
    #weight = 0.344 lb
    #ro = 0.075 lb/ft**2
    constant = 0.00461 # ro*area/(2*m)

    # C_d and C_l are constants for calculating the values of k_D and k_L
    c_d = 0.4
    c_l = 0.116
    k_d = c_d * constant # (c_d*ro*area)/(2*m)
    k_l = c_l * constant  # (c_l*ro*area)/(2*m)
    
    # the initial and final time
    t_0 = 0.0 #s
    t_f = 3.0

    # number of steps and value of h 
    N = 1000
    h = (t_f-t_0)/N

    e = 0.32 # coefficient of restitution
    c = 0.1 # constant for moisture level in the ground ranging from 0 to 1
    eps = 10E-2 # error constant
    
    # the values of the initial position of the ball and its 
    # x, y and z components
    x_0 = 1 #ft
    y_0 = 2 #ft
    z_0 = 7 #ft

    def f(r,t):
        """
        Helper function for using the fourth-order Runge Kutta (RK-4) method on the 
        second order differential equations which help plot the ball's trajectory in its
        x, y and z axes.
        """
        x = r[0]
        y = r[2]
        z = r[4]
        vx = r[1]
        vy = r[3]
        vz = r[5]
        velocity = np.sqrt(vx**2+vy**2+vz**2)
        #if np.abs(z)>eps:
        velocity = np.sqrt((vx+c*radius*wy)**2+(vy-c*radius*wx)**2+(-e*vz)**2)
            
        # equations for a cricket ball in motion
        return np.array([vx, (-k_d*velocity*vx+k_l*(wy*vz-wz*vy)),
                        vy, (-k_d*velocity*vy+k_l*(wz*vx-wx*vz)),
                        vz,(-k_d*velocity*vz+k_l*(wz*vy-wy*vx)-g)], float)
    
    t_before = np.arange(t_0, t_f, h) #array of time 
    x_before = [] 
    y_before = []
    z_before = []
    r_before = np.array([x_0, vx_0, y_0, vy_0, z_0, vz_0], float)
    
    # Applies RK-4 for each value of the position and velocity components
    for t in t_before:
        if np.abs(r_before[4])>=eps and r_before[0] <= (60+eps):  
            x_before.append(r_before[0])
            y_before.append(r_before[2])
            z_before.append(r_before[4])
            k1 = h * f(r_before, t)
            k2 = h * f(r_before + 0.5 * k1, t + 0.5 * h)
            k3 = h * f(r_before + 0.5 * k2, t + 0.5 * h)
            k4 = h * f(r_before + k3, t + h)
            r_before += (k1 + 2 * k2 + 2 * k3 + k4) / 6
    # sets the initial component values for after the bounce when z is 0
    x_f = r_before[0]
    y_f = r_before[2]
    z_f = r_before[4]
    vx_f = r_before[1]
    vy_f = r_before[3]
    vz_f = r_before[5]
    
    # Makes a 3-D plot of the x, y and z axes representing the ball before hitting
    # the ground
    plt.figure(1)
    plot1 = plt.axes(projection="3d")
    plot1.plot3D(x_before,y_before,z_before,'blue')
    plot1.set_xlabel('x')
    plot1.set_ylabel('y')
    plot1.set_zlabel('z')
    plot1.set_title('Before Bounce')
    
    return x_f,y_f,z_f,vx_f,vy_f,vz_f,x_before,y_before,z_before
    
def after_bounce(x_f,y_f,z_f,vx_f,vy_f,vz_f,wx,wy,wz):
    """
    This function plots the trajectory of the ball after it hits the ground.
    
    returns - lists of x, y and z values of the ball
    """
    # We define all the constants that we need to use
    g = 32.2 # gravitational constant in ft/ sec^2 
    radius = 0.116 # of the cricket ball in ft
    
    # We use the following two constants to calculate the value of constant_1
    #weight = 0.344 lb
    #ro = 0.075 lb/ft**2
    constant = 0.00461 # ro*area/(2*m)

    # C_d and C_l are constants for calculating the values of k_D and k_L
    c_d = 0.4
    c_l = 0.116
    k_d = c_d * constant # (c_d*ro*area)/(2*m)
    k_l = c_l * constant  # (c_l*ro*area)/(2*m)
    
    # the initial and final time
    t_0 = 0.0 #s
    t_f = 3.0

    # number of steps and value of h 
    N = 1000
    h = (t_f-t_0)/N

    e = 0.32 # coefficient of restitution
    c = 0.1 # constant for moisture level in the ground ranging from 0 to 1
    eps = 10E-2 # error constant
    
    def f_2(r,t):
        """
        Helper function for using the fourth-order Runge Kutta (RK-4) method on the 
        second order differential equations which help plot the ball's trajectory in its
        x, y and z axes after a bounce.
        """
        x = r[0]
        y = r[2]
        z = r[4]
        vx = r[1]
        vy = r[3]
        vz = r[5]
        # velocity equation for the ball after the bounce
        velocity = np.sqrt((vx+c*radius*wy)**2+(vy-c*radius*wx)**2+(-e*vz)**2)
        
        return np.array([vx, (-k_d*velocity*vx+k_l*(wy*vz-wz*vy)),
                        vy, (-k_d*velocity*vy+k_l*(wz*vx-wx*vz)),
                        vz,(-k_d*velocity*vz+k_l*(wz*vy-wy*vx)-g)], float)
    
    # Applies RK-4 for each value of the position and velocity components
    t_after = np.arange(t_0, t_f, h)
    x_after = []
    y_after = []
    z_after = []
    r_after = np.array([x_f, vx_f, y_f, vy_f, z_f, vz_f], float)
    for t in t_after:
        # continues the function until it reaches the end of the pitch
        if r_after[0] <= (60+eps):
            x_after.append(abs(r_after[0]))
            y_after.append(abs(r_after[2]))
            z_after.append(abs(r_after[4]))
            k1 = h * f_2(r_after, t)
            k2 = h * f_2(r_after + 0.5 * k1, t + 0.5 * h)
            k3 = h * f_2(r_after + 0.5 * k2, t + 0.5 * h)
            k4 = h * f_2(r_after + k3, t + h)
            r_after += (k1 + 2 * k2 + 2 * k3 + k4) / 6
            
    # Makes a 3-D plot of the x, y and z axes representing the ball after hitting
    # the ground
    plt.figure(2)
    plot2 = plt.axes(projection="3d")
    plot2.plot3D(x_after,y_after,z_after,'blue')
    plot2.set_xlabel('x')
    plot2.set_ylabel('y')
    plot2.set_zlabel('z')
    plot2.set_title('After Bounce')
    
    return x_after,y_after,z_after

def plots(x_bef,y_bef,z_bef):
    """
    Creates a 2-D and 3-D plot of the ball's total trajectory.
    """
    # Makes a 3-D plot of the x, y and z axes representing the ball's total trajectory
    plt.figure(3)
    plot3 = plt.axes(projection="3d")
    plot3.plot3D(x_bef,y_bef,z_bef,'blue')
    plot3.set_xlabel('x (ft)')
    plot3.set_ylabel('y (ft)')
    plot3.set_zlabel('z (ft)')
    plot3.set_title('Total Trajectory')
    
    # Makes a 2-D plot of the x, and z axes representing the ball's total 2-D trajectory
    plt.figure(4)
    plt.plot(x_bef,z_bef)
    plt.xlabel('x (ft)')
    plt.ylabel('z (ft)')
    plt.title('z (ft) vs x (ft)')
    plt.show()

def animation(x_bef,y_bef,z_bef):
    """
    Creates a simulation of the cricket ball's trajectory across an animated pitch. 
    """
    scene1 = vp.canvas(width = 800,height = 500,background=vp.color.cyan) # sets the scene
    
    #sets the initial positions of the ball, pitch, and wickets and draws them
    ball = vp.sphere(pos=vp.vector(x_bef[0],z_bef[0],y_bef[0]),radius=0.02,color=vp.color.red,make_trail=True)
    floor = vp.box(pos=vp.vector(x_bef[len(x_bef)//2],-5,y_bef[0]),size = vp.vector(65,10,0.1),color=vp.color.green)
    wicket = vp.box(pos=vp.vector(x_bef[0],2,y_bef[0]),size = vp.vector(1,4,0.1),color=vp.color.white)
    wicket = vp.box(pos=vp.vector(x_bef[len(x_bef)-1],2,y_bef[0]),size = vp.vector(1,4,0.1),color=vp.color.white)
    
    # changes the position of the ball according to our data 
    for i in range(len(x_bef)):
        vp.rate(35)
        ball.pos.x = x_bef[i]
        ball.pos.y = z_bef[i]
        ball.pos.z = y_bef[i]

