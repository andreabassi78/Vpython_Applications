"""
Created on Fri Mar 26 17:47:54 2021

@author: Andrea Bassi
"""

from vpython import scene, vector, arrow, color, sphere, rate, attach_trail, pi, mag
 
body = sphere(radius = 0.05)
body.color = color.orange 

R = 1

body.velocity = vector(0,0.7,0) # velocità iniziale diretta verso l'alto
body.pos = vector(R,0,0)

attach_trail(body)

dt = 0.01

# mostra gli assi x e y
axis_x = arrow(pos=vector(0,0,0), axis=vector(1,0,0), shaftwidth=0.01)            
axis_y = arrow(pos=vector(0,0,0), axis=vector(0,1,0), shaftwidth=0.01)            

time = 0 

while True:   
    
    rate(100)
    
    time = time + dt
    
    # calcola la componente centripeta dell'accelerazione (modulo) 
    acceleration_C = mag(body.velocity)**2/R # mag calcola il modulo del vettore
    
    # scrivi l'accelarazione come vettore
    acceleration = - acceleration_C * body.pos / R
     
    # calcola il vettore velocità e il vettore posizione
    body.velocity = body.velocity + acceleration *dt
    body.pos = body.pos + body.velocity *dt
    
    # mostra a schermo il valore del tempo, x, y
    scene.caption= ("t:  "+ str(round(time,2))+"s"+ "\n"
                    "x: "+ str(round(body.pos.x,3)),"m","\n"
                    "y: "+ str(round(body.pos.y,3)),"m")
    
    
    