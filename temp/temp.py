# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color,curve, sphere, mag, rate, attach_trail, dot,cross
import numpy as np
import random

scene.caption= "Bouncing balls"
pi = np.pi

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


class system:
        
    def __init__(self, ms, r0s, v0s ):
        self.bodies = []
        self.collided_couple = []
        # Create the masses  
        for index, m in enumerate(ms):
            body =  sphere()
            body.mass = m
            body.radius = self.set_radius(m)
            body.pos = r0s[index]
            body.velocity = v0s[index]
            #body.acceleration = 0.0
            body.color =  vector(1,random.random(),random.random())
            #body.acceleration_arrow =  arrow(pos=body.pos, axis= vector(0,0,0))
            self.bodies.append(body)
    def set_radius(self,mass):
        # Draw a sphere with a radius proportional to the cubic root of the volume
        density = 1000 # kg/m^3
        r = (3/(4*pi)*mass/density)**(1/3) 
        return r
    
    def set_position(self, dt):
        for index, b in enumerate(self.bodies):
            b.pos = b.pos + b.velocity*dt
    
    def set_velocity(self, dt):
        for index, b in enumerate(self.bodies):
            b.velocity = b.velocity + b.acceleration*dt
            #b.acceleration_arrow.pos = b.pos
            #b.acceleration_arrow.axis = self.accelerations[index]/100

    def calculate_acceleration(self):
        for index,body in enumerate(self.bodies): 
            body.acceleration = vector(0,0,0)
            for (other_index, other_body) in enumerate(self.bodies) : 
                if index != other_index:
                    distance =  mag (body.pos-other_body.pos)
                    if distance <= (body.radius+other_body.radius):
                       # if (index,other_index) not in self.collided_couple:
                            body.acceleration +=  K * (body.pos-other_body.pos)/distance*(distance-other_body.radius)
                            #self.collided_couple.append((other_index,index))
                            
                            
    def calculate_center_of_mass(self):
        c_m =  vector(0,0,0)
        v_m =  vector(0,0,0)
        m_tot = 0
        for index,body in enumerate(self.bodies):
            c_m += body.mass * body.pos
            v_m += body.mass * body.velocity
            m_tot += body.mass
        # print('center of mass speed(m/s)):', mag(v_m/m_tot),'\n'
        #       'total mass (kg):', m_tot)
        return (c_m/m_tot)    
                    
    def elastic_collision(self, body1, body2):
    
        vrel = body1.velocity - body2.velocity
        rrel = body1.pos-body2.pos
        a = rrel.mag2 # magnitude squared
        
        ratio1 = 2 * body2.mass / (body1.mass + body2.mass) 
        ratio2 = 2 * body1.mass / (body1.mass + body2.mass) 
        
        body1.velocity += - ratio1 * dot(vrel,rrel) / a  *rrel 
        body2.velocity += - ratio2 * dot(-vrel,-rrel) / a  *(-rrel) 
      
         
K = 1000 # elastic constant

# Set temporal sampling in seconds 
dt = 0.005 

N = 10# number of bodies

masses =[]
initial_positions = []
initial_velocities = []

for idx in range(N): 
    # Each body has the same mass: the mass of the Moon 
    masses.append(1)   # kg  
    # Place the masses randomly in space
    initial_positions.append(vector(random.uniform(-1,1),
                                    random.uniform(-1,1),
                                    0)) # m
    # Give random initial velocities
    initial_velocities.append(vector(random.uniform(0,0),
                                    random.uniform(0,0),
                                    0)) # m/2

sys = system(masses, initial_positions, initial_velocities)

# add a trace to the center of mass
trace = sphere(radius = 1e-2,
                make_trail=True,
                trail_type="points",
                trail_radius= 1e-3,
                interval=20,
                retain=50)


while True:   
    
    rate(150)
    sys.set_position(dt)        
    sys.calculate_acceleration()
    sys.set_velocity(dt) 
    center_mass = sys.calculate_center_of_mass()
    trace.pos = center_mass
    
    for index,body in enumerate(sys.bodies):
        loc = body.pos
        p = body.velocity
        if abs(loc.x) > L/2:
            if loc.x < 0: p.x =  abs(p.x)
            else: p.x =  -abs(p.x)
        
        if abs(loc.y) > L/2:
            if loc.y < 0: p.y = abs(p.y)
            else: p.y =  -abs(p.y)
        
        if abs(loc.z) > L/2:
            if loc.z < 0: p.z =  abs(p.z)
            else: p.z =  -abs(p.z)
    