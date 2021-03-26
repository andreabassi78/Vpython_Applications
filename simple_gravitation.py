# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:12:04 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, pi, mag, rate, attach_trail

G = 6.67408e-11 # Gravitational constant. All Units are in SI

# Set temporal sampling in seconds 
dt = 1000 
           
moon =  sphere() # sphere(make_trail=True)
moon.color =  vector(0.81,0.83,0.22)
moon.mass = 7.342e22
moon.radius = 10e6 # Exaggerated size of the Moon
moon.pos = vector(0, 4.054e8,0) # Moon at apogee (m)
moon.velocity = vector(-970,0,0) # Moon velocity at apogee(m/s)
# moon.texture = {'file':'/images/moon.jpg'}


earth =  sphere()
earth.color =  vector(0,0.56,0.61)  
earth.mass = 5.972e24
earth.radius = 50e6 # Exaggerated size of the Earth
earth.pos = vector(0,0,0)
earth.velocity =-moon.velocity*moon.mass/earth.mass # Conservation of momentum
# earth.texture = {'file':'/images/earth.jpg'}

while mag(moon.pos-earth.pos)>earth.radius: 
    
    rate(200)
    distance = moon.pos-earth.pos
    u = distance / mag(distance)
    # Force excerted on the Moon
    Force = - u * (G * earth.mass * moon.mass ) / mag(distance)**2
    
    # Second Newton's laws
    moon.acceleration = Force / moon.mass 
    moon.velocity = moon.velocity + moon.acceleration * dt
    moon.pos = moon.pos + moon.velocity * dt
    
    # Third Newton's laws
    earth.acceleration = - Force / earth.mass 
    earth.velocity = earth.velocity + earth.acceleration * dt
    earth.pos = earth.pos + earth.velocity * dt
    