# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 17:47:54 2021

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, rate, attach_trail, attach_arrow, pi, mag

def calola_energia_meccanica(body, k, M):
    r = mag(body.pos)
    U = -k /r
    K = 1/2 * M * mag(body.velocity)**2
    E = U + K
    return E
 
body = sphere(radius = 0.05)
body.color = color.orange 

body.pos = vector(1,0,0) # posizione iniziale
body.velocity = vector(0,0.5,0)
body.F = vector(0,0,0)

attach_trail(body)
attach_arrow(body, "F")
k = 0.5 # 
M = 1

# mostra gli assi x e y
axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            

dt = 0.01 #s

while True:   
    
    rate(100)
    r = mag(body.pos)
    u_r = body.pos/r
    body.F = -  k *u_r/r**2
    acceleration = body.F/M
    # aggiorna velocità e accelerazione
    body.velocity = body.velocity + acceleration *dt
    body.pos = body.pos + body.velocity * dt
    E = calola_energia_meccanica(body, k, M)
    print(E)    
    
    