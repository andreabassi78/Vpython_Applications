# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 16:24:05 2021

@author: Andrea Bassi
"""
from vpython import vector, sphere, arrow, mag, rate, dot, cross

axis_x = arrow(pos=vector(-1,0,0), axis=vector(2,0,0), shaftwidth=0.006, headwidth=0.04, headlength = 0.05)            
axis_y = arrow(pos=vector(0,-1,0), axis=vector(0,2,0), shaftwidth=0.006, headwidth=0.04, headlength = 0.05)            

body0 = sphere()
body0.mass = 1
body0.radius = 0.1
body0.pos = vector(-1,0,0)
body0.velocity = vector(1,0,0) 
body0.color =  vector(0.0,0.76,0.71)  

body1 = sphere()
body1.mass = 0.5
body1.radius = 0.05
body1.pos = vector(1,0,0)
body1.velocity = vector(-1,0,0) 
body1.color =  vector(1.00,0.22,0.51)
                                      
def urto_elastico(body0,body1):
    '''collisione elastica in 3 dimensioni'''
    vrel = body0.velocity - body1.velocity
    rrel = body0.pos-body1.pos
    distance = mag(rrel)
    ratio0 = 2 * body1.mass / (body0.mass + body1.mass) 
    ratio1 = 2 * body0.mass / (body0.mass + body1.mass) 
    body0.velocity += - ratio0 * dot(vrel,rrel) / distance**2 *rrel 
    body1.velocity += - ratio1 * dot(-vrel,-rrel) / distance**2 *(-rrel)
    
def urto_inelastico(body0,body1):
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
    
def urto_completamente_inelastico(body0,body1):
    '''velocità finale uguale, pari alla velocità del centro di massa'''
    m0 = body0.mass
    m1 = body1.mass
    p = body0.velocity*m0+body1.velocity*m1
    vm = p/(m0+m1)            
    body0.velocity = vm 
    body1.velocity = vm

# Set temporal sampling in seconds 
dt = 0.001 

while mag(body0.pos)<1.5 and mag(body1.pos)<1.5:   
    
    rate(200)
    body0.pos = body0.pos + body0.velocity*dt
    body1.pos = body1.pos + body1.velocity*dt
    
    # check collision
    distance = mag(body0.pos-body1.pos)
    if distance <= (body0.radius+body1.radius):
        # print ('collision!')
        urto_inelastico(body0,body1)    
    
    m_tot = body0.mass + body1.mass
    c_m = ( body0.mass * body0.pos + body1.mass * body1.pos ) / m_tot
    p = ( body0.mass * body0.velocity + body1.mass * body1.velocity ) / m_tot
    KE = 1/2 * body0.mass * mag(body0.velocity)**2 + 1/2 * body1.mass * mag(body1.velocity)**2
    
    #print('center of mass:',c_m)
    print('quantità di moto (kg*m/s):',mag(p))
    #print('energia cinetica(J):', KE)
    