# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, curve, color, sphere, mag, rate, dot, cross
import numpy as np
import random

pi = np.pi

class system:
           
    def __init__(self, ms, r0s, v0s, dt):
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
    
    
    def set_radius(self, mass, density = 200):
        # Draw a sphere with a radius proportional to the cubic root of the volume
        # density is in kg/m^3
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
                        if [other_index, index] not in self.collided_couples: 
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
            ratio0 = 2 * body1.mass / (body0.mass + body1.mass) 
            ratio1 = 2 * body0.mass / (body0.mass + body1.mass) 
            body0.velocity += - ratio0 * dot(vrel,rrel) / a  *rrel 
            body1.velocity += - ratio1 * dot(-vrel,-rrel) / a  *(-rrel)
        self.attached_couples = self.collided_couples.copy()    
        self.collided_couples.clear()
        
        
    def totally_inelastic_collision(self):
        bodies_to_remove = []
        for indexs in self.collided_couples: 
            body0 = self.bodies[indexs[0]]
            body1 = self.bodies[indexs[1]]
            m0 = body0.mass
            m1 = body1.mass
            if m0 ==0 and m1 == 0: continue
            # grow body 1 
            body0.pos = (body0.pos*m0+body1.pos*m1)/(m0+m1)
            body0.velocity = (body0.velocity*m0+body1.velocity*m1)/(m0+m1)
            body0.mass += body1.mass
            body0.radius = self.set_radius(body0.mass)
            # body2: set the mass to 0 
            body1.velocity = body0.velocity
            body1.mass = 0
            body1.visible = False
            body1.radius = self.set_radius(body1.mass)
            bodies_to_remove.append(body1)
        for body in bodies_to_remove:
            if body in self.bodies:
                self.bodies.remove(body)
        self.collided_couples.clear()
        
    def inelastic_collision(self, K=40, B=1):
        # balls are modeled as elastic (springs) with a shear friction
        # K elastic constant
        # B damping coefficient # if B=0 collision is elastic
        acceleration0 = vector(0,0,0)
        acceleration1 = vector(0,0,0)
        for indexs in self.collided_couples: 
            body0 = self.bodies[indexs[0]]
            body1 = self.bodies[indexs[1]]
            vrel = body0.velocity - body1.velocity
            rrel = body0.pos-body1.pos
            distance =  mag (rrel)
            F = + K * rrel / distance * (body0.radius+body1.radius-distance)  - B * vrel
            acceleration0 = + F / body0.mass
            acceleration1 = - F / body1.mass
            body0.velocity += acceleration0*self.dt
            body1.velocity += acceleration1*self.dt    
        self.collided_couples.clear()
        
        
    def partially_inelastic_collision(self):
        # totally inelastic collision, but if the couple of bodies collides with others can breack 
        bodies_to_remove = []
        for indexs in self.collided_couples: 
            body0 = self.bodies[indexs[0]]
            body1 = self.bodies[indexs[1]]
            m0 = body0.mass
            m1 = body1.mass
            # grow body 1 
            cm_pos = (body0.pos*m0+body1.pos*m1)/(m0+m1)
            cm_velocity = (body0.velocity*m0+body1.velocity*m1)/(m0+m1)            
            dr0 = body0.pos-cm_pos
            dv0 = body0.velocity-cm_velocity 
            dr1 = body1.pos-cm_pos
            dv1 = body1.velocity-cm_velocity            
            omega0 = cross(-dv0,dr0)/mag(dr0)**2            
            omega1 = cross(-dv1,dr1)/mag(dr1)**2
            #assert omega0 == omega1
            body0.velocity = cm_velocity + cross(omega0, dr0)
            body1.velocity = cm_velocity + cross(omega1, dr1)
        self.collided_couples.clear()
        
        
    def bounce_on_border(self, L = 2):     
        for index,body in enumerate(self.bodies):
            loc = body.pos
            vel = body.velocity
            if abs(loc.x) > L/2:
                if loc.x < 0: vel.x =  abs(vel.x)
                else: vel.x =  -abs(vel.x)
            if abs(loc.y) > L/2:
                if loc.y < 0: vel.y = abs(vel.y)
                else: vel.y =  -abs(vel.y)
            if abs(loc.z) > L/2:
                if loc.z < 0: vel.z =  abs(vel.z)
                else: vel.z =  -abs(vel.z)
                
        
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
        print('Kinetic Energy (J):', KE)
        #print('Center of Mass velocity:', mag(v_m/m_tot))
        return c_m/m_tot , KE        
      
         
if __name__ == '__main__':
    
    
    scene.caption= "Bouncing balls"

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
    
    # Set temporal sampling in seconds 
    delta_t = 0.005 
    
    N =30 # number of bodies
    
    masses =[]
    initial_positions = []
    initial_velocities = []
    
    for idx in range(N): 
        # Each body has the same mass: the mass of the Moon 
        masses.append(1)   # kg  
        # Place the masses randomly in space
        initial_positions.append(vector.random()) # m
        # Give random initial velocities
        initial_velocities.append(vector.random()) # m/2
    
    sys = system(masses, initial_positions, initial_velocities, delta_t)
    
    # add a trace to the center of mass
    trace = sphere(radius = 1e-2,
                    make_trail=True,
                    trail_type="points",
                    trail_radius= 5e-3,
                    interval=5,
                    retain=50) 
    
    while True:   
        
        rate(150)
        
        sys.set_position()
        sys.bounce_on_border(L)        
        
        sys.check_collisions()
        sys.inelastic_collision()
        
        center_mass, KE = sys.calculate_center_of_mass_and_energy()
        trace.pos = center_mass
        