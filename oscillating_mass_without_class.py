# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:17:57 2020

@author: Andrea Bassi
"""
import vpython as vp
import numpy as np

K = 1 # Elastic constant
M = 1 # Mass
LENGTH = 1 # Spring length
RADIUS = 0.15*LENGTH # Mass radius

rest_position    = vp.vector(LENGTH,0,0)
initial_position = vp.vector(1.5,0,0)
initial_velocity = vp.vector(0,0,0)

# Create a mass  
mass = vp.sphere()
mass.pos = initial_position
mass.radius = RADIUS
mass.velocity = initial_velocity
mass.color = vp.vector(0,0.56,0.61)             

# Create a spring        
spring = vp.helix()
spring.pos =  vp.vector(0,0,0)
spring.axis = mass.pos
spring.thickness = 0.05
spring.radius = 0.3*RADIUS
spring.color = vp.color.orange

# Set temporal sampling to 1/100 of the inverse of the oscillation frequency
dt = 0.01*(2*np.pi*np.sqrt(M/K)) 

while True:  
    vp.rate(100)  
    mass.pos = mass.pos + mass.velocity*dt
    spring.axis = mass.pos  
    delta = mass.pos - rest_position
    acceleration = - (K* delta) / M     
    mass.velocity = mass.velocity + acceleration * dt
    