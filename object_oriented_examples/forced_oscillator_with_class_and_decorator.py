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
RADIUS = 0.1 # Mass radius

rest_position    = vp.vector(LENGTH,0,0)
initial_position = vp.vector(1,0,0)
initial_velocity = vp.vector(0,0,0)
#initial_velocity = 1.0*vp.sqrt(K/M) * vp.vector(1,0,0)

# forced oscillation parameters
B = 0.3 # Ns/m
omega = 1.5 # rad/s
print("Applied frequency:", omega) 
F0 = 0.5 # N
# calculate and display resonance parameters
omega0 = np.sqrt(K/M) # rad/s
resonance_frequency = np.sqrt(omega0**2 - (B/M)**2/2) # rad/s 
print("Resonance frequency:", resonance_frequency)    
expected_amplitude = F0/M/np.sqrt((omega0**2-omega**2)**2+(B/M)**2*omega**2)
print("Expected amplitude:", expected_amplitude)


# Set temporal sampling to 5/1000 of the inverse of the oscillation frequency
dt = 0.005*(2*np.pi*np.sqrt(M/K)) 

axis_x = vp.arrow(pos = vp.vector(0,0,0), axis=vp.vector(2,0,0),shaftwidth=0.005, headwidth=0.04, headlength = 0.05)            
axis_y = vp.arrow(pos = vp.vector(1,-1,0), axis=vp.vector(0,2,0),shaftwidth=0.005,headwidth=0.04, headlength = 0.05)            

vp.scene.center = rest_position

class oscillator:
        
    def __init__(self, radius, r0, v0):
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
        self.amplitude = vp.vector(0,0,0) # oscillator property
        
    def set_time(self,dt):
        self.time += dt    
        
    def set_position(self, velocity,dt):
        self.mass.pos = self.mass.pos + velocity*dt
        self.spring.axis = self.mass.pos
    
    def set_velocity(self, acceleration,dt):
        self.mass.velocity = self.mass.velocity + acceleration * dt
  
    @property    
    def amplitude(self):
        return self._amp
    
    @amplitude.setter    
    def amplitude(self, delta):
        if hasattr(self,'_amp'):
            if vp.mag(delta) > vp.mag(self.amplitude):
                self._amp = delta
                #print the maxium distance from rest position, during the entire oscillation
                print("\rMeasured amplitude:", vp.mag(delta), end ='')
        else:       
            self._amp = delta
            
         
# create oscillator instance
osc = oscillator(RADIUS, initial_position, initial_velocity)

time = 0

vp.graph(scroll=True,
         fast=False,
         xmin=0, xmax=50,
         xtitle = 'times(s)',
         ytitle = 'delta (m)')

g0 = vp.gcurve()
#g1 = vp.gcurve(color = vp.color.red)


while True:
    
    vp.rate(100)   
    
    # add elastic force
    delta = osc.mass.pos - rest_position
    elastic_force = - (K* delta) / M
    
    # add fluid resistance
    dumping_force = - B * osc.mass.velocity
    
    # add external force oscillating at angular frequency omega
    external_force = F0 * np.cos(omega*time) * vp.vector(1,0,0)
    
    # calulate acceleration
    acceleration = ( elastic_force + dumping_force + external_force ) / M 
    
    # update velocity, position and time
    osc.set_velocity(acceleration, dt)
    osc.set_position(osc.mass.velocity,dt)   
    time = time + dt
    
    # update amplitude
    osc.amplitude = delta
    
    g0.plot( time, delta.x )
    
    #g1.plot( time, external_force.x )
    