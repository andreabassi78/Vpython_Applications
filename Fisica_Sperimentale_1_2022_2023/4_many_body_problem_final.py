# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, curve, color, sphere, mag, rate, dot, cross, attach_trail

def urto_anaelastico(b0,b1,dt):
    """ collisione anaelastica tra due corpi collegari ad una molla (solo durante la collisione) con 
     un attrito viscoso che dipense dalla velocità relativa """
    K = 300
    B = 3
    vrel = b0.velocity - b1.velocity
    rrel = b0.pos - b1.pos
    distance = mag (rrel)
    F =  K * rrel/distance * (b0.radius + b1.radius - distance) - B * vrel 
    accelaratione0 = F/b0.mass
    accelaratione1 = -F/b1.mass
    b0.velocity = b0.velocity + accelaratione0 * dt
    b1.velocity = b1.velocity + accelaratione1 * dt

def urto_completamente_anaelastico(b0,b1):
    """velocità finale uguale alla velocità del centro di massa"""
    m0 = b0.mass
    m1 = b1.mass
    p = m0 *b0.velocity + m1 *b1.velocity
    vm =  p /(m0+m1)
    b0.velocity = vm
    b1.velocity = vm

def urto_elastico(b0,b1):
    '''collisione elastica in 3 dimensioni'''
    vrel = b0.velocity - b1.velocity
    rrel = b0.pos-b1.pos
    distance = mag(rrel)
    ratio0 = 2 * b1.mass / (b0.mass + b1.mass) 
    ratio1 = 2 * b0.mass / (b0.mass + b1.mass) 
    b0.velocity += - ratio0 * dot(vrel,rrel) / distance**2 *rrel 
    b1.velocity += - ratio1 * dot(-vrel,-rrel) / distance**2 *(-rrel)


G = 1 # costante gravitazione 

N = 10 # numero di corpi
bodies = [] # lista che conterrà tutti i corpi (sphere)

for index in range(N):
    body = sphere()
    body.mass = 0.5
    body.radius = 0.05
    body.pos = vector.random()
    body.velocity = vector.random()
    body.color =  color.orange
    bodies.append(body)  

dt = 0.005 # campionamento temporale


# sfera con traiettoria che useremo per mostrare il centro di massa
center_mass = sphere(radius = 0.01,
                    make_trail=True,
                    trail_type="points",
                    trail_radius= 0.001,
                    interval=20,
                    retain=50)


while True:   
    
    rate(50)
    
    # controlla se ci sono collisioni
    for body in bodies:
        body.acceleration = vector(0,0,0)
        for other_body in bodies:
            if body is not other_body:
                distance =  mag (body.pos - other_body.pos)
                if distance < (body.radius + other_body.radius):
                    urto_anaelastico(body,other_body, dt)
                else:
                    body.acceleration += - G * other_body.mass /distance**3 * (body.pos - other_body.pos)
        body.velocity += body.acceleration * dt
    
    # aggiorna la posizione di ogni corpo
    for body in bodies:
        body.pos += body.velocity*dt
        # body.pos = body.pos + body.velocity*dt   
    
    # calcola il vettore centro di massa
    c_m = vector(0,0,0)
    m_tot = 0
    for body in bodies:
        c_m += body.mass * body.pos
        m_tot += body.mass    
    center_mass.pos = c_m / m_tot  
    
    # ricentra il sistema nel centro di massa
    scene.center = center_mass.pos
    
        