"""
Created on Fri Mar 26 17:47:54 2021

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, rate, sin, cos, attach_trail, pi

body = sphere(radius = 0.05)
body.color = color.orange 

R = 1

body.pos = vector(1,0,0)

attach_trail(body)

omega = 5 # rad/s # modulo della velocità angolare 

time = 0

dt = 0.001

axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            

while True:   
    
    rate(100)
    
    time = time + dt
    
    body.pos.x = R* cos(omega*time) # coordinata x in un moto circolare uniforme
    body.pos.y = R* sin(omega*time)
    
    
    
    