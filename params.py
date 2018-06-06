import glm
from ctypes import c_void_p

# Global window
window = None
null = c_void_p(0)

#for view matrix
#position = glm.vec3(20,15,10)
position = glm.vec3(9.59996,8.13144,20.7899) #This position vector is being used for backprojection. Use the original one normally.
#front = glm.vec3(0,-2,-5)
front = glm.vec3(1.4437e-05,0,-1) #Using for backprojection
up = glm.vec3(0,1,0) 

#for projection/perspective matrix
fov = 45
aspect_ratio = 1024/768
near_clipping_plane = 0.1
far_clipping_plane = 200.0

#for mouse movements
lastX = 512
lastY = 256
pitch = 0
yaw = 3.14
firstmouse = True

#MVC!
model = lambda: glm.mat4(1.0)
view = lambda: glm.lookAt(position, position+front, up)
#projection = lambda: glm.perspective(fov, aspect_ratio, near_clipping_plane, far_clipping_plane)
projection = lambda: glm.ortho(-10,30,-10,20,0.1,100) #Using for backprojection.
#time
t = 0

#Lighting parameters and matrices
light_color = glm.vec3(1.0,1.0,1.0)
light_position = glm.vec3(0.0,2.0,5.0)
near_plane = 0.1 #Near clipping plane for the light's projection matrix
far_plane = 130.0 #Far clipping plane for the light's projection matrix
