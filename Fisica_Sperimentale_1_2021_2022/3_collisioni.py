from vpython import vector, sphere, arrow, mag, rate, dot, cross


def urto_anaelastico(b0,b1):
    ''' collisione anaelastica in cui consideriamo le sfere come collegate da una molla (durante l'urto)
    con in aggiunta un attrito viscoso dipendente dalla velocità relativa'''
    K = 300 # costante elastica
    B = 3 # damping
    vrel = b0.velocity - b1.velocity
    rrel = b0.pos - b1.pos
    distance = mag(rrel)
    F = K * rrel /distance * (b0.radius + b1.radius - distance) - B * vrel
    acceleration0 =  F / b0.mass
    acceleration1 = -F / b1.mass
    b0.velocity += acceleration0 * dt
    b1.velocity += acceleration1 *dt
    
    

def urto_elastico(b0,b1):
    '''collisione elastica in 3 dimensioni'''
    vrel = b0.velocity - b1.velocity
    rrel = b0.pos-b1.pos
    distance = mag(rrel)
    ratio0 = 2 * b1.mass / (b0.mass + b1.mass) 
    ratio1 = 2 * b0.mass / (b0.mass + b1.mass) 
    b0.velocity += - ratio0 * dot(vrel,rrel) / distance**2 *rrel 
    b1.velocity += - ratio1 * dot(-vrel,-rrel) / distance**2 *(-rrel)

def urto_completamente_anaelastico(b0,b1):
    '''
    velocità finale uguale, pari alla velocità del centro di massa
    '''
    m0 = b0.mass
    m1 = b1.mass
    p = b0.velocity * m0 + b1.velocity * m1
    vm = p /(m0+m1)
    b0.velocity = vm
    b1.velocity = vm

def calcola_energia_cinetica(b0,b1):
    KE = 1/2 * b0.mass * mag(b0.velocity)**2 + 1/2 * b1.mass * mag(b1.velocity)**2
    return KE
    
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
    
    KE = calcola_energia_cinetica(body0, body1)
    print('Energia cinetica (J):', KE)
    
    rate(200)
    body0.pos = body0.pos + body0.velocity*dt
    body1.pos = body1.pos + body1.velocity*dt
    # check collision
    distance = mag(body0.pos-body1.pos)
    if distance <= (body0.radius+body1.radius):
        urto_anaelastico(body0,body1)
        
        
    