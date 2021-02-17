# -*- coding: utf-8 -*-
"""
Created on Mon May  4 00:17:57 2020

@author: Andrea Bassi
"""
import vpython as vp

class Oscillator:
    
    ''' 
    Base oscillator class
    '''
    
    def __init__(self, k=1, m=1, radius=0.1, length=1, origin = vp.vector(0,0,0)):
        # create elastic constant and mass attributes
        self.k = k
        self.m = m
        self.length = length
        self.origin = origin
        # Create a body 
        body = vp.sphere()
        body.radius = radius
        body.color = vp.vector(0,0.56,0.61) 
        self.body = body         
        # Create a spring        
        spring = vp.helix()
        spring.thickness = 0.05
        spring.radius = 0.04*length
        spring.color = vp.color.orange
        self.spring = spring
        # Set initial conditions and acceleration to a default value
        self.acceleration = vp.vector(0,0,0)
        self.set_initial_conditions(origin+vp.vector(length,0,0), vp.vector(0,0,0))
        
    def set_position(self, dt):
        self.body.pos = self.body.pos + self.body.velocity*dt
        self.spring.axis = self.body.pos - self.origin
        self.spring.pos = self.origin
    
    def set_velocity(self,dt):
        self.body.velocity = self.body.velocity + self.acceleration * dt
        
    def calculate_acceleration(self):
        r = self.body.pos - self.origin
        l = self.length
        self.dl = dl = vp.mag(r) - l
        if dl/l < -0.95:
            raise ValueError(f'Spring too compressed. Strain value: {dl/l:.2f}')
        else:
             dr = r * (dl/vp.mag(r)) 
             self.acceleration = - (self.k* dr) / self.m 
    
    def set_initial_conditions(self, initial_position, initial_velocity):
        self.body.pos = initial_position 
        self.spring.axis = self.body.pos 
        self.spring.pos = self.origin
        self.body.velocity = initial_velocity
        
    def calculate_energy(self):
        K = 1/2*self.m*vp.mag(self.body.velocity)**2
        U = 1/2*osc.k*(self.dl)**2
        return (K+U)
        
if __name__ == '__main__':            
     
    # Define constants        
    K = 1 # Elastic constant
    M = 1 # Mass
    LENGTH = 1 # Spring length
    RADIUS = 0.15 # Body radius
    
    # Instantiate oscillator
    osc = Oscillator(K, M, RADIUS, LENGTH)
    
    # Define and set initial conditions
    INITIAL_POSITION = vp.vector(1,0,0)
    INITIAL_VELOCITY = vp.vector(0.5,0,0)
    osc.set_initial_conditions(INITIAL_POSITION, INITIAL_VELOCITY)        
        
    # Set temporal sampling to 1/100 of the inverse of the oscillation frequency
    dt = 0.01*2*vp.pi*vp.sqrt(osc.m/osc.k)
        
    while True:
    
        vp.rate(100)
        
        osc.calculate_acceleration()       
        osc.set_velocity(dt)
        osc.set_position(dt)
        
        E = osc.calculate_energy()
        print(f'Mecanical energy: {1000*E:.02f} mJ')

        
    
    