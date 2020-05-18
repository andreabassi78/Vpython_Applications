# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:17:57 2020

@author: Andrea Bassi
"""
from vpython import sphere, helix, vector, color, rate, sqrt, pi, sin

K = 1 # Elastic constant
M = 1 # Mass
LENGTH = 1 # Spring length
RADIUS = 0.15*LENGTH # Mass radius

rest_position    = vector(LENGTH,0,0)
initial_position = vector(1.5,0,0)
initial_velocity = vector(0,0,0)

# Create a mass  
mass = sphere()
mass.pos = initial_position
mass.radius = RADIUS
mass.velocity = initial_velocity
mass.color = vector(0,0.56,0.61)             

# Create a spring        
spring = helix()
spring.pos =  vector(0,0,0)
spring.axis = mass.pos
spring.thickness = 0.05
spring.radius = 0.3*RADIUS
spring.color = color.orange

# Set temporal sampling to 1/100 of the inverse of the oscillation frequency
dt = 0.01*(2*pi*sqrt(M/K))

while True:  
    rate(100)  
    mass.pos = mass.pos + mass.velocity*dt
    spring.axis = mass.pos
    delta = mass.pos - rest_position
    acceleration = - (K* delta) / M 
    mass.velocity = mass.velocity + acceleration * dt
    