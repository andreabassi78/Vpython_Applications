# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:12:04 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, color, sphere, pi, mag, rate

G = 6.67408e-11 # Gravitational constant. All Units are in SI

class system:
        
    def __init__(self, ms, r0s, v0s ):
        self.bodies = []
        # Create the masses  
        for index, m in enumerate(ms):
            body =  sphere()
            body.mass = m
            body.radius = self.set_radius(m)
            body.pos = r0s[index]
            body.velocity = v0s[index]
            body.color =  vector(0,0.56,0.61)        
            #body.acceleration_arrow =  arrow(pos=body.pos, axis= vector(0,0,0))
            self.bodies.append(body)
    def set_radius(self,mass):
        # Draw a sphere with a radius proportional to the cubic root of the mass
        density = 3000 # kg/m^3
        r = (3/(4*pi)*mass/density)**(1/3) 
        return r
    
    def set_position(self, dt):
        for index, b in enumerate(self.bodies):
            b.pos = b.pos + b.velocity*dt
    
    def set_velocity(self, dt):
        for index, b in enumerate(self.bodies):
            b.velocity = b.velocity + self.accelerations[index]*dt
    
    def calculate_acceleration(self):
        self.accelerations = [] 
        for index,body in enumerate(self.bodies):            
            acceleration =  vector(0,0,0)
            other_index = 0
            while other_index < len(self.bodies): 
                other_body = self.bodies[other_index]
                if index != other_index:
                    distance =  mag (body.pos-other_body.pos)
                    if distance < (body.radius+other_body.radius) and body.visible == True and other_body.visible == True:
                        # in case of collision fuse the 2 objects and recalculate the acceleration repeating the while cycle
                        self.collision(body,other_body)
                        acceleration =  vector(0,0,0) 
                        other_index = 0
                        continue
                    elif body.visible == True and  other_body.visible == True:  
                        acceleration += - (G* other_body.mass) * (body.pos-other_body.pos)/ distance**3
                other_index += 1
                
            self.accelerations.append(acceleration)
            
    def calculate_center_of_mass(self):
        c_m =  vector(0,0,0)
        v_m =  vector(0,0,0)
        m_tot = 0
        for index,body in enumerate(self.bodies):
            c_m += body.mass * body.pos
            v_m += body.mass * body.velocity
            m_tot += body.mass
        print('center of mass speed(m/s)):', mag(v_m/m_tot),'\n'
              'total mass (kg):', m_tot)
        return (c_m/m_tot)    
                    
    def collision(self, body1,body2):
        m1 = body1.mass
        m2 = body2.mass
        # grow body 1 
        body1.pos = (body1.pos*m1+body2.pos*m2)/(m1+m2)
        body1.velocity = (body1.velocity*m1+body2.velocity*m2)/(m1+m2)
        body1.mass += body2.mass
        body1.radius = self.set_radius(body1.mass)
        body1.color =  color.orange
        # body2: set the mass to 0 
        body2.velocity = body1.velocity
        body2.mass = 0
        body2.visible = False
        body2.radius = self.set_radius(body2.mass)
        #print("collision")
               
        
# Set temporal sampling in seconds 
dt = 600 

N = 50 # number of bodies

masses =[]
initial_positions = []
initial_velocities = []

for idx in range(N): 
    # Each body has the same mass: the mass of the Moon 
    masses.append(7.342e22) # kg  
    # Place the masses randomly in space
    initial_positions.append( vector.random()*1e8) # m
    # Give random initial velocities
    initial_velocities.append( vector.random()*500) # m/s

sys = system(masses, initial_positions, initial_velocities)

# add a trace to the center of mass
trace = sphere(radius = 1e6,
               make_trail=True,
               trail_type="points",
               trail_radius= 1e5,
               interval=20,
               retain=50)

scene.caption= "N body problem"

while True:   
    
    rate(50)
    sys.set_position(dt)        
    sys.calculate_acceleration()
    sys.set_velocity(dt) 
    center_mass = sys.calculate_center_of_mass()
    scene.center = center_mass
    trace.pos = center_mass