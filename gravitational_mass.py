# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:12:04 2020

@author: Andrea Bassi
"""
import vpython as vp


#vp.scene.center = vp.vector(0,0,0)

axes = [vp.vector(1,0,0), vp.vector(0,1,0), vp.vector(0,0,1)]

vp.scene.caption= "N body problem"

class system:
        
    def __init__(self, ms, r0s, v0s ):
        self.bodies = []
        # Create the masses  
        for index, m in enumerate(ms):
            body = vp.sphere()
            body.mass = m
            body.radius = self.set_radius(m)
            body.pos = r0s[index]
            body.velocity = v0s[index]
            body.color = vp.vector(0,0.56,0.61)        
            #body.acceleration_arrow = vp.arrow(pos=body.pos, axis=vp.vector(0,0,0))
            self.bodies.append(body)
    def set_radius(self,mass):
        # Draw a sphere with a radius proportional to the cubic root of the mass
        r = 0.04*mass**(1/3) 
        return r
    
    def set_position(self, dt):
        for index, b in enumerate(self.bodies):
            b.pos = b.pos + b.velocity*dt
    
    def set_velocity(self, dt):
        for index, b in enumerate(self.bodies):
            b.velocity = b.velocity + self.accelerations[index]*dt
            #b.acceleration_arrow.pos = b.pos
            #b.acceleration_arrow.axis = self.accelerations[index]/100
    def calculate_acceleration(self):
        self.accelerations = [] 
        for index,body in enumerate(self.bodies):
            acceleration = vp.vector(0,0,0)   
            for other_index,other_body in enumerate(self.bodies):
                if index != other_index:
                    distance = vp.mag (body.pos-other_body.pos)
                    if distance < body.radius and body.visible == True and other_body.visible == True:
                        self.collision(body,other_body)
                    if distance >0:
                        acceleration += - (G* other_body.mass) * (body.pos-other_body.pos)/ distance**3
                    else:
                        acceleration += vp.vector(0,0,0)
            self.accelerations.append(acceleration)
            
    def calculate_center_of_mass(self):
        c_m = vp.vector(0,0,0)
        v_m = vp.vector(0,0,0)
        m_tot = 0
        for index,body in enumerate(self.bodies):
            c_m += body.mass * body.pos
            v_m += body.mass * body.velocity
            m_tot += body.mass
        #print(m_tot)
        print(vp.mag(v_m/m_tot))
        
        # there is something wrong because the CM is moving    
        return (c_m/m_tot)
        
                    
    def collision(self, body1,body2):
        m1 = body1.mass
        m2 = body2.mass
        # grow body 1 
        body1.velocity = (body1.velocity*m1+body2.velocity*m2)/(m1+m2)
        body1.mass += body2.mass
        body1.radius = self.set_radius(body1.mass)
        body1.color = vp.color.orange
        # remove body2 but set the mass to 0 first
        body2.velocity = body1.velocity
        body2.mass = 0
        body2.visible = False
        body2.radius = self.set_radius(body2.mass)
        #self.bodies.remove(body2)
        #del(body2)
        print("collision")
                
        

G = 0.1 # Gravitational constant
# Set temporal sampling 
dt = 0.01 

N = 50 # number of bodies

masses =[]
initial_positions = []
initial_velocities = []

for idx in range(N):    
    masses.append(1.0)     
    initial_positions.append(vp.vec.random())
    initial_velocities.append(vp.vec.random())

sys = system(masses, initial_positions, initial_velocities)

while True:   
    vp.rate(100)
    sys.set_position(dt)        
    sys.calculate_acceleration()
    sys.set_velocity(dt) 
    #print(len(sys.bodies))
    vp.scene.center = sys.calculate_center_of_mass()