from vpython import vector, sphere, arrow, mag, rate, dot, cross

def urto_completamente_anaelastico(b0,b1):
    pass

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
# Set temporal sampling in seconds 
dt = 0.001 

while mag(body0.pos)<1.5 and mag(body1.pos)<1.5:
    
    rate(200)
    body0.pos = body0.pos + body0.velocity*dt
    body1.pos = body1.pos + body1.velocity*dt
    # check collision
    distance = mag(body0.pos-body1.pos)
    if distance <= (body0.radius+body1.radius):
        print('collisione in corso')