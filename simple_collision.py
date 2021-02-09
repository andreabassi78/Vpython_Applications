# -*- coding: utf-8 -*-
"""
Created on Mon May  9 22:34:05 2020

@author: Andrea Bassi
"""
from vpython import vector, curve, color,scene, sphere, arrow, mag, rate, dot, cross

axis_x = arrow(pos=vector(-1,0,0), axis=vector(2,0,0), shaftwidth=0.006, headwidth=0.04, headlength = 0.05)            
axis_y = arrow(pos=vector(0,-1,0), axis=vector(0,2,0), shaftwidth=0.006, headwidth=0.04, headlength = 0.05)            

body0 = sphere()
body0.mass = 1
body0.radius = body0.mass/10
body0.pos = vector(-1,0,0)
body0.velocity = vector(1,0,0) 
body0.color =  vector(0.00,0.76,0.71)  

body1 = sphere()
body1.mass = 0.5
body1.radius = body1.mass/10
body1.pos = vector(1,0,0)
body1.velocity = vector(-1,0,0) 
body1.color =  vector(1.00,0.22,0.51)

def set_position(bodies,dt):
    for index, b in enumerate(bodies):
        b.pos = b.pos + b.velocity*dt
                  
def check_collision(body0,body1):
    distance = mag(body0.pos-body1.pos)
    if distance <= (body0.radius+body1.radius):
        #totally_inelastic_collision(body0,body1)           
        #elastic_collision(body0,body1)           
        inelastic_collision(body0,body1)           
                                          
def elastic_collision(body0,body1):
        vrel = body0.velocity - body1.velocity
        rrel = body0.pos-body1.pos
        a = rrel.mag2 # magnitude squared
        ratio0 = 2 * body1.mass / (body0.mass + body1.mass) 
        ratio1 = 2 * body0.mass / (body0.mass + body1.mass) 
        body0.velocity += - ratio0 * dot(vrel,rrel) / a  *rrel 
        body1.velocity += - ratio1 * dot(-vrel,-rrel) / a  *(-rrel)
    
def inelastic_collision(body0,body1,dt = 0.001):
    # ball is working as a springs with frinction proportional to velocity                 
    K = 200 # elastic constant (N/)
    B = 5 # damping
    vrel = body0.velocity - body1.velocity
    rrel = body0.pos - body1.pos
    distance =  mag (rrel)
    F = + K * rrel / distance * (body0.radius+body1.radius-distance)  - B * vrel
    acceleration0 = +F / body0.mass
    acceleration1 = -F / body1.mass
    body0.velocity = body0.velocity + acceleration0*dt
    body1.velocity = body1.velocity + acceleration1*dt    
    
def totally_inelastic_collision(body0,body1):
    m0 = body0.mass
    m1 = body1.mass
    #cm_pos = (body0.pos*m0+body1.pos*m1)/(m0+m1)
    cm_velocity = (body0.velocity*m0+body1.velocity*m1)/(m0+m1)            
    body0.velocity = cm_velocity 
    body1.velocity = cm_velocity

def calculate_center_of_mass_and_energy(body0,body1):
    m_tot = body0.mass + body1.mass
    c_m = ( body0.mass * body0.pos + body1.mass * body1.pos ) / m_tot
    v_m = ( body0.mass * body0.velocity + body1.mass * body1.velocity ) / m_tot
    KE = 1/2 * body0.mass * mag(body0.velocity)**2 + 1/2 * body1.mass * mag(body1.velocity)**2
    return c_m, v_m, KE  


# Set temporal sampling in seconds 
delta_t = 0.001 
time = 0

while mag(body0.pos)<1.5 and mag(body1.pos)<1.5:   
    rate(200)
    time = time + delta_t
    set_position([body0,body1],delta_t)      
    check_collision(body0,body1)
    c_m, v_m, KE = calculate_center_of_mass_and_energy(body0, body1)
    scene.caption= ("Time:  "+ str(round(time,2))+"s"+ "\n"
                    "Center of mass speed: "+ str(round(mag(v_m),3))," m/s","\n"
                    "Kinetic energy: "+ str(round(KE,3))," J")
    