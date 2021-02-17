# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 22:38:55 2021

@author: Andrea Bassi
"""

import vpython as vp

from coupled_oscillators import Coupled_Oscillator

class System():
    
    def __init__(self, n):
        self.n = n # number of oscillators
        oscillators = []
        k=1; m=2; r=0.15; l=1
        osc0 = Coupled_Oscillator(k, m, r, l, origin=vp.vector(-N*l/2,0,0))
        oscillators.append(osc0)
        for idx in range(n):                                  
            osc = Coupled_Oscillator(k, m, r, l, origin=oscillators[idx].body.pos)
            oscillators.append(osc)
        self.oscillators = oscillators
        
    def unbind(self, idx=0):
        # Removes the spring of the oscillator number idx. 
        # If idx==0  removes the sping and the boundary to a fixed origin
        osc = self.oscillators[idx]
        r = osc.body.pos - osc.origin
        ur = r/vp.mag(r)
        l = osc.length
        osc.origin = osc.body.pos - l * ur 
        osc.spring.visible = False
        
            
    def get_accelerations(self):        
        for idx,osc in enumerate(self.oscillators):
            if idx == self.n:
                osc.calculate_acceleration()
            else:
                osc.calculate_acceleration(self.oscillators[idx+1])
        
    def update_positions(self, dt):
        for idx,osc in enumerate(self.oscillators):
            osc.set_velocity(dt)
            osc.set_position(dt)
    
    def set_displacement(self, idx, delta):
        osc = self.oscillators[idx]
        osc.body.pos+=delta
        if idx < self.n:
            next_osc = self.oscillators[idx+1]
            next_osc.origin = osc.body.pos     
    
    def calculate_center_of_mass(self):
        c_m =  vp.vector(0,0,0)
        v_m =  vp.vector(0,0,0)
        m_tot = 0
        for index,osc in enumerate(self.oscillators):
            c_m += osc.m * osc.body.pos
            v_m += osc.m * osc.body.velocity
            m_tot += osc.m
        # print('center of mass speed(m/s)):', vp.mag(v_m/m_tot),'\n'
        #       'total mass (kg):', m_tot)
        return (c_m/m_tot)
    
    def show_center_of_mass(self, center_mass):
        if not hasattr(self, "center_mass_trace"):
            self.center_mass_trace = vp.sphere(radius = 0.05,
                                               make_trail=True,
                                               trail_type="points",
                                               trail_radius= 0.02,
                                               interval=10,
                                               retain=50)
        else:
            self.center_mass_trace.pos = center_mass
                                   
N = 8
sys = System(N)

delta=vp.vector(0.6,0.0,0.0)
sys.set_displacement(idx=4,delta=delta)

osc0 = sys.oscillators[0]        
dt = 0.01*2*vp.pi*vp.sqrt(osc0.m/osc0.k)

while True:
    vp.rate(100)
    
    sys.unbind(idx=0)
    sys.get_accelerations()
    sys.update_positions(dt)           
    
    sys.show_center_of_mass(sys.calculate_center_of_mass())
        