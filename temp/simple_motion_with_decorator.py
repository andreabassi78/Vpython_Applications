"""
Created on Mon May  6 10:10:23 2020

@author: Andrea Bassi
"""
from vpython import scene, vector, arrow, color, sphere, pi, mag, rate

def vectorize(func):
    
    def inner(*args,**kwargs):
        print(inner.called)
        
        SCALE = 0.2
        r,v = func(*args)
            
        if not inner.called:
            inner.r_arrow = arrow(pos = vector(0,0,0), axis =r, color = color.green)
            inner.v_arrow = arrow(pos = r, axis =v * SCALE, color = color.cyan)
            inner.called = True
        else:
            inner.r_arrow.axis = r
            inner.v_arrow.pos = r
            inner.v_arrow.axis = v*SCALE
            
        return r,v
    inner.called = False
    
    return(inner)
    
axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            

body = sphere(radius = 0.05)
body.color = color.orange 

# Initial values
acceleration = vector(0,-9.81,0)  
velocity = vector(2,2,0) 
body.pos = vector(0,0,0)
time = 0

@vectorize
def set_pos_vel(pos, velocity, acceleration, dt):
    velocity = velocity + acceleration *dt
    pos = pos + velocity *dt

    return pos, velocity

# Set time interval
dt = 0.001 

# Set refresh rate
while body.pos.y>=0:   
    
    rate(100)
    body.pos, velocity = set_pos_vel(body.pos,velocity,acceleration,dt)
    
    