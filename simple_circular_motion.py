"""
Created on Mon May  6 10:10:23 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, pi, mag, rate

axis_x = arrow(pos=vector(-1,0,0), axis=vector(2,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,-1,0), axis=vector(0,2,0), shaftwidth=0.01)            

body = sphere(radius = 0.05)
body.color = color.orange 

R = 0.5

body.pos = vector(R,0,0)

velocity = vector(0,1,0) 

# Set time interval
dt = 0.01 

# Set refresh rate
while True:   
        
    rate(100)
    
    a_N = mag(velocity)**2 / R
    acceleration = - a_N * body.pos / R
    
    velocity = velocity + acceleration *dt
    body.pos = body.pos + velocity *dt

