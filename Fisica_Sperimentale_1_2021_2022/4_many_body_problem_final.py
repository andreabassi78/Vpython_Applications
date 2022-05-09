# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, curve, color, sphere, mag, rate, dot, cross

def urto_completamente_anaelastico(body0,body1):
    '''velocità finale uguale, pari alla velocità del centro di massa'''
    m0 = body0.mass
    m1 = body1.mass
    p = body0.velocity*m0+body1.velocity*m1
    vm = p/(m0+m1)            
    body0.velocity = vm 
    body1.velocity = vm    

def urto_elastico(body0,body1):
    '''collisione elastica in 3 dimensioni'''
    vrel = body0.velocity - body1.velocity
    rrel = body0.pos - body1.pos
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
                    urto_anaelastico(body, other_body)
                else:
                    body.acceleration += - (G * other_body.mass) * (body.pos - other_body.pos)/ distance**3
        body.velocity += body.acceleration *dt 
    
    # aggiorna la posizione di ogni corpo
    for body in bodies:
        body.pos += body.velocity*dt   
    
    # calcola il vettore centro di massa
    c_m = vector(0,0,0)
    m_tot = 0
    for body in bodies:
        c_m += body.mass * body.pos
        m_tot += body.mass
    center_mass.pos = c_m / m_tot  
    
    # ricentra il sistem nel centro di massa
    scene.center = center_mass.pos
   
        