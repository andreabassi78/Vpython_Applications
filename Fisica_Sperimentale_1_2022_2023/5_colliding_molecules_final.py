# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import gcurve, vector, curve, color, sphere, mag, rate, dot, attach_trail

def urto_elastico(body0,body1):
    '''collisione elastica in 3 dimensioni'''
    vrel = body0.velocity - body1.velocity
    rrel = body0.pos - body1.pos
    distance = mag(rrel)
    ratio0 = 2 * body1.mass / (body0.mass + body1.mass) 
    ratio1 = 2 * body0.mass / (body0.mass + body1.mass) 
    body0.velocity += - ratio0 * dot(vrel,rrel) / distance**2 *rrel 
    body1.velocity += - ratio1 * dot(-vrel,-rrel) / distance**2 *(-rrel)

def rimbalza_al_bordo(body, d):     
        loc = body.pos
        vel = body.velocity
        if abs(loc.x) > d:
            if loc.x < 0: vel.x =  abs(vel.x)
            else: vel.x =  -abs(vel.x)
        if abs(loc.y) > d:
            if loc.y < 0: vel.y = abs(vel.y)
            else: vel.y =  -abs(vel.y)
        if abs(loc.z) > d:
            if loc.z < 0: vel.z =  abs(vel.z)
            else: vel.z =  -abs(vel.z)

N = 1000 # numero di particelle
particelle = [] # lista che conterrà tutte le particelle (sphere)

g = 3 


for index in range(N):
    particella = sphere()
    particella.mass = 0.01
    particella.radius = 0.015
    particella.pos = vector.random()
    particella.velocity = vector.random()
    particella.color =  color.orange
    particella.acceleration = vector(0,-g,0)
    particelle.append(particella)  


# definisco il corpo polline
polline = sphere()
polline.mass = 1
polline.radius = 0.15
polline.pos = vector(0,0,0)
polline.velocity = vector(3,0,0)
polline.acceleration = vector(0,-g,0)
polline.color = color.green
attach_trail(polline, radius=0.006, retain=200, pps=1, type='points')



# Disegna un cubo di lato 2d
d = 1 # semilato del cubo
r = 0.005
gray = color.gray(0.7)
boxbottom = curve(color=gray, radius=r)
boxbottom.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d)])
boxtop = curve(color=gray, radius=r)
boxtop.append([vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,d,-d), vector(-d,d,-d)])
vert1 = curve(color=gray, radius=r)
vert2 = curve(color=gray, radius=r)
vert3 = curve(color=gray, radius=r)
vert4 = curve(color=gray, radius=r)
vert1.append([vector(-d,-d,-d), vector(-d,d,-d)])
vert2.append([vector(-d,-d,d), vector(-d,d,d)])
vert3.append([vector(d,-d,d), vector(d,d,d)])
vert4.append([vector(d,-d,-d), vector(d,d,-d)])

grafico0 = gcurve(color = color.cyan)
grafico1 = gcurve(color = color.red)

#campionamento temporale
dt = 0.005
t = 0 
while t<10:   
    
    rate(50)

    polline.velocity += polline.acceleration *dt
    polline.pos += polline.velocity*dt
    rimbalza_al_bordo(polline,d)

    for particella in particelle:
        distance = mag(particella.pos-polline.pos)
        if distance < particella.radius + polline.radius:
            urto_elastico(polline, particella)


    
    # aggiorna la posizione di ogni particella
    for particella in particelle:
        particella.velocity += particella.acceleration*dt
        particella.pos += particella.velocity*dt 
        rimbalza_al_bordo(particella,d)
    
    t += dt

    grafico0.plot(t, abs(polline.velocity.x) )
    grafico1.plot(t, abs(polline.velocity.y) )