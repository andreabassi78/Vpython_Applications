# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:58:34 2021

@author: Andrea Bassi
"""
import vpython as vp

from simple_oscillator_with_class import Oscillator

class Dumped_Oscillator(Oscillator):
    
    def __init__(self, k, m, beta, radius, length):
        super().__init__(k, m, radius, length)
        self.beta = beta
                
    def dump(self):
        self.acceleration += -self.beta*self.body.velocity/self.m 
        

osc = Dumped_Oscillator(k=1, m=1, beta=0.1, radius=0.15, length=1)

osc.set_initial_conditions(vp.vector(1.5,0,0), vp.vector(0,0,0))  

dt = 0.01*2*vp.pi*vp.sqrt(osc.m/osc.k)

while True:
    vp.rate(100)
    osc.calculate_acceleration() 
    osc.dump()      
    osc.set_velocity(dt)
    osc.set_position(dt)
    

