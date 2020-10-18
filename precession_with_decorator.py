# -*- coding: utf-8 -*-
"""
Created on Sat May 16 22:13:00 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, sin, cos, arrow,cone, quad, text, cross,dot, rate, mag, mag2, textures, vertex, pi, color

LENGTH = 1.5

SHAFTWIDTH = LENGTH/80
HEADWIDTH = LENGTH/30
HEADLENGTH = LENGTH/20

RADIUS = 0.35 * LENGTH # arbitrary value        
MASS = 0.1 # kg
I = 3 * MASS * RADIUS**2 /10 # moment of inertia of the cone

OMEGA = 2*pi * 15 # rotation frequancy rad/s
ALPHA = 30 * pi/180 # initial orientation in xz plane


def vectorize(function):
    COLORS = (color.magenta,color.green,color.white,color.cyan,color.purple)
    APPLICATION_POINTS = ('base','t','c_m','origin','origin')
    # decorator used to show vectors as arrows in space,
    # shown vectors are the ones retured by "function" 
    def inner(*args,**kwargs):
        vs = function(*args)
        sys = args[0]
        
        for index, v in enumerate(vs):
            if not inner.called: 
                inner.arrows[index]=arrow(color=COLORS[index],shaftwidth=SHAFTWIDTH,headwidth=HEADWIDTH,headlength=HEADLENGTH)               
            inner.arrows[index].pos = getattr(sys,APPLICATION_POINTS[index])
            inner.arrows[index].axis = v
        inner.called = True
        #return vs
        
    inner.called = False
    inner.arrows = {}
    return inner

class spinning_top:
    
    def __init__(self, omega0):
        
        self.origin = vector(0,0,0)
        self.L = I * omega0
        self.base = base = self.L /mag(self.L) * LENGTH
        self.c_m = base * 3/4
        self.t = self.base + self.L # application point of the torque, for visualization only
        self.weight = MASS*vector(0,-9.81,0)
        self.norm = -self.weight
        self.torque = cross(self.c_m, self.weight)
        self.precession_omega = p_o = cross(self.L,self.torque)/mag2(self.L) / sin(ALPHA)
        self.friction =  - MASS * cross(p_o,cross(p_o,self.c_m))

        self.cone = cone(pos = self.base,
                         axis =  - self.base,
                         radius = RADIUS,
                         length = LENGTH,
                         texture = {'file':'/images/kandinsky.jpg'}
                         )
        
        #self.application_points = { 'L':'base', 'torque':'t', 'weight':'c_m', 'norm': 'origin' }
        #self.colors = { 'L':color.green,'torque':color.white,'weight':color.magenta,'norm':color.cyan }
        
        # Print precession frequency
        #theo_omega = mag(self.weight) * mag(self.c_m) / I / mag(omega0) 
        #print ('Calculated precession frequency:', theo_omega/(2*pi),'Hz')
        #precession_omega = cross(self.L,self.torque)/mag2(self.L) / sin(ALPHA)
        #print ('Measured precession frequency:', mag(precession_omega)/(2*pi),'Hz')       
               
    def move_cone(self,dt):
        rot_angle = OMEGA*dt  
        self.cone.rotate(angle=rot_angle, axis=self.c_m, origin = vector(0,0,0))
        self.cone.pos = self.base
        self.cone.axis = -self.base  
        
    @vectorize       
    def set_vectors(self,dt): 
        self.torque = cross(self.c_m, self.weight)
        self.L += self.torque *dt      
        self.base = base = self.L /mag(self.L) * LENGTH
        self.t = base + self.L # application point of the torque, for visualization only
        self.c_m = base * 3/4
        self.precession_omega = p_o = mag(cross(self.L,self.torque)/mag2(self.L)) / sin(ALPHA) * vector(0,1,0)
        self.friction =  - MASS * cross(p_o,cross(p_o,self.c_m))
        return self.L, self.torque, self.weight, self.norm, self.friction


# %% run code here
        
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
    
    st.set_vectors(dt)
    st.move_cone(dt)