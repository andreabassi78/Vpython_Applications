# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 17:47:54 2021

@author: Andrea Bassi
"""
from vpython import scene, dot, vector, arrow, color, sphere, rate, attach_trail, attach_arrow, pi, mag

def urto_completamente_anaelastico(b0,b1):
    m0 = body0.mass
    m1 = body1.mass
    p = body0.velocity * m0 + body1.velocity *m1 # quantità di moto
    vm = p /(m0+m1)
    b0.velocity = vm
    b1.velocity = vm
    
def urto_elastico(b0,b1):
    vrel = b0.velocity - b1.velocity
    rrel = b0.pos - b1.pos
    distance = mag(rrel)
    ratio0 = 2 * b1.mass / (b0.mass + b1.mass)
    ratio1 = 2 * b0.mass / (b0.mass + b1.mass)
    b0.velocity -= ratio0 * dot(vrel,rrel) / distance**2 * rrel
    b1.velocity -= ratio1 * dot(-vrel,-rrel) / distance**2 * (-rrel)
      
def urto_anaelastico(b0,b1):
    dt = 0.001
    K = 300 # elastic constant 
    B = 0 # damping
    vrel = b0.velocity - b1.velocity
    rrel = b0.pos - b1.pos
    distance = mag(rrel)
    F = K * rrel /distance * (b0.radius + b1.radius - distance) - B * vrel
    acceleration0 = F /b0.mass
    acceleration1 = -F /b1.mass
    b0.velocity += acceleration0 * dt
    b1.velocity += acceleration1 * dt
     
body0 = sphere(radius = 0.05)
body0.color = color.orange 
body0.pos = vector(-1,0,0) # posizione iniziale
body0.velocity = vector(1,0,0)
body0.mass = 1
body0.radius = 0.1

body1 = sphere(radius = 0.05)
body1.color = color.green 
body1.pos = vector(1,0,0) # posizione iniziale
body1.velocity = vector(-1,0,0)
body1.mass = 0.5
body1.radius = 0.05

# mostra gli assi x e y
axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            

dt = 0.001 #s

while mag(body0.pos)<1.5 and mag(body1.pos)<1.5:
    
    rate(200)
    # body.velocity = body.velocity + acceleration *dt
    body0.pos = body0.pos + body0.velocity * dt
    body1.pos = body1.pos + body1.velocity * dt
    
    distance = mag(body0.pos - body1.pos)
    if distance <= (body0.radius + body1.radius):
        urto_anaelastico(body0,body1)
        
    p = body0.velocity * body0.mass + body1.velocity * body1.mass
    KE = 1/2 * body0.mass *mag(body0.velocity)**2 + 1/2 * body1.mass * mag(body1.velocity)**2
    
    # print('quantità di moto (kg*m/s):', mag(p))
    print('energia cinetica (J):', KE)
    
    