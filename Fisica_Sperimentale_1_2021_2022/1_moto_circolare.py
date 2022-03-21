# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 17:19:47 2022

@author: andrea
"""

from vpython import scene, vector, arrow, color, sphere, rate, sin, cos, attach_trail


body = sphere(radius=0.05)
body.color = color.orange

R = 1

body.pos = vector(R,0,0)

attach_trail(body)

omega = 5 # rad/s velocità angolare (costante)

time = 0
dt = 0.001

axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)


while True:
    
    rate(100)
    time = time + dt
    theta = omega*time
    body.pos.x = R*cos(theta) # coordinata x in un moto circolare uniforme
    body.pos.y = R*sin(theta)
    
    
    