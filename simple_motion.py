import vpython as vp

scene = vp.scene



axis_x = vp.arrow(pos=vp.vector(0,0,0), axis=vp.vector(1,0,0),shaftwidth=0.01)            
axis_y = vp.arrow(pos=vp.vector(0,0,0), axis=vp.vector(0,1,0),shaftwidth=0.01)            
#axis_z = vp.arrow(pos=vp.vector(0,0,0), axis=vp.vector(0,0,1),shaftwidth=0.01)  

body = vp.sphere()
body.radius = 0.05
body.color = vp.color.orange 


# Initial values
acceleration = vp.vector(0,-9.81,0)  
velocity = vp.vector(2,2,0) 
body.pos = vp.vector(0,0,0)
time = 0


# Set temporal sampling 
dt = 0.001 

# Set refresh rate
while True:   
    
    vp.rate(100)
    time = time + dt
    velocity = velocity + acceleration *dt
    body.pos = body.pos + velocity *dt

    scene.caption= ("t:"+ str(round(time,2))+"s "+ "\n"
                    "x:"+ str(round(body.pos.x,2)),"m","\n"
                    "y:"+ str(round(body.pos.y,2)),"m","\n"
                    "z:"+ str(round(body.pos.z,2)),"m")