from vpython import *
#GlowScript 3.0 VPython
scene.width = scene.height = 600
scene.range = 0.6

# A pulse ripples along a rug, demonstrating dynamic changea of shape
# Bruce Sherwood, May 2012

def display_instructions():
    s = """In GlowScript programs:
  To rotate "camera", drag with right button or Ctrl-drag.
  To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
  To pan left/right and up/down, Shift-drag.
  Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.caption = s
    
display_instructions()

# Construct a square WxH divided into little squares
# There are (w+1)x(h+1) vertices
# Center of rug is at 0,0,0

H = W = 1
w = 1
h = 1
dx = W/w
dy = H/h

# Create a grid of vertex objects covering the rug
verts = []
for y in range(h+1): # from 0 to h inclusive, to include both bottom and top edges
    verts.append([])
    for x in range(w+1): # from 0 to w inclusive, to include both left and right edges
        verts[y].append(vertex(pos=vector(-0.5+x*dx,-0.5+y*dy,0), texpos=vector(x,y,0)))


print(verts[1][0].pos)

LENGTH = 0.5
verts[0][0] = vertex( pos=vector(-1,0,-1) * LENGTH, texpos=vector(0,0,0))
verts[0][1] = vertex( pos=vector(1,0,-1) * LENGTH , texpos=vector(1,0,0))
verts[1][1] = vertex( pos=vector(1,0,1) * LENGTH , texpos=vector(1,1,0))
verts[1][0] = vertex( pos=vector(-1,0,1) * LENGTH, texpos=vector(0,1,0))

print(verts[1][0].pos)

# Create quads (equivalent to two triangles) based on the vertex objects just created.
# Note that a particular vertex may be shared by as many as 4 neighboring quads, and
# changing one vertex affects all of the quads that use that vertex.
#for y in range(h): # from 0 to h, not including h
 #   for x in range(w): # from 0 to w, not including w
quad(vs=[verts[0][0], verts[0][1], verts[1][1], verts[1][0]], texture=textures.rug)

scene.waitfor('textures') # wait until the rug texture has been loaded
