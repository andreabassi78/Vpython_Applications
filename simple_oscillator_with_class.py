# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:17:57 2020

@author: Andrea Bassi
"""
import vpython as vp
import numpy as np

class oscillator:
        
    def __init__(self, k, m, radius, rest_position):
        # create elastic constant and mass attributes
        self.k = k
        self.m = m
        self.rest_position = rest_position
        # Create a body 
        body = vp.sphere()
        body.radius = radius
        body.color = vp.vector(0,0.56,0.61) 
        self.body = body         
        # Create a spring        
        spring = vp.helix()
        spring.thickness = 0.05
        spring.radius = 0.3*radius
        spring.color = vp.color.orange
        self.spring = spring
        # Set initial conditions to a default value
        self.set_initial_conditions()        
        
    def set_position(self, dt):
        self.body.pos = self.body.pos + self.body.velocity*dt
        self.spring.axis = self.body.pos
    
    def set_velocity(self,dt):
        self.body.velocity = self.body.velocity + self.acceleration * dt
        
    def calculate_acceleration(self):
        delta = self.body.pos - self.rest_position
        self.acceleration = - (self.k* delta) / self.m 
    
    def set_initial_conditions(self,
                               initial_position = vp.vector(0,0,0),
                               initial_velocity = vp.vector(0,0,0)
                               ):
        self.body.pos = initial_position
        self.spring.axis = self.body.pos
        self.body.velocity = initial_velocity
        if not hasattr(self, "acceleration"):
            self.acceleration = vp.vector(0,0,0)
            
# Define constants        
K = 1 # Elastic constant
M = 1 # Mass
LENGTH = 1 # Spring length
RADIUS = 0.15*LENGTH # Body radius
REST_POSITION = vp.vector(LENGTH,0,0)

# Instantiate oscillator
osc = oscillator(K, M, RADIUS, REST_POSITION)

# Define and set initial conditions
initial_position = vp.vector(1.5,0,0)
initial_velocity = vp.vector(0,0,0)
osc.set_initial_conditions(initial_position, initial_velocity)        
    
# Set temporal sampling to 1/100 of the inverse of the oscillation frequency
dt = 0.01*2*np.pi*np.sqrt(osc.m/osc.k)

while True:

    vp.rate(50)
    osc.calculate_acceleration()       
    osc.set_velocity(dt)
    osc.set_position(dt) 


    
    