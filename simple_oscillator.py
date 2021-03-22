# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:17:57 2020

@author: Andrea Bassi
"""
from vpython import sphere, helix, vector, color, rate, sqrt, pi

K = 1 # Elastic constant
M = 1 # Mass
LENGTH = 1 # Spring length
RADIUS = 0.15*LENGTH # Body radius

REST_POSITION    = vector(LENGTH,0,0)
INITIAL_POSITION = vector(1.5,0,0)
INITIAL_VELOCITY = vector(0,0,0)

# Create a body  
body = sphere()
body.pos = INITIAL_POSITION
body.radius = RADIUS
body.velocity = INITIAL_VELOCITY
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
    
    rate(100)  
    
    delta = body.pos - REST_POSITION
    acceleration = - (K* delta) / M
    
    body.velocity = body.velocity + acceleration * dt
    
    body.pos = body.pos + body.velocity*dt
    spring.axis = body.pos
    