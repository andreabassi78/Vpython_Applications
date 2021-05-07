# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, curve, color, sphere, mag, rate, dot, cross, attach_trail
  
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
        for other_body in bodies:
            if body is not other_body:
                distance =  mag (body.pos - other_body.pos)
                if distance < (body.radius + other_body.radius):
                    print('collisione!')
    
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
    
        