"""
Created on Mon May  6 10:10:23 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, rate, sin, cos, attach_trail, pi, mag

body = sphere(radius = 0.05)
body.color = color.orange 

R = 1


body.velocity = vector(0,1,0)
body.pos = vector(R,0,0)

attach_trail(body)


time = 0

dt = 0.01

axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            


while True:   
    
    rate(100)
    
    time = time + dt
    
    acceleration_C = mag(body.velocity)**2/R
    
    acceleration = - acceleration_C * body.pos / R
        
    body.velocity = body.velocity + acceleration *dt
    body.pos = body.pos + body.velocity *dt
    
    # scene.caption= ("t:  "+ str(round(time,2))+"s"+ "\n"
    #                 "x: "+ str(round(body.pos.x,3)),"m","\n"
    #                 "y: "+ str(round(body.pos.y,3)),"m")
    
    
    