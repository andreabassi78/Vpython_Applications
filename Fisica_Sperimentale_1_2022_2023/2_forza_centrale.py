# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:24:39 2022

@author: andrea
"""

from vpython import scene, vector, arrow, color, sphere, rate, attach_arrow, attach_trail, mag, pi, cross

def calcola_energia_meccanica(body, K, m):
    distanza = mag(body.pos)
    U = -K*m/distanza # energia potenziale
    KE = 1/2 * m * mag(body.velocity)**2 # energia cinetica
    E_tot = U + KE
    return E_tot

def calcola_momento_angolare(body,K,m):
    r = body.pos
    p = m * body.velocity
    L = cross(r,p)
    return L


body = sphere(radius=0.05)
body.color = color.orange
body.pos = vector(1.0,0.0,0.0)
body.velocity = vector(0, 0.8, 0)
body.forza = vector(0,0,0)

axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)       
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)

K = 1 #G*M
m = 1 # massa del corpo

attach_trail(body)
attach_arrow(body, "forza" )

dt = 0.01
while True:
    
    rate(100)
    r = body.pos 
    u_r = r/mag(r)
    body.forza = - K*m * u_r /mag(r)**2 # forza gravitazionale
    # body.forza = - K *u_r * mag(r) # forza elastica
    accelerazione  = body.forza / m
    body.velocity += accelerazione * dt    
    # body.velocity = body.velocity + accelerazione * dt 
    body.pos +=  body.velocity * dt
    E = calcola_energia_meccanica(body,K,m)
    print(E)
    # L = calcola_momento_angolare(body,K,m)
    # print(mag(L))
    
    
    