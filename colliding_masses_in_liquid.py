# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:31:32 2020

@author: Andrea Bassi
"""

from vpython import scene, vector, curve, color, rate, sphere, mag
from colliding_masses import system


# Draw box
L=2
d = L/2
r = 0.005
gray = color.gray(0.7)
boxbottom = curve(color=gray, radius=r)
boxbottom.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d)])
boxtop = curve(color=gray, radius=r)
boxtop.append([vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,d,-d), vector(-d,d,-d)])
vert1 = curve(color=gray, radius=r)
vert2 = curve(color=gray, radius=r)
vert3 = curve(color=gray, radius=r)
vert4 = curve(color=gray, radius=r)
vert1.append([vector(-d,-d,-d), vector(-d,d,-d)])
vert2.append([vector(-d,-d,d), vector(-d,d,d)])
vert3.append([vector(d,-d,d), vector(d,d,d)])
vert4.append([vector(d,-d,-d), vector(d,d,-d)])

delta_t = 0.01 
    
N =50 # number of bodies

masses =[]
initial_positions = []
initial_velocities = []

for idx in range(N): 
    # Each body has the same mass: the mass of the Moon 
    masses.append(0.5)   # kg  
    # Place the masses randomly in space
    initial_positions.append(vector.random()) # m
    # Give random initial velocities
    initial_velocities.append(vector.random()) # m/2

sys = system(masses, initial_positions, initial_velocities, delta_t)

trace = sphere(radius = 1e-2,
                    make_trail=True,
                    trail_type="points",
                    trail_radius= 5e-3,
                    interval=5,
                    retain=50) 

while True:   
        
    rate(150)
    
    B = 0.05
    for body in sys.bodies: 
        body.acceleration = - B * body.velocity *mag(body.velocity)
    
    sys.set_velocity()
    
    sys.set_position()
    sys.bounce_on_border(L)

    sys.check_collisions()
    sys.elastic_collision()
    
    
    center_mass, KE = sys.calculate_center_of_mass_and_energy()
    trace.pos = center_mass        
    
