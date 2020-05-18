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

# Set temporal sampling to 1/100 of the inverse of the oscillation frequency
dt = 0.01*(2*np.pi*np.sqrt(M/K)) 

rest_position    = vp.vector(LENGTH,0,0)
initial_position = vp.vector(1.5,0,0)
initial_velocity = vp.vector(0,0,0)
#initial_velocity = 1.0*vp.sqrt(K/M) * vp.vector(1,0,0)

class oscillator:
        
    def __init__(self, radius, r0, v0 ):
        # Create a mass  
        mass = vp.sphere()
        mass.pos = r0
        mass.radius = radius
        mass.velocity = v0
        mass.color = vp.vector(0,0.56,0.61)        
        self.mass = mass         
        # Create a spring        
        spring = vp.helix()
        spring.pos =  vp.vector(0,0,0)
        spring.axis = mass.pos
        spring.thickness = 0.05
        spring.radius = 0.3*radius
        spring.color = vp.color.orange
        self.spring = spring      
        
    def set_position(self, velocity,dt):
        self.mass.pos = self.mass.pos + velocity*dt
        self.spring.axis = self.mass.pos
    
    def set_velocity(self, acceleration,dt):
        self.mass.velocity = self.mass.velocity + acceleration * dt

osc = oscillator(RADIUS, initial_position, initial_velocity)


vp.graph(scroll=True,
         fast=False,
         xmin=0, xmax=100,
         xtitle = 'times(s)',
         ytitle = 'delta (m)')

g = vp.gcurve()

time = 0

while True:
    
    vp.rate(100)
    
    time = time + dt
    osc.set_position(osc.mass.velocity,dt)        
    delta = osc.mass.pos - rest_position
    acceleration = - (K* delta) / M 
    osc.set_velocity(acceleration, dt)
    
    g.plot( time, delta.x )
    
    