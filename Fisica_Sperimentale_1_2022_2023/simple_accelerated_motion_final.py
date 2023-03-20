"""
Created on Mon May  6 10:10:23 2020

@author: Andrea Bassi
"""

from vpython import scene, vector, sphere, color, rate, arrow, pi, sin, cos, attach_trail, mag
body = sphere(radius = 0.05)
body.color = color.orange
r=1
dt = 0.005
axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)
attach_trail(body, color = color.red)
body.pos = vector(1,0,0)
body.velocity = vector (0,1,0) # velocità diretta verso l'alto

while True:
    rate(100)
    accelerazione_modulo = mag(body.velocity)**2/r
    accelerazione = - accelerazione_modulo * body.pos / mag(body.pos) # versore dato da: body.pos/mag(body.pos)
    body.velocity  = body.velocity + accelerazione *dt
    body.pos = body.pos + body.velocity *dt
    
    
    

    
    
    