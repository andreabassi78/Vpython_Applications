# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:13:00 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, sin, cos, arrow,cone, quad, text, cross,dot, rate, mag, mag2, textures, vertex, pi, color
  
LENGTH = 1.5

SHAFTWIDTH = LENGTH/80
HEADWIDTH = LENGTH/30
HEADLENGTH = LENGTH/15

RADIUS = 0.35 * LENGTH # arbitrary value        
MASS = 0.1 # kg
I = 3 * MASS * RADIUS**2 /10 # moment of inertia of the cone

OMEGA = 2*pi*15 # rotation frequancy rad/s 

ALPHA = 30 * pi/180 # initial orientation in xz plane     

class spinning_top:
    
    def __init__(self, omega0):
        
        self.origin = vector(0,0,0)
        L = I * omega0
        self.base = base = L /mag(L) * LENGTH
        self.vert = - self.base
        self.c_m = base * 3/4
        self.t = vector (1,0,0)
        
        self.animated_objects = {}
        
        self.L = I * omega0
        self.add_arrow({"name" : 'angular momentum',
                        "pos" : 'base',
                        "axis" : 'L',
                        "color" : color.magenta})
        
        self.weight = MASS*vector(0,-9.81,0)
        self.add_arrow({"name" : 'weight',
                        "pos" : 'c_m',
                        "axis" : 'weight',
                        "color" : color.white})
    
        self.norm = -self.weight
        self.add_arrow({"name" : 'floor reaction',
                        "pos" : 'origin',
                        "axis" : 'norm',
                        "color" : color.cyan})
        
        self.torque = cross(self.c_m, self.weight)
        self.add_arrow({"name" : 'torque',
                        "pos" : 't',
                        "axis" : 'torque',
                        "color" : color.green})

        c = cone(pos = self.base,
                 axis =  - self.base,
                 radius = RADIUS,
                 length = LENGTH,
                 texture = {'file':'kandinsky.jpg'}
                 )
        c.properties = ({"name" : 'cone',
                         "pos" : 'base',
                         "axis" : 'vert'})
        self.animated_objects['cone'] = c
        
        # Print precession frequency
        theo_omega = mag(self.weight) * mag(self.c_m) / I / mag(omega0) 
        print ('Calculated precession frequency:', theo_omega/(2*pi),'Hz')
        precession_omega = dot(cross(self.L,self.torque)/mag2(self.L),vector(0,1,0))*vector(0,1,0)
        precession_omega = cross(self.L,self.torque)/mag2(self.L) / sin(ALPHA)
        print ('Measured precession frequency:', mag(precession_omega)/(2*pi),'Hz')       
    
    def add_arrow(self, properties):
        vect_arrow = arrow(pos = vector(0,0,0),
                           axis=vector(0,1,0),
                           shaftwidth=SHAFTWIDTH, headwidth=HEADWIDTH, headlength = HEADLENGTH,
                           color = properties["color"])          
        vect_arrow.properties = properties
        self.animated_objects[properties["name"]]= vect_arrow
        #print(self.animated_objects['angular momentum'])
        
    def set_animated_objects(self):
        for _key,ani_obj in self.animated_objects.items():
            ani_obj.pos  = getattr(self,ani_obj.properties['pos'])
            ani_obj.axis = getattr(self,ani_obj.properties['axis'])
            
    def rotate_cone(self,dt):
        rot_angle = OMEGA*dt  
        self.animated_objects['cone'].rotate(angle=rot_angle, axis=self.c_m, origin = vector(0,0,0) )
        self.set_animated_objects()
                     
    def set_torque(self):
        self.torque = cross(self.c_m, self.weight)
           
    def set_L(self,dt):     
        self.L += self.torque *dt      
        self.base = base = self.L /mag(self.L) * LENGTH
        self.t = base + self.L # application point of the torque, for visualization only
        self.vert = -base
        self.c_m = base * 3/4  
        
# sampling time
dt = 2*pi/OMEGA /100

# create instance of the spinning top
initial_orientation = vector(0, cos(ALPHA), sin(ALPHA))
st = spinning_top(OMEGA*initial_orientation)

# create floor
a = vertex( pos=vector(-1,0,-1) * LENGTH, texpos=vector(0,0,0))
b = vertex( pos=vector(1,0,-1) * LENGTH , texpos=vector(1,0,0))
c = vertex( pos=vector(1,0,1) * LENGTH , texpos=vector(1,1,0))
d = vertex( pos=vector(-1,0,1) * LENGTH, texpos=vector(0,1,0))

Q = quad( vs =[a,b,c,d], 
          texture = textures.wood )

# text(text='Angular momentum', align='upper_right', color=color.magenta, height = 0.1, pos=vector(0.5,2,0))
# text(text='Torque', align='lower_right', color=color.green, height = 0.1, pos=vector(0.5,1.85,0) )
# text(text='Weight', align='lower_right', color = color.white, height = 0.1, pos=vector(0.5,1.7,0) )
# text(text='Floor reaction', align='lower_right', color=color.cyan, height = 0.1, pos=vector(0.5,1.55,0) )

scene.waitfor('textures')
scene.center = vector(0,LENGTH,0)

while True:
    rate(100)
    st.rotate_cone(dt)
    st.set_torque()
    st.set_L(dt)        
    
    scene.caption= ("Precession of the spinning top \n"
                    "Assumes rotation frequency >> precession frequency \n"
                    "Static friction is not shown")
    