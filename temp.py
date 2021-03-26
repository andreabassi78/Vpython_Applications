"""
Created on Mon May  6 10:10:23 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, rate, sin, cos, attach_trail, pi

import vpython as vp

vp.no_notebook.__server.shutdown()
vp.no_notebook.__interact_loop.stop()

body = sphere(radius = 0.05)
body.color = color.orange 

R = 1

# acceleration = vector(0,-9.81,0) 
# body.velocity = vector(2,2,0)
body.pos = vector(1,0,0)

attach_trail(body)

omega = 5 # rad/s


time = 0

dt = 0.001

axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            


while True:   
    
    rate(100)
    
    time = time + dt
    
    body.pos.x = R* cos(omega*time)
    body.pos.y = R* sin(omega*time)
    
    # body.velocity = body.velocity + acceleration *dt
    # body.pos = body.pos + body.velocity *dt
    
    # scene.caption= ("t:  "+ str(round(time,2))+"s"+ "\n"
    #                 "x: "+ str(round(body.pos.x,3)),"m","\n"
    #                 "y: "+ str(round(body.pos.y,3)),"m")
    
    
    