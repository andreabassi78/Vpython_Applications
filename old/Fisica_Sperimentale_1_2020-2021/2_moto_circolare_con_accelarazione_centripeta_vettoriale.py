"""
Created on Fri Mar 26 17:47:54 2021

@author: Andrea Bassi
"""

from vpython import scene, vector, arrow, color, sphere, rate, attach_trail, pi, mag, cross
 
body = sphere(radius = 0.05)
body.color = color.orange 

R = 1 #m

body.pos = vector(R,0,0)

attach_trail(body)

dt = 0.01

# mostra gli assi x e y
axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            

# definisco la velocità angolare come un vettore perpendicolare al piano di rotazione
omega = vector(0,0,0) # rad/s

alpha = vector(0,0,0.1) # rad/s**2

velocity = cross(omega,body.pos)

while True:   
    
    rate(100)
    
    # calcola il vettore accelerazione centripeta  
    acceleration_C = cross (omega, cross (omega, body.pos))
    acceleration_T = cross(alpha,body.pos)
    
    acceleration = acceleration_C + acceleration_T
    
    # aggiorna velocità e accelerazione
    omega = omega + alpha *dt
    velocity = velocity + acceleration *dt
    body.pos = body.pos + velocity * dt
    