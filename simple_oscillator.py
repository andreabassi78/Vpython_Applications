# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:17:57 2020

@author: Andrea Bassi
"""
from vpython import sphere, helix, vector, color, rate, sqrt, pi, sin, graph, curve

K = 1 # Elastic constant
M = 1 # Mass
LENGTH = 1 # Spring length
RADIUS = 0.15*LENGTH # Body radius

rest_position    = vector(LENGTH,0,0)
initial_position = vector(1.5,0,0)
initial_velocity = vector(0,0,0)

# Create a body  
body = sphere()
body.pos = initial_position
body.radius = RADIUS
body.velocity = initial_velocity
body.color = vector(0,0.56,0.61)             

# Create a spring        
spring = helix()
spring.pos =  vector(0,0,0)
spring.axis = body.pos
spring.thickness = 0.05
spring.radius = 0.3*RADIUS
spring.color = color.orange

# Set temporal sampling to 1/100 of the inverse of the oscillation frequency
dt = 0.01*(2*pi*sqrt(M/K))

while True:  
    rate(50)  
    body.pos = body.pos + body.velocity*dt
    spring.axis = body.pos
    delta = body.pos - rest_position
    acceleration = - (K* delta) / M
    body.velocity = body.velocity + acceleration * dt
