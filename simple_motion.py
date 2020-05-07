"""
Created on Mon May  6 10:10:23 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, pi, mag, rate

#scene.autoscale = False

axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0),shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0),shaftwidth=0.01)            

#body = sphere(radius = 0.05)
body = sphere(radius = 0.05, make_trail=True, trail_type="points",
              interval=10, retain=50)

body.color = color.orange 

# Initial values
acceleration = vector(0,-9.81,0)  
velocity = vector(2,2,0) 
body.pos = vector(0,0,0)
time = 0

# Set time interval
dt = 0.001 

# Set refresh rate
while body.pos.y>=0:   
    
    rate(100)
    time = time + dt
    velocity = velocity + acceleration *dt
    body.pos = body.pos + velocity *dt

    scene.caption= ("t:  "+ str(round(time,2))+"s"+ "\n"
                    "x: "+ str(round(body.pos.x,3)),"m","\n"
                    "y: "+ str(round(body.pos.y,3)),"m")