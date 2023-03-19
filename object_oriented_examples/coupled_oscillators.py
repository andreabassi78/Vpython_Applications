# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:58:34 2020

@author: Andrea Bassi
"""
import vpython as vp

from simple_oscillator_with_class import Oscillator

class Coupled_Oscillator(Oscillator):
    
    def update_origin(self, origin):
        self.origin = origin
        
                         
    def calculate_acceleration(self, other=None):
        if other is None:
            super().calculate_acceleration()
        else:
            r0 = self.body.pos - self.origin
            l0 = self.length
            dl0 = vp.mag(r0) - l0
            self.dl = dl0 # useful to calculate potential energy
            r1 = other.body.pos - other.origin
            l1 = other.length
            dl1 = vp.mag(r1) - l1
            
            if dl0/l0 < -0.95 or dl1/l1 < -0.95 :
                raise ValueError('Spring too compressed')
            else:
                 dr0 = r0 * (dl0/vp.mag(r0))
                 dr1 = r1 * (dl1/vp.mag(r1)) 
                 self.acceleration = - (self.k* dr0) / self.m + (other.k* dr1) / self.m
        

if __name__ == '__main__':  
                                  
    osc0 = Coupled_Oscillator(k=1, m=1, radius=0.15, length=1, origin=vp.vector(0,0,0))
    osc1 = Coupled_Oscillator(k=1, m=1, radius=0.15, length=1, origin=vp.vector(osc0.body.pos))
    
    osc1.set_initial_conditions(osc1.body.pos, vp.vector(0.5,0,0))  
    
    dt = 0.01*2*vp.pi*vp.sqrt(osc0.m/osc0.k)
    
    while True:
        vp.rate(100)
        osc0.calculate_acceleration(osc1) 
        osc1.calculate_acceleration() 
        
        osc0.set_velocity(dt)
        osc1.set_velocity(dt)
        
        osc0.set_position(dt)           
        osc1.update_origin(osc0.body.pos)      
        osc1.set_position(dt)           
        