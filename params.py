import glm
from ctypes import c_void_p

# Global window
window = None
null = c_void_p(0)

#for perspective view matrix
position = glm.vec3(20,15,10)
front = glm.vec3(0,-2,-5)
#front = glm.vec3(0,0,-1)
up = glm.vec3(0,1,0) 
#orthogonal view matrix (Keep scale (in ply_model file) to 0.04)
ortho_position = glm.vec3(6.37698, 5.92235, 15.8825) #This position vector is being used for backprojection. Use the original one normally.
ortho_front = glm.vec3(-0.00087995, 0.0137004, -0.999906) #Using for backprojection

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
projection = lambda: glm.perspective(fov, aspect_ratio, near_clipping_plane, far_clipping_plane)

ortho_view = lambda: glm.lookAt(ortho_position, ortho_position+ortho_front,up)
ortho_projection = lambda: glm.ortho(-10,30,-10,20,0.1,100) #Using for backprojection.

#time
t = 0

#Lighting parameters and matrices
light_color = glm.vec3(1.0,1.0,1.0)
light_position = glm.vec3(0.0,2.0,5.0)
near_plane = 0.1 #Near clipping plane for the light's projection matrix
far_plane = 130.0 #Far clipping plane for the light's projection matrix

#Toggle
switch = True

screenshot_taken = False
