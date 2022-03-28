# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, curve, color, sphere, mag, rate, attach_trail, dot,cross
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
        
    def __init__(self, ms, r0s, v0s, dt ):
        self.bodies = []
        self.collided_couples = []
        self.attached_couples = []
        self.dt = dt
        # Create the masses  
        for index, m in enumerate(ms):
            body =  sphere()
            body.mass = m
            body.radius = self.set_radius(m)
            body.pos = r0s[index]
            body.velocity = v0s[index]
            body.acceleration = vector(0,0,0)
            body.color =  vector(1,random.random(),random.random())
            self.bodies.append(body)
    
    def set_radius(self,mass):
        # Draw a sphere with a radius proportional to the cubic root of the volume
        density = 1000 # kg/m^3
        radius = (3/(4*pi)*mass/density)**(1/3) 
        return radius
    
    def set_position(self):
        for index, b in enumerate(self.bodies):
            b.pos = b.pos + b.velocity*self.dt
    
    def set_velocity(self):
        for index, b in enumerate(self.bodies):
            b.velocity = b.velocity + b.acceleration*self.dt
              
    def check_collisions(self):
        for index,body in enumerate(self.bodies):            
            for other_index, other_body in enumerate(self.bodies) : 
                if index != other_index:
                    distance =  mag (body.pos-other_body.pos)
                    if distance <= (body.radius+other_body.radius):
                        if ([index, other_index] not in self.collided_couples 
                        and [other_index, index] not in self.collided_couples):
                            self.collided_couples.append([index,other_index])
        return(self.collided_couples)                      
                                              
    def elastic_collision(self):
        for indexs in self.collided_couples: 
            if indexs in self.attached_couples: continue
            body0 = self.bodies[indexs[0]]
            body1 = self.bodies[indexs[1]]
            vrel = body0.velocity - body1.velocity
            rrel = body0.pos-body1.pos
            a = rrel.mag2 # magnitude squared
            #if a == 0: continue
            ratio0 = 2 * body1.mass / (body0.mass + body1.mass) 
            ratio1 = 2 * body0.mass / (body0.mass + body1.mass) 
            body0.velocity += - ratio0 * dot(vrel,rrel) / a  *rrel 
            body1.velocity += - ratio1 * dot(-vrel,-rrel) / a  *(-rrel)
        self.attached_couples = self.collided_couples.copy()    
        self.collided_couples.clear()
            
    def elastic_ball_collision(self):
        acceleration0 = vector(0,0,0)
        acceleration1 = vector(0,0,0)
        for indexs in self.collided_couples: 
            #if indexs in self.attached_couples: continue
            body0 = self.bodies[indexs[0]]
            body1 = self.bodies[indexs[1]]
            #body0.acceleration = vector(0,0,0)
            distance =  mag (body0.pos-body1.pos)
            acceleration0 += K * (body0.pos-body1.pos)/distance*(body0.radius+body1.radius-distance)
            acceleration1 +=  - acceleration0
            body0.velocity += acceleration0*self.dt
            body1.velocity += acceleration1*self.dt
        #self.attached_couples = self.collided_couples.copy()  
        self.collided_couples.clear()
        
    def calculate_center_of_mass_and_energy(self):
        c_m =  vector(0,0,0)
        v_m =  vector(0,0,0)
        m_tot = 0
        KE = 0
        for index,body in enumerate(self.bodies):
            c_m += body.mass * body.pos
            v_m += body.mass * body.velocity
            m_tot += body.mass
            KE += 1/2 * body.mass * mag(body.velocity)**2
        #print('Kinetic Energy (J):', KE)
        return c_m/m_tot , KE        
      
         
K = 5000 # elastic constant

# Set temporal sampling in seconds 
delta_t = 0.001 

N =20# number of bodies

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
    initial_velocities.append(vector(random.uniform(-1,1),
                                    random.uniform(-1,1),
                                    0)) # m/2

sys = system(masses, initial_positions, initial_velocities, delta_t)

# add a trace to the center of mass
trace = sphere(radius = 1e-2,
                make_trail=True,
                trail_type="points",
                trail_radius= 5e-3,
                interval=5,
                retain=50) 

while True:   
    
    rate(100)
    sys.set_position()        
    cc = sys.check_collisions()
    #print("Collided couples:",cc)
    sys.elastic_ball_collision()
    center_mass, KE = sys.calculate_center_of_mass_and_energy()
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
    