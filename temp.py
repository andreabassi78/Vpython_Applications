# -*- coding: utf-8 -*-
"""
Created on Fri May  7 16:48:33 2021

@author: andrea
"""

from vpython import vector, color, sphere, arrow, mag, rate, dot, cross, attach_trail, scene

def urto_elastico(body0,body1):
    '''collisione elastica in 3 dimensioni'''
    vrel = body0.velocity - body1.velocity
    rrel = body0.pos-body1.pos
    distance = mag(rrel)
    ratio0 = 2 * body1.mass / (body0.mass + body1.mass) 
    ratio1 = 2 * body0.mass / (body0.mass + body1.mass) 
    body0.velocity += - ratio0 * dot(vrel,rrel) / distance**2 *rrel 
    body1.velocity += - ratio1 * dot(-vrel,-rrel) / distance**2 *(-rrel)
    
def urto_anaelastico(body0,body1):
    ''' collisione inelastica in cui consideriamo la passa come una molla
    con in aggiunta un attrito viscoso dipendente dalla velocità relativa'''                
    dt = 0.001
    K = 300 # elastic constant
    B = 3 # damping
    vrel = body0.velocity - body1.velocity
    rrel = body0.pos - body1.pos
    distance =  mag (rrel)
    F = + K * rrel / distance * (body0.radius+body1.radius-distance) - B * vrel
    acceleration0 = +F / body0.mass
    acceleration1 = -F / body1.mass
    body0.velocity = body0.velocity + acceleration0*dt
    body1.velocity = body1.velocity + acceleration1*dt    
    
def urto_completamente_anaelastico(body0,body1):
    '''velocità finale uguale, pari alla velocità del centro di massa'''
    m0 = body0.mass
    m1 = body1.mass
    p = body0.velocity*m0+body1.velocity*m1
    vm = p/(m0+m1)            
    body0.velocity = vm 
    body1.velocity = vm


G = 1 # costante gravitazionale

N = 10 # numero di corpi

bodies = [] # lista  che conterrà i corpi (sfere)

for index in range(N):
    body = sphere()
    body.mass = 2
    body.radius = 0.05
    body.pos = vector.random()
    body.velocity = vector.random()
    body.color = color.orange
    bodies.append(body)

dt = 0.005 # campionamento temporale    


center_mass = sphere(radius = 0.01)
# center_mass.radius = 0.001
attach_trail(center_mass, retain=30, pps=5, type='points')
    
while True:
    
    rate(50)
    
    # controlla se ci sono collisioni
    for idx,body in enumerate(bodies):
        body.force = vector(0,0,0)
        for other_body in bodies:
            if body is not other_body:
                distance = mag (body.pos -other_body.pos)
                if distance < (body.radius + other_body.radius):
                    urto_anaelastico(body, other_body)
                else:
                    body.force += - G * body.mass *other_body.mass / distance**2 * (body.pos- other_body.pos) /distance
        body.acceleration = body.force / body.mass
        body.velocity += body.acceleration * dt             
    
               
    for body in bodies:
        body.pos += body.velocity *dt
    
    c_m = vector(0,0,0)
    m_tot = 0
    for body in bodies:
        c_m += body.mass * body.pos
        m_tot += body.mass
    center_mass.pos = c_m / m_tot
    
    scene.center = bodies[0].pos
    
    


    
    

