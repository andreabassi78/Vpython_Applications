# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 17:46:47 2022

@author: andrea
"""


from vpython import scene, vector, arrow, color, sphere, rate, sin, cos, attach_trail, mag, pi

R = 1

body = sphere(radius=0.05)
body.color = color.orange

body.pos = vector(1,0,0)

body.velocity = vector(0, 0.5, 0) # velocità iniziale diretta verso l'alto

attach_trail(body, color = color.red)

dt = 0.01

axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)

while True:
    
    rate(100)
    
    accelerazione_abs =  mag(body.velocity)**2/R # modulo dell'accelerazione centripeta
    
    accelerazione =  - accelerazione_abs * body.pos/R
    
    body.velocity = body.velocity + accelerazione * dt
    
    body.pos = body.pos + body.velocity * dt
    
    
    
    
    