# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:04:25 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, sin, cos, arrow, sphere, quad, text, cross, rate, mag, textures, vertex, pi, color


LENGTH = 20

# draw ceiling
a = vertex( pos=vector(-LENGTH/2,LENGTH,-LENGTH/2), texpos=vector(0,0,0))
b = vertex( pos=vector(LENGTH/2,LENGTH,-LENGTH/2) , texpos=vector(1,0,0))
c = vertex( pos=vector(LENGTH/2,LENGTH,LENGTH/2)  , texpos=vector(1,1,0))
d = vertex( pos=vector(-LENGTH/2,LENGTH,LENGTH/2) , texpos=vector(0,1,0))
Q = quad( vs =[a,b,c,d], texture = textures.wood )



THETA = 30 * pi/180
MASS = 1
g = -9.81

def show_arrows(function):
    
    def create_arrow(pend):
        vectors,colors = function(pend)
        idx = 0
        for key in vectors:
            if not hasattr(pend, key):
                setattr(pend, key, arrow(pos = pend.body.pos,
                                         axis = vectors[key],
                                         color = colors[key],
                                         shaftwidth=0.3,
                                         headwidth=1,
                                         headlength = 1
                                         )) 
                # text(text=key,
                #      align='lower_right',
                #      color=colors[key], 
                #      height = 1, 
                #      pos=vector(LENGTH,LENGTH-1.5*idx,0) )
                # idx+=1

            else:
                pass
                arr = getattr(pend, key)
                arr.pos = pend.body.pos
                arr.axis = vectors[key]
                
        return
    
    return create_arrow


class pendolum:
    
    def  __init__(self, length, angle0):
        
        self.length = length
        self.angle = angle0
        self.omega = 0
        # create mass
        body = sphere(radius = 1.2)
        body.pos = vector(length*sin(angle0), length*(1-cos(angle0)),0)
        body.color = color.orange
        self.body = body
        #create cord
        self.rope = arrow(pos = vector(0,LENGTH,0),
                          axis = body.pos, 
                          shaftwidth=0.15, headwidth=0.001, headlength = 0.001,
                          color = color.gray(0.7))
        self.rope.axis = self.body.pos - vector (0,LENGTH,0)  
        
        
        
    def set_velocity(self, dt):
        alpha = g * sin(self.angle) / self.length
        self.omega += alpha * dt
        
    def set_position(self, dt):
        self.angle += self.omega * dt
        self.body.pos = vector(self.length*sin(self.angle), self.length*(1-cos(self.angle)),0)
        self.rope.axis = self.body.pos - vector (0,LENGTH,0) 
    
    @show_arrows
    def calculate_vectors(self):
        origin = vector(0,LENGTH,0)
        r = self.body.pos-origin
        av = self.omega*vector(0,0,1)
        v = cross(av, r)   
        weight = g *vector(0,1,0) * MASS
        tension = MASS * (r/mag(r)*g*cos(self.angle) + cross(av,v)) 
        acceleration = (tension + weight) / MASS
        
        vectors = {"velocity":v,
                   "weight":weight,
                   "tension":tension,
                   "acceleration":acceleration}
        colors = {"velocity":color.green,
                  "weight":color.white,
                  "tension": color.magenta,
                  "acceleration": color.cyan}

        return vectors, colors

    
p = pendolum(LENGTH,THETA)

dt = 0.01    

scene.center = vector(0,LENGTH/2,0)
scene.waitfor('textures')
    
while True:
    rate(100)
    p.set_velocity(dt)
    p.set_position(dt)
    p.calculate_vectors()